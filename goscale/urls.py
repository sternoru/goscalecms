from django.conf.urls import patterns
import views

urlpatterns = patterns('',
    (r'^utils/form/$', views.form),
)
