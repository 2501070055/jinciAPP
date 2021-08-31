from django.db import models


class StatusChoices(models.IntegerChoices):
    """
    性别选择
    """

    valid = 1, '有效',
    invalid = 0, '删除'