"""
URL configuration for demoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from demo.views import MainPageView, EmbedWebsiteView
from demo import views
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('demo/', include('demo.urls')),  # Include URLs from the demo app
    path('home/', MainPageView.as_view(), name='index'),  # Use MainPageView for the '/home/' URL
      path('embed-website/', EmbedWebsiteView.as_view(), name='embed_website'),

    path('chatbot/process/', views.process_chat_message, name='process_chat_message'),
              path('chatbot/process/', views.process_chat_message, name='process_chat_message'),



]
