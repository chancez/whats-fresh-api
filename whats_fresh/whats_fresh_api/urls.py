from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^vendors/?$', 'whats_fresh_api.views.vendor.vendor_list', name='vendors-list'),
    url(r'^stories/(?P<id>\d+)/?$', 'whats_fresh_api.views.story.story_details', name='story-details'),
    url(r'^products/(?P<id>\d+)/?$', 'whats_fresh_api.views.product.product_details', name='product-details'),
    url(r'^products/vendors/(?P<id>\d+)/?$', 'whats_fresh_api.views.product_vendor.product_vendor_details', name='product-vendo-details'),
)

