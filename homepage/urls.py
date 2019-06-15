from django.conf.urls import url, include
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from homepage import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'gwajams'
urlpatterns = [
    url(r'^auth/$', views.AuthList.as_view()),
    url(r'^users/$', views.user_list),
    url(r'^users/(?P<username>\w+)/$', views.user_detail),
    
    url(r'^profile/$',views.profile_list),
    
    path('groups/<int:group_id>/admin/', views.update_group, name='group_admin'),
    path('groups/<int:group_id>/members/<int:user_id>/', views.update_member, name='update_member'),
    path('groups/<int:group_id>/members/', views.member_list, name='member_list'),
    path('groups/<int:group_id>/drop/', views.drop_group, name='group_withdraw'),
    path('groups/<int:group_id>/post/<int:design_id>/', views.post_design, name='post_design'),
    path('groups/edit/<int:design_id>/', views.edit_design, name='edit_design'),
    path('groups/like/<int:design_id>/', views.update_likes, name='update_likes'),
    path('groups/unlike/<int:design_id>/', views.undo_likes, name='undo_likes'),
    path('groups/delete/<int:design_id>/', views.delete_design, name='delete_design'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    url(r'^groups/(?P<username>\w+)/$',views.group_list, name='group_list'),
    path('groups/', views.group_list_all, name='group_list_all'),
    path('create_group/', views.create_group, name='create_group'),
    path('join_group/<int:group_id>/', views.join_group, name='join_group'),
    path('', views.main, name='main'),
    # url(r'login/', views.login.as_view(), name='login'),
    # url(r'logout/', views.logout.as_view(), name='logout'),
    # url(r'join/', views.join.as_view(), name='join'),
    # url(r'mypage/', views.mypage.as_view(), name='mypage'),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
