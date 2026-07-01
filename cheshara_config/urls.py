from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('ai.urls')),
    path('api/v1/', include('business.urls')),
    path('api/v1/', include('communications.urls')),
    path('api/v1/', include('core.urls')),
    path('api/v1/', include('crm.urls')),
    path('api/v1/', include('subscription.urls')),
]
