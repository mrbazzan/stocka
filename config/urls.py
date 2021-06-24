"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.urls import path, include, re_path
# This is import the vue js
# form django.views.generic import TemplateView

urlpatterns = [
    # Included Djoser
    path('auth/', include('djoser.urls')),
    # Json web token
    path('auth/', include('djoser.urls.jwt')),
]

# View from Vue Js
# urlpatterns += [re_path(r'^.^*', TemplateView.as_view(template_name='index.html'))]