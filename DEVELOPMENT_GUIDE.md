# 员工管理系统 - 开发指南

## 🚀 快速开始

### 前置要求
- Python 3.8+
- MySQL 5.7+
- pip

### 本地开发步骤

#### 1. 创建虚拟环境
```bash
cd employee-wechat-miniapp/wxcloudrun-django-main
python -m venv venv

# Windows 激活虚拟环境
venv\Scripts\activate

# Mac/Linux 激活虚拟环境
source venv/bin/activate
```

#### 2. 安装依赖
```bash
pip install -r requirements.txt
```

#### 3. 配置数据库

**方式一：使用环境变量（推荐）**
```bash
# Windows (PowerShell)
$env:MYSQL_DATABASE="employee_management"
$env:MYSQL_USERNAME="root"
$env:MYSQL_PASSWORD="your_password"
$env:MYSQL_HOST="localhost"
$env:MYSQL_PORT="3306"

# Windows (CMD)
set MYSQL_DATABASE=employee_management
set MYSQL_USERNAME=root
set MYSQL_PASSWORD=your_password
set MYSQL_HOST=localhost
set MYSQL_PORT=3306

# Mac/Linux
export MYSQL_DATABASE=employee_management
export MYSQL_USERNAME=root
export MYSQL_PASSWORD=your_password
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
```

**方式二：修改配置文件**
编辑 `wxcloudrun/settings.py` 中的 `DATABASES` 配置。

#### 4. 初始化数据库
```bash
# 创建数据库表
python manage.py migrate

# 创建超级用户
python create_admin.py
```

默认管理员账号：
- 工号：`admin`
- 密码：`admin123`

可以通过环境变量自定义：
```bash
$env:ADMIN_CODE="admin"
$env:ADMIN_PASSWORD="admin123"
python create_admin.py
```

#### 5. 启动开发服务器
```bash
python manage.py runserver
```

服务将在 `http://localhost:8000` 启动

## 📡 API测试

### 健康检查
```bash
curl http://localhost:8000/health/
```

### 登录获取Token
```bash
curl -X POST http://localhost:8000/api/employees/login/ `
  -H "Content-Type: application/json" `
  -d '{"employee_code": "admin", "password": "admin123"}'
```

### 获取员工列表（需要Token）
```bash
curl http://localhost:8000/api/employees/ `
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🗂️ 项目结构

```
wxcloudrun-django-main/
├── wxcloudrun/                    # Django应用
│   ├── __init__.py
│   ├── apps.py                   # 应用配置
│   ├── models.py                 # 数据模型
│   ├── serializers.py            # 序列化器
│   ├── views.py                  # API视图
│   ├── urls.py                   # URL路由
│   ├── settings.py               # Django设置
│   ├── wsgi.py                   # WSGI配置
│   └── migrations/               # 数据库迁移文件
├── manage.py                     # Django管理命令
├── create_admin.py              # 创建管理员脚本
├── Dockerfile                    # Docker配置
├── docker-entrypoint.sh          # 容器启动脚本
├── requirements.txt             # Python依赖
└── README.md                    # 项目文档
```

## 🔧 开发配置

### 数据库配置
系统支持通过环境变量配置数据库连接：

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| MYSQL_ADDRESS | 数据库地址 | - |
| MYSQL_DATABASE | 数据库名称 | employee_management |
| MYSQL_USERNAME | 数据库用户名 | root |
| MYSQL_PASSWORD | 数据库密码 | - |
| MYSQL_HOST | 数据库主机 | - |
| MYSQL_PORT | 数据库端口 | 3306 |

### JWT配置
| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| JWT_SECRET | JWT密钥 | 使用SECRET_KEY |
| ACCESS_TOKEN_LIFETIME | 访问令牌有效期 | 7天 |
| REFRESH_TOKEN_LIFETIME | 刷新令牌有效期 | 30天 |

### 管理员配置
| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| ADMIN_CODE | 管理员工号 | admin |
| ADMIN_PASSWORD | 管理员密码 | admin123 |

## 📊 数据库表结构

