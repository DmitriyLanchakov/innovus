# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('admin.views',
    url(
        regex = '^update_category_order/$',
        view  = 'update_category_order',
        name  =  'update-category-order',
    ),
    url(
        regex = '^post/(?P<post_id>\d+)/category/add/$',
        view  = 'add_category',
        name  = 'add-category',
    ),
    url(
        regex = '^post/category/add/$',
        view  = 'add_category',
        name  = 'add-category',
    ),
    # ------
    url(
        regex = '^post_save/$',
        view  = 'post_save',
        name  = 'post-save',
    ),
)

