from django.conf.urls import include, url
from doctores import views as list_views
from doctores import urls as list_urls

urlpatterns = [
    url(r'^$', list_views.home_page, name='home'),
    url(r'^doctores/', include(list_urls)),
    # url(r'^admin/', include(admin.site.urls)),
]
