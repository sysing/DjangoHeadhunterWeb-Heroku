from django.urls import path, include, re_path
from . import views
from django.shortcuts import render_to_response
from django.contrib.auth import views as auth_views
from rest_framework import routers
from .forms import LoginForm

# router = routers.DefaultRouter()
# router.register('recruiters',views.RecruiterView)

urlpatterns = [
    path('', views.index, name='index'),

    #user forms
    path('login/',views.login, name = 'login'),
    path('logout/',auth_views.logout, {'next_page': '/'}, name='logout'),
    path('signup/',views.signup,name='signup'),
    path('update_profile/', views.update_profile, name='update_profile'),

    #job apply
    re_path(r'candidate_create_job/(?P<pk>\d+)/', views.candidate_create_job, name='candidate_create_job'),
    re_path(r'candidate_select_job/(?P<pk>\d+)/', views.candidate_select_job, name='candidate_select_job'),

    re_path(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    re_path(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # path('rest/', include(router.urls)),
    # path('rest-auth/', include('rest_framework.urls')),
    re_path(r'^language/(?P<language>[a-z\-]+)/$',views.language,name="language"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),

    path('dashboard',views.dashboard, name ='dashboard'),
    path('active_users',views.active_users_json, name = "active_users_json"),
    path('new_candidates',views.new_candidates_json, name = "new_candidates_json"),
    path('top_candidates',views.top_candidates_json, name = "top_candidates_json"),
    path('top_functions',views.top_functions_json, name = "top_functions_json"),
    path('line_chart_json',views.line_chart_json, name = "line_chart_json"),
]
