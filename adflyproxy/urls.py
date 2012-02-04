from django.conf.urls.defaults import patterns

urlpatterns = patterns("adflyproxy.views"
    (r'^adfly/(?P<code>[A-Za-z0-9]{3,5})$', 'proxy'),
)
