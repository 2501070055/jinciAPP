"""
Django settings for jinci project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import time
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5jh*4ey&o0aa^q24wbj5-$o1=zk(y#6#6%3^wa)^ef%325$y4='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # 后台面板
    'simpleui',
    # md编辑器
    'mdeditor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 用户模块
    'users.apps.UsersConfig',
    # 系统模块（验证码接口）
    'system.apps.SystemConfig',
    # 板块模块
    'plates.apps.PlatesConfig',
    # 评论模块
    'comments.apps.CommentsConfig',
    # 邮件模块
    'emaillist.apps.EmaillistConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jinci.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jinci.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jinci_django',
        'USER': 'root',
        'PASSWORD': 'abc123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            # 设置关闭外键
            'init_command': 'SET foreign_key_checks = 0,'
                            'sql_mode="STRICT_TRANS_TABLES"'
        }
    }
}


# 缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_ROOT = 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# 用户模块设置
AUTH_USER_MODEL = 'users.User'

# 媒体文件
MEDIA_URL = 'http://localhost:8000/medias/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'medias').replace('\\', '/')

# 邮箱设置
# 发送邮箱验证码
EMAIL_HOST = "smtp.163.com"  # 服务器
EMAIL_PORT = 25  # 一般情况下都为25
EMAIL_HOST_USER = "zrriii@163.com"  # 账号
EMAIL_HOST_PASSWORD = "KHAWAOYEMACQXUQR"  # 密码 (注意：这里的密码指的是授权码)
EMAIL_USE_TLS = False  # 一般都为False
EMAIL_FROM = "zrriii@163.com"  # 邮箱来自


AUTH_API = 'zrrwhnqh199817'


cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
if not os.path.exists(log_path):
    os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        # 日志格式
        'standard': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
                      '[%(levelname)s]- %(message)s'},
        'simple': {  # 简单格式
            'format': '%(levelname)s %(message)s'
        },
    },
    # 过滤
    'filters': {
    },
    # 定义具体处理日志的方式
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'all-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'error-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 输出警告日志
        'warning': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'warning-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 控制台输出
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 输出info日志
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'info-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',  # 设置默认编码
        },
    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        # 类型 为 django 处理所有类型的日志， 默认调用
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        # log 调用时需要当作参数传入
        'log': {
            'handlers': ['error', 'info', 'console', 'default', 'warning'],
            'level': 'INFO',
            'propagate': True
        },
    }
}


# 离线模式
SIMPLEUI_STATIC_OFFLINE = True

# 菜单自定义
SIMPLEUI_CONFIG = {
    'system_keep': False,
    # 开启排序和过滤功能, 不填此字段为默认排序和全部显示, 空列表[] 为全部不显示.
    'menu_display': ['ZR博客', '帖子', '收藏', '标签', '热门', '板块主题', '评论管理', '邮件管理', '文件管理', '用户组',
                     '用户', '用户详细信息', '认证和授权', '组', '文件', '评论', '公共邮件', '私人邮件'],
    'dynamic': False,  # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
    'menus': [{
        'name': 'ZR博客',
        'icon': 'fas fa-blog',
        'url': 'https://www.zrr.show/'
    }, {
        'app': 'auth',
        'name': '认证和授权',
        'icon': 'fas fa-user-shield',
        'models': [{
            'name': '组',
            'icon': 'fa fa-user',
            'url': 'auth/group/'
        }]
    }, {
        'app': 'users',
        'name': '用户组',
        'icon': 'fas fa-users',
        'models': [{
            'name': '用户',
            'icon': 'fas fa-user',
            'url': '/admin/users/user/'
        }, {
            'name': '用户详细信息',
            'icon': 'fas fa-user',
            'url': '/admin/users/userinfo/'
        }]
    }, {
        'app': 'system',
        'name': '文件管理',
        'icon': 'fas fa-folder-open',
        'models': [{
            'name': '文件',
            'icon': 'fas fa-upload',
            'url': '/admin/system/filepost/'
        }]
    }, {
        'app': 'plates',
        'name': '板块主题',
        'icon': 'fas fa-list-ul',
        'models': [{
            'name': '帖子',
            'icon': 'fas fa-book-open',
            'url': '/admin/plates/title/'
        }, {
            'name': '标签',
            'icon': 'fas fa-tags',
            'url': '/admin/plates/label/'
        }, {
            'name': '热门',
            'icon': 'fab fa-hotjar',
            'url': '/admin/plates/hotpost/'
        }, {
            'name': '收藏',
            'icon': 'fas fa-bowling-ball',
            'url': '/admin/plates/collect/'
        }, {
            'name': '板块主题',
            'icon': 'fab fa-buffer',
            'url': '/admin/plates/plate/'
        }]
    }, {
        'app': 'comments',
        'name': '评论管理',
        'icon': 'fas fa-comment-alt',
        'models': [{
            'name': '评论',
            'icon': 'fas fa-comment-dots',
            'url': '/admin/comments/commentone/'
        }]
    }, {
        'app': 'emaillist',
        'name': '邮件管理',
        'icon': 'fas fa-mail-bulk',
        'models': [{
            'name': '公共邮件',
            'icon': 'fas fa-inbox',
            'url': '/admin/emaillist/openemail/'
        }, {
            'name': '私人邮件',
            'icon': 'fas fa-envelope',
            'url': '/admin/emaillist/emailgo/'
        }]
    }]
}

# 服务器消息不显示
SIMPLEUI_HOME_INFO = False

# 自定义LOGO
SIMPLEUI_LOGO = 'https://cdn.jsdelivr.net/gh/2501070055/PIC/usr/uploads/2021/01/984714669.png'

# md文档编辑器设置
MDEDITOR_CONFIGS = {
'default':{
    'width': '100%',  # 自定义编辑框宽度
    'heigth': 500,   # 自定义编辑框高度
    'toolbar': ["undo", "redo", "|",
                "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                "h1", "h2", "h3", "h5", "h6", "|",
                "list-ul", "list-ol", "hr", "|",
                "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime",
                "html-entities", "pagebreak", "goto-line", "|",
                "||", "preview", "watch", "fullscreen"],  # 自定义编辑框工具栏
    'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # 图片上传格式类型
    'image_folder': 'editor',  # 图片保存文件夹名称
    'theme': 'default',  # 编辑框主题 ，dark / default
    'preview_theme': 'default',  # 预览区域主题， dark / default
    'editor_theme': 'default',  # edit区域主题，pastel-on-dark / default
    'toolbar_autofixed': True,  # 工具栏是否吸顶
    'search_replace': True,  # 是否开启查找替换
    'emoji': False,  # 是否开启表情功能
    'tex': True,  # 是否开启 tex 图表功能
    'flow_chart': True,  # 是否开启流程图功能
    'sequence': True,  # 是否开启序列图功能
    'watch': True,  # 实时预览
    'lineWrapping': False,  # 自动换行
    'lineNumbers': False  # 行号
    }
}

X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_CONTENT_TYPE_NOSNIFF = False