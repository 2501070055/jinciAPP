
from django.contrib import admin
from emaillist.models import OpenEmail, EmailGo


@admin.register(OpenEmail)
class OpenEmailAdmin(admin.ModelAdmin):
    """
    邮件
    """

    # 展示字段
    list_display = ('user', 'title', 'content', 'created_at', 'status', )
    # 查询字段
    search_fields = ('user', 'title', 'content', )
    # 每一页条数
    list_per_page = 15
    # 批量处理
    actions = ['disable_email', 'enable_email']
    # 选择字段
    list_filter = ('status', )
    # 时间分层
    date_hierarchy = 'created_at'

    def disable_email(self, request, queryset):
        queryset.update(status=0)

    def enable_email(self, request, queryset):
        queryset.update(status=1)

    disable_email.short_description = '失效'
    enable_email.short_description = '生效'


@admin.register(EmailGo)
class OpenEmailAdmin(admin.ModelAdmin):
    """
    邮件
    """

    # 展示字段
    list_display = ('user', 'user_to', 'title', 'content', 'created_at', 'status', )
    # 查询字段
    search_fields = ('user', 'title', 'content', )
    # 每一页条数
    list_per_page = 15
    # 批量处理
    actions = ['disable_email', 'enable_email']
    # 选择字段
    list_filter = ('status', )
    # 时间分层
    date_hierarchy = 'created_at'

    def disable_email(self, request, queryset):
        queryset.update(status=0)

    def enable_email(self, request, queryset):
        queryset.update(status=1)

    disable_email.short_description = '失效'
    enable_email.short_description = '生效'