### employees（员工表）
- `id` - 主键
- `employee_code` - 工号（唯一）
- `name` - 姓名
- `password` - 密码（bcrypt加密）
- `department` - 部门
- `position` - 职位
- `phone` - 联系电话
- `email` - 邮箱
- `hire_date` - 入职日期
- `role` - 角色（employee/admin）
- `wechat_openid` - 微信OpenID
- `avatar_url` - 头像URL
- `created_at` - 创建时间
- `updated_at` - 更新时间

### salaries（工资单表）
- `id` - 主键
- `employee_id` - 员工ID（外键）
- `period` - 月份（如：2024-01）
- `base_salary` - 基本工资
- `performance_salary` - 绩效工资
- `overtime_pay` - 加班费
- `bonus` - 奖金
- `allowance` - 补贴
- `social_security` - 社保
- `housing_fund` - 公积金
- `income_tax` - 个税
- `other_deduction` - 其他扣除
- `total_income` - 总收入
- `total_deduction` - 总扣除
- `net_salary` - 实发工资
- `pay_date` - 发放日期
- `created_at` - 创建时间

### notices（公告表）
- `id` - 主键
- `title` - 标题
- `content` - 内容
- `date` - 日期
- `created_at` - 创建时间

## 🛡️ 安全设置

### 生产环境配置
在生产环境中，需要修改以下安全配置：

```python
# wxcloudrun/settings.py

# 修改密钥
SECRET_KEY = 'your-random-secret-key'

# 关闭调试模式
DEBUG = False

# 配置允许的主机
ALLOWED_HOSTS = ['yourdomain.com', 'api.yourdomain.com']

# 设置强密码
JWT_SECRET_KEY = 'your-strong-jwt-secret-key'
```

### 密码安全
- 所有密码使用 bcrypt 加密存储
- 密码字段设置为 write_only，不会在序列化中返回

### API认证
- 所有API（除登录）都需要JWT Token认证
- Token有效期为7天
- 支持使用refresh_token刷新token

## 📝 常用命令

### Django管理命令
```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver

# 进入Python shell
python manage.py shell

# 清空数据库（慎用）
python manage.py flush
```

### 数据库操作
```bash
# 查看SQL
python manage.py sqlmigrate wxcloudrun 0001

# 检查数据库问题
python manage.py check

# 创建数据库备份
mysqldump -u root -p employee_management > backup.sql

# 恢复数据库
mysql -u root -p employee_management < backup.sql
```

## 🐛 调试技巧

### 查看日志
日志文件位于 `logs/` 目录：
- `all-YYYY-MM-DD.log` - 所有日志
- `info-YYYY-MM-DD.log` - 信息日志
- `error-YYYY-MM-DD.log` - 错误日志

### Django调试
```python
# 在代码中使用Python调试器
import pdb; pdb.set_trace()

# 或使用ipdb
import ipdb; ipdb.set_trace()
```

### API调试
```bash
# 查看响应头
curl -i http://localhost:8000/api/employees/

# 查看详细信息
curl -v http://localhost:8000/api/employees/

# 保存响应到文件
curl http://localhost:8000/api/employees/ > response.json
```

## 🔍 故障排查

### 问题1：数据库连接失败
**解决方案：**
1. 检查MySQL服务是否运行
2. 确认数据库连接信息是否正确
3. 检查防火墙设置

### 问题2：迁移失败
**解决方案：**
```bash
# 删除迁移文件（保留__init__.py）
rm wxcloudrun/migrations/0*.py

# 重新生成迁移
python manage.py makemigrations

# 执行迁移
python manage.py migrate
```

### 问题3：端口已被占用
**解决方案：**
```bash
# 使用其他端口
python manage.py runserver 8080
```

### 问题4：依赖包冲突
**解决方案：**
```bash
# 升级pip
pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

## 📚 参考资料

- [Django官方文档](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [微信云开发文档](https://cloud.tencent.com/document/product)
- [wxcloudrun-django](https://github.com/WeixinCloud/wxcloudrun-django)

---

**开发者指南版本**: 1.0.0
**更新时间**: 2024-01-14
