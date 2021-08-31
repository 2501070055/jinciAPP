from django.apps import apps
from django.contrib import admin

from plates.models import Plate, Title, Content, Label, Collect, HotPost
from system.models import FilePost


class ContentListLine(admin.StackedInline):
    model = Content
    extra = 0
    can_delete = False
    # 定义展示的字段和顺序
    fields = ('post_content', )

    def has_add_permission(self, request, obj=None):
        """
        不允许这个inline类增加记录 (当然也增加不了，readonly_fileds中定义的字段，在增加时无法输入内容)
        """
        return False


class FileListLine(admin.StackedInline):
    model = FilePost
    extra = 0
    can_delete = False
    # 定义展示的字段和顺序
    readonly_fields = ('user', 'file')

    def has_add_permission(self, request, obj=None):
        """
        不允许这个inline类增加记录 (当然也增加不了，readonly_fileds中定义的字段，在增加时无法输入内容)
        """
        return False


@admin.register(Title)
class ContentAdmin(admin.ModelAdmin):
    """
    帖子标题
    """

    # 展示字段
    list_display = ('post_title', 'status', 'post_time', )
    # 查询字段
    search_fields = ('post_title', 'content__post_content', )
    # 每一页条数
    list_per_page = 15
    # 批量处理
    actions = ['disable_post', 'enable_post']
    # 选择字段
    list_filter = ('status', )
    # 联系外表
    list_select_related = ('content', )
    # 时间分层
    date_hierarchy = 'post_time'

    filter_horizontal = ('label', )

    inlines = [FileListLine, ContentListLine]

    def disable_post(self, request, queryset):
        queryset.update(status=0)

    def enable_post(self, request, queryset):
        queryset.update(status=1)

    disable_post.short_description = '失效'
    enable_post.short_description = '生效'


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    """
    标签
    """

    # 展示字段
    list_display = ('label_title', 'label_dp', 'created_at', )
    # 查询字段
    search_fields = ('label_title', 'label_dp', )
    # 每一页条数
    list_per_page = 15
    # 批量处理
    actions = ['disable_label', 'enable_label']
    # 选择字段
    list_filter = ('status', )
    # 时间分层
    date_hierarchy = 'created_at'

    def disable_label(self, request, queryset):
        queryset.update(status=0)

    def enable_label(self, request, queryset):
        queryset.update(status=1)

    disable_label.short_description = '失效'
    enable_label.short_description = '生效'


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    """
    收藏
    """

    # 展示字段
    list_display = ('user', 'post', 'status',  'created_at')
    # 查询字段
    search_fields = ('post', )
    # 每一页条数
    list_per_page = 15
    # 批量处理
    actions = ['disable_label', 'enable_label']
    # 选择字段
    list_filter = ('status', )
    # 时间分层
    date_hierarchy = 'created_at'

    def disable_label(self, request, queryset):
        queryset.update(status=0)

    def enable_label(self, request, queryset):
        queryset.update(status=1)

    disable_label.short_description = '失效'
    enable_label.short_description = '生效'


@admin.register(HotPost)
class HotPostAdmin(admin.ModelAdmin):
    """
    热门设置
    """

    # 展示字段
    list_display = ('title', 'status', 'created_at')
    # 查询字段
    search_fields = ('title', )
    # 每一页条数
    list_per_page = 15
    # 批量处理
    actions = ['disable_label', 'enable_label']
    # 选择字段
    list_filter = ('status', )
    # 时间分层
    date_hierarchy = 'created_at'

    def disable_label(self, request, queryset):
        queryset.update(status=0)

    def enable_label(self, request, queryset):
        queryset.update(status=1)

    disable_label.short_description = '失效'
    enable_label.short_description = '生效'


@admin.register(Plate)
class PlateAdmin(admin.ModelAdmin):
    """
    板块
    """

    # 展示字段
    list_display = ('plate_title', 'plate_dp', 'status')
    # 查询字段
    search_fields = ('plate_title', )
    # 每一页条数
    list_per_page = 15
    # 批量处理
    actions = ['disable_plate', 'enable_plate']
    # 选择字段
    list_filter = ('status', )
    # 时间分层
    date_hierarchy = 'created_at'

    def disable_plate(self, request, queryset):
        queryset.update(status=0)

    def enable_plate(self, request, queryset):
        queryset.update(status=1)

    disable_plate.short_description = '失效'
    enable_plate.short_description = '生效'
