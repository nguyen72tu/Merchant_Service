from functools import wraps

def additional_filters(filter_kwargs):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(*args, **kwargs):
            queryset = view_func(*args, **kwargs)
            
            # Apply additional filters to the queryset based on filter_kwargs
            queryset = queryset.filter(**filter_kwargs)
            
            return queryset
        return _wrapped
    return decorator
