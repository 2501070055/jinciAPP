from django.http import JsonResponse


class NotFoundJsonResponse(JsonResponse):
    """
    404 对应Json相应
    """

    status_code = 404

    def __init__(self, *args, **kwargs):

        data = {
            "error_code": '404',
            "error_msg": "您访问的内容不存在或被删除。"
        }
        super().__init__(data, *args, **kwargs)


class BadRequestJsonResponse(JsonResponse):
    """
    表单请求参数错误
     """

    status_code = 400

    def __init__(self, err_list=[], *args, **kwargs):
        data = {
            "error_code": '400',
            "error_msg": "参数格式不正确",
            "err_list": err_list
        }
        super().__init__(data, *args, **kwargs)


class MethodNotAllowedJsonResponse(JsonResponse):
    """
     表单请求方式错误
     """

    status_code = 405

    def __init__(self, *args, **kwargs):
        data = {
            "error_code": '4050000',
            "error_msg": "表单请求方式错误",
        }
        super().__init__(data, *args, **kwargs)


class UnauthorizedJsonResponse(JsonResponse):
    """
    请登录
    """

    status_code = 401

    def __init__(self, *args, **kwargs):
        data = {
            "error_code": '401',
            "error_msg": "请登录",
        }
        super().__init__(data, *args, **kwargs)


class ServerErrorJsonResponse(JsonResponse):
    """
    服务器没有相应
    """

    status_code = 500

    def __init__(self, *args, **kwargs):
        data = {
            "error_code": '500',
            "error_msg": "服务器正忙，请稍后重试",
        }
        super().__init__(data, *args, **kwargs)
