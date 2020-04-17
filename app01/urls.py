from django.conf.urls import url,include

from app01.views import account
from app01.views import blog


urlpatterns = [
    # 方式一
    # url(r'^course/$', course.CourseView.as_view()),

    # url(r'^course/(?P<pk>\d+)/$', course.CourseView.as_view()),

    # 方式二
    # url(r'^course/$', course.CourseView.as_view({'get':'list'})),
    #
    # url(r'^course/(?P<pk>\d+)/$', course.CourseView.as_view({'get':'retrieve'})),
    #
    #
    # url(r'^test$', course.test),
    #
    # url(r'^auth/$', account.AuthView.as_view()),
    # url(r'^micro/$', course.MicroView.as_view()),
    url(r'^login/$', account.Account.as_view()),
    url(r'^blog/$', blog.BlogView.as_view()),


]
