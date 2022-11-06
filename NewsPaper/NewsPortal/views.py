from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category, PostCategory
from .filters import NewsFilter
from .forms import NewsForm
from .tasks import send_to_sub


class NewsList(ListView):
    model = Post
    ordering = 'time_post'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs


class NewsDetail(DetailView):
    model = Post
    template_name = 'current_news.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        category_id = PostCategory.objects.filter(post_id=pk).values('category_id')[0]['category_id']
        context['category'] = Category.objects.values('category_name')[category_id-1]['category_name']
        return context


class NewsSearch(NewsList):
    template_name = 'search.html'


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    permission_required = ('NewsPortal.add_post',)
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = "NW"
        post = super().form_valid(form)
        categories = self.object.category.all()
        emails = []
        for category in categories:
            for sub in category.subscribers.all():
                email_ = sub.email
                emails.append(email_)
        send_to_sub(self.object, emails)
        return post


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    permission_required = ('NewsPortal.change_post',)
    template_name = 'news_edit.html'


class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    permission_required = ('NewsPortal.add_post',)
    template_name = 'article_edit.html'

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.categoryType = "AR"
        post = super().form_valid(form)
        categories = self.object.category.all()
        emails = []
        for category in categories:
            for sub in category.subscribers.all():
                email_ = sub.email
                emails.append(email_)
        send_to_sub(self.object, emails)
        return post


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    permission_required = ('NewsPortal.change_post',)
    template_name = 'article_edit.html'


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')


class CategoryView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categorys'
    queryset = Category.objects.all()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('news')


@login_required
def subscribe_cat(request, category_id):
    category = Category.objects.get(id=category_id)
    user = request.user
    if user not in category.subscribers.all():
        category.subscribers.add(user)
    else:
        category.subscribers.remove(user)
    return redirect('categories')

