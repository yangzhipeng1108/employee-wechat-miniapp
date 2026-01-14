from rest_framework import serializers
from .models import Employee, Salary, Notice


class EmployeeSerializer(serializers.ModelSerializer):
    """员工序列化器"""
    class Meta:
        model = Employee
        fields = ['id', 'employee_code', 'name', 'department', 'position', 
                  'phone', 'email', 'hire_date', 'role', 'avatar_url']
        read_only_fields = ['id']


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """员工详细信息序列化器"""
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class SalarySerializer(serializers.ModelSerializer):
    """工资单序列化器"""
    class Meta:
        model = Salary
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class NoticeSerializer(serializers.ModelSerializer):
    """公告序列化器"""
    class Meta:
        model = Notice
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    employee_code = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class WechatLoginSerializer(serializers.Serializer):
    """微信登录序列化器"""
    code = serializers.CharField(required=True)
    userInfo = serializers.DictField(required=False)


class BindWechatSerializer(serializers.Serializer):
    """绑定微信序列化器"""
    code = serializers.CharField(required=False)
    userInfo = serializers.DictField(required=False)
