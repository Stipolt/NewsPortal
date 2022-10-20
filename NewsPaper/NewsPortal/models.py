from django.contrib.auth.models import User
from django.db import models
from django.urls import  reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _auth_rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'

    def update_rating(self):
        self._auth_rating = 0
        for post in Post.objects.filter(author__user=self.user):
            self._auth_rating += post.post_rating * 3
            for comment in Comment.objects.filter(post=post):
                self._auth_rating += comment.comment_rating
        for comment in Comment.objects.filter(user=self.user):
            self._auth_rating += comment.comment_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS)
    time_post = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=255)
    content = models.TextField()
    _post_rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # 1 to many Author
    category = models.ManyToManyField(Category, through='PostCategory')  # many to many Category

    @property
    def post_rating(self):
        return self._post_rating

    def like(self):
        self._post_rating += 1
        self.save()

    def dislike(self):
        self._post_rating -= 1
        self.save()

    def preview(self):
        _preview = self.content[:125] + "..."
        return _preview

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class PostCategory(models.Model):  # binding model many to many Post - Category
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    _comment_rating = models.IntegerField(default=0)

    @property
    def comment_rating(self):
        return self._comment_rating

    def like(self):
        self._comment_rating += 1
        self.save()

    def dislike(self):
        self._comment_rating -= 1
        self.save()
