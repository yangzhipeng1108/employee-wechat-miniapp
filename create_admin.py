#!/usr/bin/env python
"""创建默认管理员账号"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wxcloudrun.settings')
django.setup()

from wxcloudrun.models import Employee

def create_admin():
    """创建默认管理员账号"""
    admin_code = os.environ.get('ADMIN_CODE', 'admin')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    try:
        admin = Employee.objects.get(employee_code=admin_code)
        print(f'管理员 {admin_code} 已存在，跳过创建')
        return admin
    except Employee.DoesNotExist:
        admin = Employee(
            employee_code=admin_code,
            name='管理员',
            department='管理部',
            position='管理员',
            role='admin',
            is_staff=True,
            is_superuser=True,
        )
        admin.set_password(admin_password)
        admin.save()
        print(f'默认管理员账号创建成功！')
        print(f'工号: {admin_code}')
        print(f'密码: {admin_password}')
        return admin

if __name__ == '__main__':
    create_admin()