import datetime
import logging
import random
import re

from django import forms
from django.contrib.auth import login, authenticate
from django.core.cache import cache
from django.db import transaction
from django.utils.timezone import now

from users.choices import SexChoices
from users.models import User, UserInfo

logs = logging.getLogger('log')


class RegisterForm(forms.Form):
    """
    用户注册
    """

    email = forms.CharField(label='邮箱',
                            max_length=128,
                            required=True,
                            error_messages={
                                'required': '输入正确的邮箱，建议使用QQ邮箱或者163邮箱'
                            })
    password = forms.CharField(label='用户密码',
                               max_length=256,
                               required=True,
                               error_messages={
                                   'required': '密码一定要滴'
                               })
    nickname = forms.CharField(label='昵称',
                               max_length=16,
                               required=True,
                               error_messages={
                                   'required': '昵称不可为空'
                               })

    def clean_email(self):
        """
        验证邮箱是不输入正确
        :return: email
        """

        email = self.cleaned_data['email']
        pattern = r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
        if not re.search(pattern, email):
            raise forms.ValidationError('邮箱%s输入有问题',
                                        code='invalid_email',
                                        params=(email, ))
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱%s已经存在啦',
                                        code='exist_email',
                                        params=(email, ))
        return email

    def clean_nickname(self):
        """
        昵称验证
        :return: email
        """

        nickname = self.cleaned_data['nickname']
        if User.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('昵称%s已被使用啦',
                                        code='exist_nickname',
                                        params=(nickname, ))
        return nickname

    def clean(self):
        data = super().clean()
        logs.info(data)
        if self.errors:
            return
        return data

    @transaction.atomic()
    def do_register(self, request):
        """
        注册
        :param request: 请求对象
        :return: user,info对象
        """

        data = self.cleaned_data
        version = request.headers.get('version', '')
        source = request.headers.get('source', '')
        try:
            # 1. 创建基础信息表
            user = User.objects.create_user(
                email=data.get('email', None),
                username=data.get('email', None),
                password=data.get('password', None),
                nickname=data.get('nickname', None)
            )
            # 2. 创建详细表
            user_info = UserInfo.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                version=version,
                source=source
            )
            # 3. 执行登录
            login(request, user)
            # 4. 记录登录日志
            user.last_login = now()
            user.date_joined = now()
            user.save()

            ip = request.META.get('REMOTE_ADDR', '')
            # 5. 记录登录历史
            user.add_login_record(
                username=user.username,
                ip=ip,
                version=version,
                source=source
            )
            return True
        except Exception as e:
            logs.error(e)
            return None


class LoginForm(forms.Form):
    """
    登录表单
    """
    username = forms.CharField(label='用户',
                               max_length=100,
                               required=False,
                               help_text='用户邮箱',
                               initial='2501070055@qq.com')
    password = forms.CharField(label='密码',
                               max_length=200,
                               min_length=6,
                               widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 当前登录的用户
        self.user = None

    def clean_username(self):
        """ 验证用户名 hook 钩子函数 """
        username = self.cleaned_data['username']
        pattern = r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
        if not re.search(pattern, username):
            raise forms.ValidationError('邮箱%s输入不正确',
                                        code='invalid_email',
                                        params=(username, ))
        return username

    def clean(self):
        data = super().clean()
        logs.info(data)
        # 如果单个字段有错误，直接返回，不执行后面的验证
        if self.errors:
            return
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名不存在或者密码不正确')
        else:
            if not user.is_active:
                raise forms.ValidationError('该用户已经被禁用')
        self.user = user
        return data

    @transaction.atomic()
    def do_login(self, request):
        """ 执行用户登录 """

        try:
            user = self.user
            # 调用登录
            login(request, user)
            # 修改最后登录的时间
            user.last_login = now()
            user.save()
            # 保存登录历史
            ip = request.META.get('REMOTE_ADDR', '')
            version = request.headers.get('version', '')
            source = request.headers.get('source', '')
            user.add_login_record(
                username=user.info.username,
                ip=ip,
                version=version,
                source=source
            )
            return True
        except Exception as e:
            logs.error(e)
            return None


class DetailForm(forms.Form):
    username = forms.CharField(label='用户名',
                               required=False)
    signature = forms.CharField(label='个性签名',
                                required=False,
                                help_text='个性签名',
                                initial='这个人太懒了，什么也没有留下')
    sex = forms.ChoiceField(choices=SexChoices.choices,
                            required=False,
                            initial=0)
    age = forms.DecimalField(label='年龄',
                             min_value=0,
                             max_value=200,
                             max_digits=16,
                             decimal_places=0,
                             initial=18,
                             required=False)
    avatar = forms.ImageField(label='图片',
                              required=False)

    def clean_sex(self):
        sex = self.cleaned_data.get('sex')
        if sex == '':
            sex = '1'
        if int(sex) not in (0, 1):
            raise forms.ValidationError('只能填0或者1，1为男，0为女')
        return sex

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None:
            age = '18'
        return age

    def clean(self):
        data = super().clean()
        logs.info(data)
        # 如果单个字段有错误，直接返回，不执行后面的验证
        if self.errors:
            return
        return data

    @transaction.atomic()
    def do_change_detail(self, request):
        """
        修改用户详细信息
        :return: data
        """

        try:
            user = request.user

            data = self.cleaned_data
            signature = data.get('signature', '')
            sex = data.get('sex', '')
            age = data.get('age', '')
            avatar = data.get('avatar', '')
            username = data.get('username', '')

            user.info.user_id = user.id
            user_info = user.info

            # 上传avatar修改图片名字
            if avatar is not None:
                ext = avatar.name.split('.')[-1]
                new_avatar_name = str(random.randint(111111, 999999)) + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                avatar.name = '{}'.format(new_avatar_name) + '.' + ext
                user_info.avatar = request.FILES.get('avatar')

            user_info.signature = signature
            user_info.sex = sex
            user_info.age = age
            user_info.username = username

            user_info.save()

            return True
        except Exception as e:
            logs.error(e)
            return None


