# 员工管理系统 - Django后端

基于微信官方 [wxcloudrun-django](https://github.com/WeixinCloud/wxcloudrun-django) 模板开发的员工管理系统后端。

## 功能特性

### 员工端功能
- ✅ 工号密码登录
- ✅ 微信一键登录
- ✅ 查看个人信息
- ✅ 绑定微信号
- ✅ 查看工资单（按月份筛选）
- ✅ 查看统计数据

### 管理端功能
- ✅ 添加员工信息
- ✅ 生成员工工资单
- ✅ 查看全局统计数据
- ✅ 员工列表管理

## 技术栈

- **后端框架**: Django 3.2.8
- **API框架**: Django REST Framework 3.12.4
- **数据库**: MySQL (云开发MySQL)
- **认证**: JWT (djangorestframework-simplejwt)
- **部署**: 微信云托管 / Docker

## 项目结构

```
wxcloudrun-django-main/
├── Dockerfile                  # Docker配置文件
├── docker-entrypoint.sh        # 容器启动脚本
├── create_admin.py            # 创建管理员账号脚本
├── manage.py                  # Django管理命令
├── requirements.txt           # Python依赖包
├── README.md                  # 项目说明文档
├── container.config.json      # 云托管配置
├── wxcloudrun/                # Django应用目录
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py              # 数据模型
│   ├── serializers.py         # 序列化器
│   ├── views.py               # 视图函数
│   ├── urls.py                # URL路由
│   ├── settings.py            # Django配置
│   ├── wsgi.py                # WSGI配置
│   └── migrations/            # 数据库迁移文件
└── .gitignore
```

## 快速开始

### 前置要求

- Python 3.8+
- MySQL 5.7+ (云开发MySQL会自动配置)
- 微信云托管账号

### 本地开发

#### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 2. 配置数据库

编辑 `wxcloudrun/settings.py`，设置数据库连接：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'employee_management',  # 数据库名称
        'USER': 'root',                   # 用户名
        'HOST': 'localhost',              # 主机
        'PORT': '3306',                   # 端口
        'PASSWORD': 'your_password',      # 密码
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

#### 3. 执行数据库迁移

```bash
# 创建数据库表
python manage.py migrate

# 创建默认管理员账号
python create_admin.py
```

默认管理员账号：
- 工号: `admin`
- 密码: `admin123`

可以通过环境变量自定义：
```bash
export ADMIN_CODE=admin
export ADMIN_PASSWORD=admin123
python create_admin.py
```

#### 4. 启动开发服务器

```bash
python manage.py runserver
```

服务将在 `http://localhost:8000` 启动

#### 5. 测试API

```bash
# 健康检查
curl http://localhost:8000/health/

# 登录
curl -X POST http://localhost:8000/api/employees/login/ \
  -H "Content-Type: application/json" \
  -d '{"employee_code": "admin", "password": "admin123"}'
```

## 云托管部署

### 方式一：使用微信云托管模板

1. 登录[微信云托管控制台](https://console.cloud.tencent.com/tcb)
2. 点击"新建服务"
3. 选择"从模板创建"
4. 选择 "wxcloudrun-django" 模板
5. 按照引导完成配置

### 方式二：手动部署

#### 1. 修改container.config.json

```json
{
  "dataBaseName":"employee_management",
  "executeSQLs":[
    "CREATE DATABASE IF NOT EXISTS employee_management;",
    "USE employee_management;"
  ]
}
```

#### 2. 配置环境变量

在云托管控制台配置以下环境变量：

```
MYSQL_ADDRESS=mysql-instance:3306
MYSQL_USERNAME=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=employee_management
JWT_SECRET=your-secret-key-change-in-production
ADMIN_CODE=admin
ADMIN_PASSWORD=admin123
```

#### 3. 上传代码

可以使用Git上传代码到仓库，然后在云托管控制台选择代码仓库进行部署。

#### 4. 部署服务

按照云托管控制台的指引完成服务部署。

## API接口文档

### 认证接口

#### 登录
```
POST /api/employees/login/
Content-Type: application/json

{
  "employee_code": "admin",
  "password": "admin123"
}

响应:
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbG...",
  "employee": {
    "id": 1,
    "employee_code": "admin",
    "name": "管理员",
    ...
  }
}
```

#### 微信登录
```
POST /api/employees/wechat_login/
Content-Type: application/json

{
  "code": "wx_login_code",
  "userInfo": {
    "nickName": "用户昵称",
    "avatarUrl": "头像地址"
  }
}
```

### 员工接口

#### 获取员工信息
```
GET /api/employees/:id/
Authorization: Bearer {token}
```

#### 绑定微信
```
POST /api/employees/bind_wechat/
Authorization: Bearer {token}
Content-Type: application/json

{
  "code": "wx_code",
  "userInfo": {...}
}
```

#### 获取员工统计
```
GET /api/employees/stats/
Authorization: Bearer {token}

响应:
{
  "success": true,
  "totalSalary": 8000
}
```

### 工资单接口

#### 获取工资单
```
GET /api/salaries/?employeeId=1&period=2024-01
Authorization: Bearer {token}
```

#### 生成工资单（管理员）
```
POST /api/salaries/
Authorization: Bearer {token}
Content-Type: application/json

{
  "employeeId": 1,
  "period": "2024-01",
  "baseSalary": 5000,
  "performanceSalary": 2000,
  "overtimePay": 500,
  "bonus": 1000,
  "allowance": 300,
  "socialSecurity": 400,
  "housingFund": 400,
  "incomeTax": 200,
  "otherDeduction": 0,
  "payDate": "2024-01-15"
}
```

### 公告接口

#### 获取公告列表
```
GET /api/notices/
```

### 管理员接口

#### 获取全局统计
```
GET /api/admin/stats/
Authorization: Bearer {token}

响应:
{
  "success": true,
  "stats": {
    "totalEmployees": 10,
    "totalSalary": 80000
  }
}
```

#### 添加员工
```
POST /api/admin/employees/
Authorization: Bearer {token}
Content-Type: application/json

{
  "employee_code": "E001",
  "name": "张三",
  "password": "password123",
  "department": "技术部",
  "position": "开发工程师",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "hire_date": "2024-01-01"
}
```

## 数据库说明

### 数据表

**employees（员工表）**
```sql
- id: 主键
- employee_code: 工号（唯一）
- name: 姓名
- password: 密码（bcrypt加密）
- department: 部门
- position: 职位
- phone: 联系电话
- email: 邮箱
- hire_date: 入职日期
- role: 角色（employee/admin）
- wechat_openid: 微信OpenID
- avatar_url: 头像URL
- created_at: 创建时间
- updated_at: 更新时间
```

**salaries（工资单表）**
```sql
- id: 主键
- employee_id: 员工ID（外键）
- period: 月份（如：2024-01）
- base_salary: 基本工资
- performance_salary: 绩效工资
- overtime_pay: 加班费
- bonus: 奖金
- allowance: 补贴
- social_security: 社保
- housing_fund: 公积金
- income_tax: 个税
- other_deduction: 其他扣除
- total_income: 总收入
- total_deduction: 总扣除
- net_salary: 实发工资
- pay_date: 发放日期
- created_at: 创建时间
```

**notices（公告表）**
```sql
- id: 主键
- title: 标题
- content: 内容
- date: 日期
- created_at: 创建时间
```

## 安全注意事项

1. **生产环境配置**
   - 修改 `SECRET_KEY` 为随机密钥
   - 修改 `JWT_SECRET` 为强密码
   - 设置 `DEBUG = False`
   - 配置正确的 `ALLOWED_HOSTS`

2. **密码安全**
   - 使用bcrypt加密存储密码
   - 密码字段设置为 `write_only`

3. **API认证**
   - 所有API都需要JWT认证（除登录和公开接口）
   - Token有效期为7天
   - 支持Token刷新

4. **权限控制**
   - 管理员接口只允许role='admin'的用户访问
   - 普通用户只能访问自己的数据

## 开发建议

1. **代码风格**
   - 遵循PEP 8规范
   - 使用类型注解
   - 添加文档字符串

2. **错误处理**
   - 使用Django REST Framework的异常处理
   - 返回统一的错误格式

3. **日志记录**
   - 使用Django logging系统
   - 记录关键操作和错误

4. **测试**
   - 编写单元测试
   - 编写API测试

## 常见问题

### Q1: 数据库连接失败？

**解决方案：**
1. 检查数据库配置是否正确
2. 确认数据库服务是否运行
3. 检查网络连接

### Q2: 迁移失败？

**解决方案：**
```bash
# 删除迁移文件（保留__init__.py）
rm wxcloudrun/migrations/0*.py

# 重新生成迁移
python manage.py makemigrations

# 执行迁移
python manage.py migrate
```

### Q3: 管理员账号创建失败？

**解决方案：**
```bash
# 手动创建超级用户
python manage.py createsuperuser

# 或使用create_admin.py脚本
python create_admin.py
```

### Q4: JWT Token过期？

**解决方案：**
使用refresh_token刷新token：
```
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "refresh_token_value"
}
```

## 参考资源

- [微信云开发文档](https://cloud.tencent.com/document/product)
- [wxcloudrun-django GitHub](https://github.com/WeixinCloud/wxcloudrun-django)
- [Django官方文档](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## 许可证

MIT License

## 联系方式

如有问题或建议，请在项目中提交Issue。
