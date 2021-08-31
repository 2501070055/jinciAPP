import logging

from django import forms
from django.db import transaction

from comments.models import CommentOne, CommentTwo
from plates.models import Title
from users.models import User

logs = logging.getLogger('log')


class CommentOneForm(forms.Form):
    """
    一级评论
    """

    pid = forms.CharField(label='帖子ID',
                          required=True,
                          max_length=16,
                          error_messages={
                             'required': '帖子ID必须填写'
                          })

    content = forms.CharField(label='评论内容',
                              required=True,
                              max_length=512,
                              error_messages={
                                  'required': '评论内容不可为空'
                              })

    def clean_title_id(self):
        pid = self.cleaned_data['pid']
        if not Title.objects.filter(id=pid, status=1).exists():
            raise forms.ValidationError('该帖子不存在')
        return pid

    def clean(self):
        data = super().clean()
        logs.info(data)
        # 如果单个字段有错误，直接返回，不执行后面的验证
        if self.errors:
            return
        return data

    @transaction.atomic()
    def do_comment_to(self, request):
        """
        发送一级评论
        :param request:
        :return:
        """

        try:
            user = request.user

            data = self.cleaned_data
            title_id = data.get('pid', '')
            content = data.get('content', '')

            content_one = CommentOne(title_id=title_id, content=content, user=user)
            content_one.save()

            return True
        except Exception as e:
            logs.error(e)
            return None


class CommentTwoForm(forms.Form):
    """
    二级评论
    """

    comment_one = forms.CharField(label='一级评论ID',
                                  max_length=16,
                                  required=True,
                                  error_messages={
                                      'required': '一级评论ID必须填写'
                                  })
    user_to = forms.CharField(label='被评论人ID',
                              max_length=16,
                              required=True,
                              error_messages={
                                  'required': '被评论人ID请填写'
                              })
    content = forms.CharField(label='二级评论内容',
                              max_length=512,
                              required=True,
                              error_messages={
                                  'required': '二级评论内容'
                              })

    def clean_comment_one(self):
        comment_one = self.cleaned_data['comment_one']
        if not CommentOne.objects.filter(id=comment_one, status=1).exists():
            raise forms.ValidationError('一级评论不存在或者已经被删除')
        return comment_one

    def clean_user_to(self):
        user_to = self.cleaned_data['user_to']
        if not User.objects.filter(id=user_to, is_active=1).exists():
            raise forms.ValidationError('用户不存在或者已经注销')
        return user_to

    def clean(self):
        data = super().clean()
        logs.info(data)
        # 如果单个字段有错误，直接返回，不执行后面的验证
        if self.errors:
            return
        return data

    @transaction.atomic()
    def do_comment_two(self, request):
        """
        二级评论
        :param request:
        :return:
        """

        try:
            user = request.user

            data = self.cleaned_data
            comment_one_id = data.get('comment_one', '')
            user_to_id = data.get('user_to', '')
            content = data.get('content', '')

            comment_two = CommentTwo(user=user, comment_one_id=comment_one_id, user_to_id=user_to_id, content=content)
            comment_two.save()

            return True
        except Exception as e:
            logs.error(e)
            return None
