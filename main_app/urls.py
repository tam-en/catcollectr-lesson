from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.login_view, name="login"),
    url(r'^user/(\w+)/$', views.profile, name='profile'),
    url(r'^logout/$', views.logout_view, name="logout"),
	url(r'^$', views.index, name='index'),
    url(r'^([0-9]+)/$', views.show, name='show'),
    url(r'^post_url/$', views.post_cat, name="post_cat"),
    url(r'^like_cat/$', views.like_cat, name='like_cat')
]
