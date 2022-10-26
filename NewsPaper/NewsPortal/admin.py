from django.contrib import admin
from .models import Post, PostCategory, Category, User, Author

admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Category)
admin.site.register(Author)

