from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, UserInfo


@admin.register(User)
class MyUserAdmin(UserAdmin):
    """
    用户基础管理
    """

    # 展示字段
    list_display = ('username', 'nickname', 'email', 'last_login', 'is_active')
    # 查询字段
    search_fields = ('username', 'email', 'nickname')
    # 每一页条数
    list_per_page = 5
    # 批量处理
    actions = ['disable_user', 'enable_user']
    # 新增的表单
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nickname', )}),
    )
    # 修改的表单
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname', )}),
    )
    # 时间分层
    date_hierarchy = 'last_login'

    def disable_user(self, request, queryset):
        queryset.update(is_active=False)

    def enable_user(self, request, queryset):
        queryset.update(is_active=True)

    disable_user.short_description = '禁用'
    enable_user.short_description = '启用'


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    """
    用户详细信息
    """

    # 展示字段
    list_display = ('username', 'email', 'phone', 'signature', 'sex', 'age', 'status')
    # 查询字段
    search_fields = ('username', 'email', 'phone', 'signature')
    # 每一页条数
    list_per_page = 5
    # 批量处理
    actions = ['disable_user', 'enable_user']
    # 选择字段
    list_filter = ('sex', 'status')
    # 时间分层
    date_hierarchy = 'created_at'

    def disable_user(self, request, queryset):
        queryset.update(status=1)

    def enable_user(self, request, queryset):
        queryset.update(status=0)

    disable_user.short_description = '隐身'
    enable_user.short_description = '在线'


# 用户后台标题
admin.site.site_header = '锦词管理后台'
admin.site.site_title = '锦词后台'
admin.site.index_title = '3'
