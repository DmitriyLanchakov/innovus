from datetime import datetime
from django.utils.functional import wraps
from django.shortcuts import redirect

def works_in(start_date, end_date):
    """decorator that limits working period of the view"""
    def renderer(view):

        @wraps(view)
        def wrapper(request, *args, **kw):
            if start_date < datetime.now() < end_date or request.user.is_staff:
                return view(request, *args, **kw)
            else:
                return redirect('/finished/')

        return wrapper

    return renderer
