import logging

from django import forms
from django.db import transaction

from emaillist.models import OpenEmail, EmailGo
from users.models import User

logs = logging.getLogger('log')


class SendOpenEmailForm(forms.Form):
    """
    发送公共邮件
    """

    title = forms.CharField(label='邮件名称',
                            required=True,
                            max_length=16,
                            error_messages={
                                'required': '邮件名称必须填写'
                            })
    content = forms.CharField(label='邮件内容',
                              required=True,
                              max_length=16,
                              error_messages={
                                  'required': '邮件内容必须填写'
                              })
    audio = forms.CharField(label='录音url',
                            required=False,
                            max_length=128)

    def clean(self):
        data = super().clean()
        logs.info(data)
        # 如果单个字段有错误，直接返回，不执行后面的验证
        if self.errors:
            return
        return data

    @transaction.atomic()
    def do_send_open_email(self, request):
        """
        发送公共邮件
        :param request:
        :return:
        """

        try:
            user = request.user

            data = self.cleaned_data
            title = data.get('title', '')
            content = data.get('content', '')
            audio = data.get('audio', '')

            open_email = OpenEmail(user=user, title=title, content=content, audio=audio)
            open_email.save()

            return True
        except Exception as e:
            logs.error(e)
            return None


class SendEmailGoForm(forms.Form):
    """
    发送私人邮件
    """

    to_user = forms.CharField(label='邮件收件人ID',
                              required=True,
                              max_length=16,
                              error_messages={
                                  'required': '邮件收件人ID必须填写'
                              })
    title = forms.CharField(label='邮件名称',
                            required=True,
                            max_length=16,
                            error_messages={
                                'required': '邮件名称必须填写'
                            })
    content = forms.CharField(label='邮件内容',
                              required=True,
                              max_length=16,
                              error_messages={
                                  'required': '邮件内容必须填写'
                              })

    def clean_to_user(self):
        to_user = self.cleaned_data['to_user']
        if not User.objects.filter(id=to_user).exists():
            raise forms.ValidationError('该用户不存在或者已经被删除了')
        return to_user

    def clean(self):
        data = super().clean()
        logs.info(data)
        # 如果单个字段有错误，直接返回，不执行后面的验证
        if self.errors:
            return
        return data

    @transaction.atomic()
    def do_send_email_go(self, request):
        """
        发送私人邮件
        :param request:
        :return:
        """

        try:
            user = request.user

            data = self.cleaned_data
            to_user = data.get('to_user', '')
            title = data.get('title', '')
            content = data.get('content', '')

            email_go = EmailGo(user=user, user_to_id=to_user, title=title, content=content)
            email_go.save()

            return True
        except Exception as e:
            logs.error(e)
            return None
