from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.db.models import Count, Sum, Q
from .models import Employee, Salary, Notice
from .serializers import (
    EmployeeSerializer, EmployeeDetailSerializer, SalarySerializer, 
    NoticeSerializer, LoginSerializer, 
    WechatLoginSerializer, BindWechatSerializer
)


class EmployeeViewSet(viewsets.ModelViewSet):
    """员工视图集"""
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return EmployeeDetailSerializer
        return EmployeeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # 管理员可以查看所有员工，员工只能查看自己
        if not self.request.user.role == 'admin':
            queryset = queryset.filter(id=self.request.user.id)
        return queryset

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """员工登录"""
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'message': '请输入工号和密码'},
                status=status.HTTP_400_BAD_REQUEST
            )

        employee_code = serializer.validated_data['employee_code']
        password = serializer.validated_data['password']

        try:
            employee = Employee.objects.get(employee_code=employee_code)
        except Employee.DoesNotExist:
            return Response(
                {'success': False, 'message': '工号或密码错误'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not employee.check_password(password):
            return Response(
                {'success': False, 'message': '工号或密码错误'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 生成JWT token
        refresh = RefreshToken.for_user(employee)
        
        return Response({
            'success': True,
            'token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'employee': EmployeeSerializer(employee).data
        })

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def wechat_login(self, request):
        """微信登录"""
        serializer = WechatLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'message': '参数错误'},
                status=status.HTTP_400_BAD_REQUEST
            )

        code = serializer.validated_data['code']
        # 这里应该调用微信API获取openid
        # 简化处理，使用mock数据
        mock_openid = f'mock_openid_{timezone.now().timestamp()}'

        try:
            employee = Employee.objects.get(wechat_openid=mock_openid)
        except Employee.DoesNotExist:
            # 新用户需要绑定账号
            return Response({
                'success': False,
                'message': '请先使用工号和密码登录，然后在个人中心绑定微信'
            })

        # 生成JWT token
        refresh = RefreshToken.for_user(employee)
        
        return Response({
            'success': True,
            'token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'employee': EmployeeSerializer(employee).data
        })

    @action(detail=False, methods=['post'])
    def bind_wechat(self, request):
        """绑定微信"""
        serializer = BindWechatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'message': '参数错误'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_info = serializer.validated_data.get('userInfo', {})
        mock_openid = f'mock_openid_{timezone.now().timestamp()}'

        employee = request.user
        employee.wechat_openid = mock_openid
        if user_info.get('avatarUrl'):
            employee.avatar_url = user_info.get('avatarUrl')
        employee.save()

        return Response({'success': True, 'message': '绑定成功'})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """获取统计数据"""
        employee = request.user
        
        # 获取本月工资
        current_month = timezone.now().strftime('%Y-%m')
        try:
            salary = Salary.objects.get(employee=employee, period=current_month)
            total_salary = float(salary.net_salary)
        except Salary.DoesNotExist:
            total_salary = 0

        return Response({
            'success': True,
            'totalSalary': total_salary
        })


class SalaryViewSet(viewsets.ModelViewSet):
    """工资单视图集"""
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 只能查看自己的工资单（除非是管理员）
        if not self.request.user.role == 'admin':
            queryset = queryset.filter(employee=self.request.user)
        
        # 支持按月份筛选
        employeeId = self.request.query_params.get('employeeId')
        period = self.request.query_params.get('period')
        
        if employeeId:
            queryset = queryset.filter(employee_id=employeeId)
        if period:
            queryset = queryset.filter(period=period)
        
        return queryset.order_by('-created_at')

    def create(self, request, *args, **kwargs):
        """生成工资单（仅管理员）"""
        if not request.user.role == 'admin':
            return Response(
                {'success': False, 'message': '权限不足'},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data.copy()
        # 计算总收入和总扣除
        total_income = (float(data.get('base_salary', 0)) + 
                       float(data.get('performance_salary', 0)) + 
                       float(data.get('overtime_pay', 0)) + 
                       float(data.get('bonus', 0)) + 
                       float(data.get('allowance', 0)))
        total_deduction = (float(data.get('social_security', 0)) + 
                          float(data.get('housing_fund', 0)) + 
                          float(data.get('income_tax', 0)) + 
                          float(data.get('other_deduction', 0)))
        
        data['total_income'] = total_income
        data['total_deduction'] = total_deduction
        data['net_salary'] = total_income - total_deduction

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'message': '数据验证失败', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response({
            'success': True,
            'message': '生成成功',
            'salaryId': serializer.data['id']
        }, status=status.HTTP_201_CREATED)


class NoticeViewSet(viewsets.ReadOnlyModelViewSet):
    """公告视图集"""
    queryset = Notice.objects.all().order_by('-created_at')
    serializer_class = NoticeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset[:5]


class AdminViewSet(viewsets.ViewSet):
    """管理员视图集"""
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        """检查管理员权限"""
        if request.user.role != 'admin':
            return Response(
                {'success': False, 'message': '权限不足'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().initial(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """获取全局统计"""
        total_employees = Employee.objects.count()

        current_month = timezone.now().strftime('%Y-%m')
        salary_result = Salary.objects.filter(period=current_month).aggregate(
            total=Sum('net_salary')
        )
        total_salary = int(salary_result['total'] or 0)

        return Response({
            'success': True,
            'stats': {
                'totalEmployees': total_employees,
                'totalSalary': total_salary
            }
        })

    @action(detail=False, methods=['post'])
    def employees(self, request):
        """添加员工"""
        serializer = EmployeeDetailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'message': '数据验证失败', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.validated_data.get('employee_code') and Employee.objects.filter(
            employee_code=serializer.validated_data['employee_code']
        ).exists():
            return Response(
                {'success': False, 'message': '工号已存在'},
                status=status.HTTP_400_BAD_REQUEST
            )

        employee = serializer.save()
        
        return Response({
            'success': True,
            'message': '添加成功',
            'employeeId': employee.id
        }, status=status.HTTP_201_CREATED)
