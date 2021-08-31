import logging

from django import forms
from django.db import transaction

from plates.models import Plate, Title, Content, Label

logs = logging.getLogger('log')


class WriteArticle(forms.Form):
    """
    写文章
    """

    plate = forms.CharField(label='板块id',
                            max_length=16,
                            required=True,
                            error_messages={
                                'required': '必须填写板块id'
                            })
    label = forms.CharField(label='标签',
                            max_length=128,
                            required=False)
    post_title = forms.CharField(label='文章标题',
                                 max_length=16,
                                 required=True,
                                 error_messages={
                                     'required': '必须填写文章标题'
                                 })
    post_content = forms.CharField(label='文章内容',
                                   max_length=512,
                                   required=True,
                                   error_messages={
                                       'required': '文章内容必须填写'
                                   })

    def clean_plate(self):
        plate = self.cleaned_data['plate']
        if not Plate.objects.filter(status=1, id=plate).exists():
            raise forms.ValidationError('板块不存在')
        return plate

    def clean_label(self):
        label = self.cleaned_data['label']
        if label:
            label = label.split(',')
        return label

    def clean(self):
        data = super().clean()
        logs.info(data)
        # 如果单个字段有错误，直接返回，不执行后面的验证
        if self.errors:
            return
        return data

    @transaction.atomic()
    def do_write(self, request):
        """
        写文章
        :param request:
        :return:
        """
        try:
            data = self.cleaned_data
            plate_id = data.get('plate', '')
            post_title = data.get('post_title', '')
            post_content = data.get('post_content', '')
            label_list = data.get('label', '')

            user = request.user

            title = Title(plate_id=plate_id, user=user, post_title=post_title)
            title.save()

            label_list_query = []

            # 创建标签
            for item in label_list:
                label = Label(label_title=item, user=user)
                label.save()
                label_list_query.append(label)

            # 迭代label对象
            for item in label_list_query:
                title.label.add(item)
            title.save()

            content = Content(post=title, post_content=post_content)

            content.save()

            return True

        except Exception as e:
            logs.info(e)
            return None



