"""Custom Decorators"""
from django.http import HttpResponseBadRequest

def ajax_required(f):
    """Getting required function"""
    def wrap(request, *args, **kwargs):
        """Internal"""
        if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
            return HttpResponseBadRequest()
        return f(request,*args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__=f.__name__
    return wrap
