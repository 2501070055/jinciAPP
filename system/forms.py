import datetime
import logging
import random

from django import forms
from django.db import transaction

from plates.models import Title
from system.models import FilePost

logs = logging.getLogger('log')


class FileUploadForm(forms.Form):
    """
    附件上传
    """

    file = forms.FileField(label='文件上传',
                           required=False,
                           max_length=512)

    pid = forms.CharField(label='文章ID',
                          required=False,
                          max_length=16,)

    def clean_title_id(self):
        pid = self.cleaned_data['pid']
        if pid == '':
            return pid
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
    def do_upload_file(self, request):
        """
        上传文件
        :return:
        """

        try:
            user = request.user

            data = self.cleaned_data
            title_id = data.get('pid', '')
            file = data.get('file', '')

            # 处理文件名
            ext = file.name.split('.')[-1]
            file_new_name = str(random.randint(111111, 999999)) + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            file.name = '{}.{}'.format(file_new_name, ext)

            file_post = FilePost(title_id=title_id, user=user, file=file)
            file_post.save()

            return file_post

        except Exception as e:
            logs.error(e)
            return None
