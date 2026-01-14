# 🚀 启动指南

## 前置要求

- Python 3.8 或更高版本
- MySQL 5.7 或更高版本
- pip 包管理器

## 快速启动步骤

### 1️⃣ 安装 Python 依赖

```bash
cd employee-wechat-miniapp/wxcloudrun-django-main

# 创建虚拟环境（如果还没有）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安装依赖包
pip install -r requirements.txt
```

### 2️⃣ 配置数据库

#### 方式一：使用环境变量（推荐）

**Windows PowerShell:**
```powershell
$env:MYSQL_ADDRESS="localhost:3306"
$env:MYSQL_DATABASE="employee_management"
$env:MYSQL_USERNAME="root"
$env:MYSQL_PASSWORD="your_password"
$env:MYSQL_HOST="localhost"
$env:MYSQL_PORT="3306"
```

**Windows CMD:**
```cmd
set MYSQL_ADDRESS=localhost:3306
set MYSQL_DATABASE=employee_management
set MYSQL_USERNAME=root
set MYSQL_PASSWORD=your_password
set MYSQL_HOST=localhost
set MYSQL_PORT=3306
```

**Mac/Linux:**
```bash
export MYSQL_ADDRESS=localhost:3306
export MYSQL_DATABASE=employee_management
export MYSQL_USERNAME=root
export MYSQL_PASSWORD=your_password
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
```

#### 方式二：修改配置文件

编辑 `wxcloudrun/settings.py`，找到 `DATABASES` 部分：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'employee_management',      # 数据库名称
        'USER': 'root',                     # 用户名
        'PASSWORD': 'your_password',        # 密码
        'HOST': 'localhost',                # 主机
        'PORT': '3306',                     # 端口
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

### 3️⃣ 创建数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE IF NOT EXISTS employee_management 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;
```

### 4️⃣ 执行数据库迁移

```bash
# 生成迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate
```

### 5️⃣ 创建管理员账号

```bash
# 使用默认配置
python create_admin.py

# 或者自定义管理员信息
$env:ADMIN_CODE="admin"
$env:ADMIN_PASSWORD="admin123"
python create_admin.py
```

默认管理员账号：
- 工号：`admin`
- 密码：`admin123`

### 6️⃣ 启动开发服务器

```bash
python manage.py runserver
```

服务器将在 `http://localhost:8000` 启动

## 测试 API

### 1. 健康检查
```bash
curl http://localhost:8000/health/
```

预期响应：
```json
{
  "status": "OK",
  "message": "服务器运行正常"
}
```

### 2. 登录获取 Token
```bash
curl -X POST http://localhost:8000/api/employees/login/ `
  -H "Content-Type: application/json" `
  -d '{"employee_code": "admin", "password": "admin123"}'
```

预期响应：
```json
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

### 3. 获取员工列表（需要 Token）
```bash
# 替换 YOUR_TOKEN 为上面返回的 token
curl http://localhost:8000/api/employees/ `
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 常见问题

### ❌ 数据库连接失败

**错误信息：**
```
django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")
```

**解决方案：**
1. 确认 MySQL 服务是否运行
2. 检查数据库连接信息是否正确
3. 检查防火墙设置

```bash
# Windows 检查 MySQL 服务
sc query mysql

# 启动 MySQL 服务
net start mysql

# 检查 MySQL 是否在运行
mysql -u root -p
```

### ❌ 数据库不存在

**错误信息：**
```
django.db.utils.OperationalError: (1049, "Unknown database 'employee_management'")
```

**解决方案：**
```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE IF NOT EXISTS employee_management 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;

# 退出
EXIT;
```

### ❌ 权限错误

**错误信息：**
```
django.db.utils.OperationalError: (1045, "Access denied for user")
```

**解决方案：**
检查数据库用户名和密码是否正确，确保用户有访问数据库的权限。

### ❌ 端口已被占用

**错误信息：**
```
Error: That port is already in use.
```

**解决方案：**
```bash
# 使用其他端口
python manage.py runserver 8080

# 或者关闭占用 8000 端口的程序
# Windows
netstat -ano | findstr :8000
taskkill /PID <进程ID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### ❌ 依赖包未安装

**错误信息：**
```
ModuleNotFoundError: No module named '...'
```

**解决方案：**
```bash
# 重新安装依赖
pip install -r requirements.txt --force-reinstall

# 或升级 pip
pip install --upgrade pip
```

## 开发工具

### 使用 Django Shell

```bash
python manage.py shell
```

示例操作：
```python
from wxcloudrun.models import Employee

# 创建新员工
employee = Employee(
    employee_code='E001',
    name='张三',
    department='技术部',
    position='开发工程师'
)
employee.set_password('password123')
employee.save()

# 查询员工
employees = Employee.objects.all()
print(employees)
```

### 查看 SQL 日志

在 `settings.py` 中添加：
```python
LOGGING = {
    # ... 其他配置 ...
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 生产部署

### 云托管部署

1. 登录微信云托管控制台
2. 创建新服务
3. 配置环境变量：
   ```
   MYSQL_ADDRESS=mysql-instance:3306
   MYSQL_DATABASE=employee_management
   MYSQL_USERNAME=root
   MYSQL_PASSWORD=your_password
   JWT_SECRET=your-jwt-secret
   ADMIN_CODE=admin
   ADMIN_PASSWORD=admin123
   ```
4. 上传代码
5. 部署服务

### Docker 部署

```bash
# 构建镜像
docker build -t employee-management .

# 运行容器
docker run -d -p 8000:80 \
  -e MYSQL_ADDRESS=host.docker.internal:3306 \
  -e MYSQL_DATABASE=employee_management \
  -e MYSQL_USERNAME=root \
  -e MYSQL_PASSWORD=your_password \
  employee-management
```

## 项目结构

```
wxcloudrun-django-main/
├── wxcloudrun/              # Django 应用
│   ├── models.py           # 数据模型
│   ├── serializers.py      # 序列化器
│   ├── views.py            # API 视图
│   ├── urls.py             # URL 路由
│   └── settings.py         # Django 配置
├── manage.py               # Django 管理命令
├── create_admin.py        # 创建管理员脚本
├── requirements.txt       # Python 依赖
├── Dockerfile            # Docker 配置
└── README.md             # 项目文档
```

## 下一步

启动成功后，您可以：

1. 📖 阅读 [README.md](README.md) 了解项目功能
2. 📚 查看 [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) 获取详细开发指南
3. 📊 测试各种 API 接口
4. 🎨 开发微信小程序前端
5. 🚀 部署到生产环境

## 获取帮助

如果遇到问题：

1. 查看日志文件：`logs/` 目录
2. 检查错误信息
3. 参考常见问题部分
4. 查阅 Django 官方文档
5. 查阅微信云开发文档

---

**祝您开发愉快！** 🎉
