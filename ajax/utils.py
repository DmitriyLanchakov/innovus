# -*- coding: utf-8 -*-

def get_int_safe(request, key, default=0):
    """
    Get int parameter from GET request
    """
    try:
        integer = int(request.GET.get(key, default))
    except:
        integer = default
    return integer