from django.contrib import admin

from system.models import FilePost


@admin.register(FilePost)
class PlateAdmin(admin.ModelAdmin):
    """
    板块
    """

    # 展示字段
    list_display = ('user', 'title', 'file', 'status', 'created_at')
    # 查询字段
    search_fields = ('file', 'user', 'title')
    # 每一页条数
    list_per_page = 15
    # 批量处理
    actions = ['disable_file', 'enable_file']
    # 选择字段
    list_filter = ('status', )
    # 时间分层
    date_hierarchy = 'created_at'

    def disable_file(self, request, queryset):
        queryset.update(status=0)

    def enable_file(self, request, queryset):
        queryset.update(status=1)

    disable_file.short_description = '失效'
    enable_file.short_description = '生效'
