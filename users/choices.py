from django.db import models


class SexChoices(models.IntegerChoices):
    """
    性别选择
    """

    boy = 1, '男',
    girl = 0, '女'


class StatusChoices(models.IntegerChoices):
    """
    用户登录状态
    """

    online = 0, '在线',
    invisibility = 1, '隐身',


class FollowChoices(models.IntegerChoices):
    """
    关注状态
    """

    follow = 1, '关注',
    un_follow = 0, '未关注',
