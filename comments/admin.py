from django.contrib import admin

from comments.models import CommentTwo, CommentOne


class CommentTwoListLine(admin.StackedInline):
    model = CommentTwo
    extra = 0
    can_delete = False
    # 定义展示的字段和顺序
    fields = ('user', 'comment_one', 'user_to', 'content', 'status')

    def has_add_permission(self, request, obj=None):
        """
        不允许这个inline类增加记录 (当然也增加不了，readonly_fileds中定义的字段，在增加时无法输入内容)
        """
        return False


@admin.register(CommentOne)
class CommentAdmin(admin.ModelAdmin):
    """
    评论
    """

    # 展示字段
    list_display = ('user', 'title', 'content', 'created_at', 'status', )
    # 查询字段
    search_fields = ('user', 'title', 'content', )
    # 每一页条数
    list_per_page = 15
    # 批量处理
    actions = ['disable_comment', 'enable_comment']
    # 选择字段
    list_filter = ('status', )
    # 时间分层
    date_hierarchy = 'created_at'

    inlines = [CommentTwoListLine]

    def disable_comment(self, request, queryset):
        queryset.update(status=0)

    def enable_comment(self, request, queryset):
        queryset.update(status=1)

    disable_comment.short_description = '失效'
    enable_comment.short_description = '生效'
