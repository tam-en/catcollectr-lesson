from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	# add the line below to your urlpatterns array
	url(r'^', include('main_app.urls'))
]
