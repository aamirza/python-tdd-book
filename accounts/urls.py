from django.conf.urls import url

from accounts import views


urlpatterns = [
    url(r'^send_login_email$', view=views.send_login_email, name="send_login_email"),
    url(r'^login$', view=views.login, name="login")
]
