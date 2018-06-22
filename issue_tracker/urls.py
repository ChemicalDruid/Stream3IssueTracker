"""issue_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from home import views as home_views
from accounts import views as accounts_views
from ua_bugs import views as uabugs_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_views.get_index, name='index'),
    url(r'^register/$', accounts_views.register, name='register'),
    url(r'^profile/$', accounts_views.profile, name='profile'),
    url(r'^login/$', accounts_views.login, name='login'),
    url(r'^logout/$', accounts_views.logout, name='logout'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^uabugs/$', uabugs_views.uabugs, name='uabugs'),
    url(r'^bugs/(?P<subject_id>\d+)/$', uabugs_views.bugs, name='bugs'),
    url(r'^new_bug/(?P<subject_id>\d+)/$', uabugs_views.new_bug, name='new_bug'),
    url(r'^bug/(?P<bug_id>\d+)/$', uabugs_views.bug, name='bug'),
    url(r'^post/new/(?P<bug_id>\d+)/$', uabugs_views.new_post, name='new_post'),
    url(r'^post/edit/(?P<bug_id>\d+)/(?P<post_id>\d+)/$', uabugs_views.edit_post, name='edit_post'),
    url(r'^post/delete/(?P<bug_id>\d+)/(?P<post_id>\d+)/$', uabugs_views.delete_post, name='delete_post'),
    url(r'^bug/vote/(?P<bug_id>\d+)/(?P<subject_id>\d+)/$', uabugs_views.bug_vote, name='cast_vote'),
]
