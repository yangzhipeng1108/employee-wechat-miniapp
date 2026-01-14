from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import bcrypt


class Employee(AbstractUser):
    """员工模型"""
    employee_code = models.CharField(max_length=20, unique=True, verbose_name='工号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    password = models.CharField(max_length=255, verbose_name='密码')
    department = models.CharField(max_length=50, blank=True, verbose_name='部门')
    position = models.CharField(max_length=50, blank=True, verbose_name='职位')
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    hire_date = models.DateField(null=True, blank=True, verbose_name='入职日期')
    role = models.CharField(max_length=20, default='employee', verbose_name='角色')
    wechat_openid = models.CharField(max_length=100, blank=True, null=True, verbose_name='微信OpenID')
    avatar_url = models.URLField(blank=True, verbose_name='头像URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'employees'
        verbose_name = '员工'
        verbose_name_plural = '员工'

    def __str__(self):
        return f"{self.name} ({self.employee_code})"

    def set_password(self, raw_password):
        """设置密码（使用bcrypt加密）"""
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        """验证密码"""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    def to_dict(self):
        """转换为字典（排除密码）"""
        data = {
            'id': self.id,
            'employee_code': self.employee_code,
            'name': self.name,
            'department': self.department,
            'position': self.position,
            'phone': self.phone,
            'email': self.email,
            'hire_date': self.hire_date.strftime('%Y-%m-%d') if self.hire_date else None,
            'role': self.role,
            'wechat_openid': self.wechat_openid,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
        }
        return data


class Salary(models.Model):
    """工资单模型"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='员工')
    period = models.CharField(max_length=10, verbose_name='月份')  # 格式: 2024-01
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='基本工资')
    performance_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='绩效工资')
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='加班费')
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='奖金')
    allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='补贴')
    social_security = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='社保')
    housing_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='公积金')
    income_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='个税')
    other_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='其他扣除')
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='总收入')
    total_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='总扣除')
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='实发工资')
    pay_date = models.DateField(null=True, blank=True, verbose_name='发放日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'salaries'
        verbose_name = '工资单'
        verbose_name_plural = '工资单'
        unique_together = ('employee', 'period')

    def __str__(self):
        return f"{self.employee.name} - {self.period}"

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'period': self.period,
            'base_salary': float(self.base_salary),
            'performance_salary': float(self.performance_salary),
            'overtime_pay': float(self.overtime_pay),
            'bonus': float(self.bonus),
            'allowance': float(self.allowance),
            'social_security': float(self.social_security),
            'housing_fund': float(self.housing_fund),
            'income_tax': float(self.income_tax),
            'other_deduction': float(self.other_deduction),
            'total_income': float(self.total_income),
            'total_deduction': float(self.total_deduction),
            'net_salary': float(self.net_salary),
            'pay_date': self.pay_date.strftime('%Y-%m-%d') if self.pay_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        }


class Notice(models.Model):
    """公告模型"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(blank=True, verbose_name='内容')
    date = models.DateField(verbose_name='日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'notices'
        verbose_name = '公告'
        verbose_name_plural = '公告'

    def __str__(self):
        return self.title

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'date': self.date.strftime('%Y-%m-%d'),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        }
