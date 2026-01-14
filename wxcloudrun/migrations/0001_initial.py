# Generated migration using Django conventions for custom user model

from django.db import migrations, models
import django.utils.timezone
import django.contrib.auth.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('employee_code', models.CharField(max_length=20, unique=True, verbose_name='工号')),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('department', models.CharField(max_length=50, verbose_name='部门')),
                ('position', models.CharField(max_length=50, verbose_name='职位')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='联系电话')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱')),
                ('hire_date', models.DateField(verbose_name='入职日期')),
                ('role', models.CharField(choices=[('employee', '普通员工'), ('admin', '管理员')], default='employee', max_length=10, verbose_name='角色')),
                ('wechat_openid', models.CharField(blank=True, max_length=100, null=True, verbose_name='微信OpenID')),
                ('avatar_url', models.CharField(blank=True, max_length=500, null=True, verbose_name='头像URL')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否激活')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '员工',
                'verbose_name_plural': '员工',
                'db_table': 'employees',
            },
            bases=(models.Model, django.contrib.auth.models.AbstractBaseUser, django.contrib.auth.models.PermissionsMixin),
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(max_length=7, verbose_name='月份')),
                ('base_salary', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='基本工资')),
                ('performance_salary', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='绩效工资')),
                ('overtime_pay', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='加班费')),
                ('bonus', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='奖金')),
                ('allowance', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='补贴')),
                ('social_security', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='社保')),
                ('housing_fund', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='公积金')),
                ('income_tax', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='个税')),
                ('other_deduction', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='其他扣除')),
                ('total_income', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='总收入')),
                ('total_deduction', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='总扣除')),
                ('net_salary', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='实发工资')),
                ('pay_date', models.DateField(verbose_name='发放日期')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('employee', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='salaries', to='wxcloudrun.employee', verbose_name='员工')),
            ],
            options={
                'verbose_name': '工资单',
                'verbose_name_plural': '工资单',
                'db_table': 'salaries',
                'ordering': ['-period', '-pay_date'],
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='日期')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '公告',
                'verbose_name_plural': '公告',
                'db_table': 'notices',
                'ordering': ['-date', '-created_at'],
            },
        ),
    ]
