from django.conf.urls import patterns, url
from django.conf import settings
import views

urlpatterns = patterns('',
    url(r'^utils/form/$', views.form, name="goscale_form_handler"),
)

if 'allauth.account' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^signup/$', views.signup, name='goscale_account_signup',
            kwargs={'template_name': 'user/signup.html'}
        )
    )
