from django.contrib import admin
from .models import Post, PostCategory, Category, Author, SubscribersCategory


class PostAdmin(admin.ModelAdmin):
    list_display = ('header', 'categoryType', 'time_post', '_post_rating')
    list_filter = ('categoryType', 'time_post')
    search_fields = ('header', 'time_post', 'categoryType')


class SubscribersCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'user')
    list_filter = ('category',)


admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(SubscribersCategory, SubscribersCategoryAdmin)


