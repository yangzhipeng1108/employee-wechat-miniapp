#!/bin/sh
set -e

echo "Starting Django application..."

# 执行数据库迁移
echo "Running database migrations..."
python3 manage.py migrate --noinput || true

# 创建默认管理员账号
echo "Creating default admin account..."
python3 create_admin.py || echo "Admin creation skipped"

# 启动Django服务器
echo "Starting Django server on 0.0.0.0:80..."
exec python3 manage.py runserver 0.0.0.0:80