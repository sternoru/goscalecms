from django.conf.urls import patterns, url
from django.conf import settings
import views

urlpatterns = patterns('',
    url(r'^utils/form/$', views.form, name="goscale_form_handler"),
)

if 'allauth.account' in settings.INSTALLED_APPS:
    try:
        from allauth.account.views import signup
        urlpatterns += patterns('',
            url(r'^signup/$', signup, name='goscale_account_signup',
                kwargs={'template_name': 'user/signup.html'}
            )
        )
    except ImportError:
        # allauth is not properly installed
        pass
