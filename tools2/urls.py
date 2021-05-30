"""tools2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from accounts import views
from users import views as user_views
from home import views as home_views
from home.views import PostListView,PostCreateView,PostUpdateView,PostDeleteView,Rate,PostDetail,RequestToolView#,PostDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetail, name='post-detail'), #path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/rate', Rate, name='rate-post'),
    path('post/<int:pk>/requesttool', RequestToolView, name='request-post'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', home_views.about, name='about'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', user_views.profile, name='profile'),
    path('accounts/mytools/', user_views.mytools, name='mytools'),
    path('accounts/notifications/', user_views.NotificationView, name='mynotis'),
    path('accounts/sendnotifs/', user_views.SendNotiView, name='sendnotis'),
    path('accounts/replynotifs/', user_views.ReplyNotiView, name='replynotis'),
    path('accounts/rejectnotifs/<int:pk>/', user_views.RejectNotiView, name='reject-request'),
    path('accounts/acceptnotifs/<int:pk>/', user_views.AcceptNotiView, name='accept-request'),
    path('accounts/startcontract/<int:pk>/', user_views.StartContractView, name='start-contract'),
    path('accounts/contracthistory/', user_views.ContractHistory, name='contract-history'),
    path('accounts/contractsongoing/', user_views.ContractsOngoing, name='contracts-ongoing'),
    path('accounts/contractdetail/<int:pk>/', user_views.ContractDetail, name='contract-detail'),
    path('accounts/contractdetail/status1/<int:pk>/', user_views.Status1, name='status1'),
    path('accounts/contractdetail/status2/<int:pk>/', user_views.Status2, name='status2'),
    path('accounts/contractdetail/status3/<int:pk>/', user_views.Status3, name='status3'),
    path('accounts/contractdetail/status4/<int:pk>/', user_views.Status4, name='status4'),
    path('accounts/contractdetail/status5/<int:pk>/', user_views.Status5, name='status5'),
    path('accounts/contractdetail/status6/<int:pk>/', user_views.Status6, name='status6'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#     path('profile/', user_views.profile.as_view(template_name='templates/users/profile.html'), name='profile'),

    # path('accounts/readnotifs/', user_views.ReadNotiView, name='readnotis'),