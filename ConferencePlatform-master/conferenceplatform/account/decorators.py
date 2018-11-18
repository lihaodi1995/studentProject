from django.http.response import JsonResponse

def user_has_permission(permission):
    def decorator(func):
        def wrapper(request, *args, **kw):
            data = {'message':'', 'data':{}}
            if request.user.is_authenticated:
                if request.user.has_perm(permission) is False:
                    data['message'] = 'permission error'
                    return JsonResponse(data)
                else:
                    return func(request, *args, **kw)
            else:
                data['message'] = 'anonymous user'
                return JsonResponse(data)
        return wrapper
    return decorator
    