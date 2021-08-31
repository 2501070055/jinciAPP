from utils.response import UnauthorizedJsonResponse


def check_login(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, *kwargs)
        else:
            # 获取用户当前访问的url，并传递给/user/login/
            # next = request.get_full_path()
            # red = HttpResponseRedirect('/user/login/?next=' + next)
            return UnauthorizedJsonResponse()
    return wrapper
