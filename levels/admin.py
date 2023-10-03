from django.contrib import admin

from massassi.admin import MassassiModelAdmin
from news.models import News
from .models import Level, LevelCategory, LevelComment

class LevelCategoryAdmin(MassassiModelAdmin):
    list_display = ('id', 'name', 'path', 'game', 'enable_3dpreview')
    fields = ('name', 'path', 'game', 'enable_3dpreview')


admin.site.register(LevelCategory, LevelCategoryAdmin)

class LevelAdmin(MassassiModelAdmin):
    list_display = ('id', 'name', 'category', 'author', 'last_modified_at')
    search_fields = ('id', 'name', 'author')
    readonly_fields = ('file_hash', 'file_size', 'dl_count', 'rate_count', 'rating', 'comment_count')
    fields = (
        'category', 'name', 'description', 'author', 'email', 'file',
        'file_hash', 'file_size', 'screenshot_1', 'screenshot_2',
        'dl_count', 'comment_count', 'rate_count', 'rating'
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # If it's a new level, add a news post
        if not change:
            headline_fmt = "New {}: {}"
            story_fmt = """
                <b>File:</b> <a href="/levels/files/{level_id}.shtml">{level_name}</a><br>
                <b>Author:</b> {level_author}<br>
                <b>Description:</b> <font color="gray">{level_description}</font><br>
                <a href="/cgi-bin/screenshot.cgi?levels/files/screenshots/{level_id}_1.jpg">
                    <img border="1" vspace="4" width=400 height=300 src="/levels/files/thumbnails/{level_id}_1.jpg"></a>
                <a href="/cgi-bin/screenshot.cgi?levels/files/screenshots/{level_id}_2.jpg">
                    <img border="1" vspace="4" width=400 height=300 src="/levels/files/thumbnails/{level_id}_2.jpg"></a>
            """
            news_post = News(
                user = request.user,
                headline = headline_fmt.format(obj.category.name, obj.name),
                story = story_fmt.format(
                    level_id = obj.id,
                    level_name = obj.name,
                    level_description = obj.description,
                    level_author = obj.author,
                ),
            )

            news_post.save()

admin.site.register(Level, LevelAdmin)

class LevelCommentAdmin(MassassiModelAdmin):
    list_display = ('id', 'level', 'user', 'comment', 'ip', 'date_created')
    search_fields = ('id', 'level__name', 'user__username', 'comment', 'ip', 'date_created')
    readonly_fields = ('id', 'level', 'user', 'comment', 'ip', 'date_created')
    fields = ('id', 'level', 'user', 'comment', 'ip', 'date_created')

admin.site.register(LevelComment, LevelCommentAdmin)
