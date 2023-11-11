"""_config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [

    # System/Root Application
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('home/')),
    
    # General Purpose Application
    path('home/', include('home.urls')),
    path('common/', include('common.urls')),

    # User Purpose Application
    path('medass/', include('medass.urls'))
]

from django.conf import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'common.views.error400'
handler403 = 'common.views.error403'
handler404 = 'common.views.error404'
handler500 = 'common.views.error500'
handler502 = 'common.views.error502'
handler503 = 'common.views.error503'