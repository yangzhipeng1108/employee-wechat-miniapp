from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    EmployeeViewSet, SalaryViewSet, 
    NoticeViewSet, AdminViewSet
)

# 创建路由器
router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'salaries', SalaryViewSet, basename='salary')
router.register(r'notices', NoticeViewSet, basename='notice')
router.register(r'admin', AdminViewSet, basename='admin')

urlpatterns = [
    # API路由
    path('api/', include(router.urls)),
    
    # JWT Token路由
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 健康检查
    path('health/', lambda request: {'status': 'OK', 'message': '服务器运行正常'}),
]
