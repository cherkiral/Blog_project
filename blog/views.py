from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post, Comments
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.shortcuts import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

def home(request):
    posts = Post.objects.all()
    content = {
        'posts': posts
    }
    return render(request, 'blog/home.html', content)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_create.html'


    def form_valid(self, form):
        messages.success(self.request, 'You have updated the post')
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog_home')
    context_object_name = 'delete_post'
    template_name = 'blog/post_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

    def form_valid(self, form):
        messages.success(self.request, 'You have deleted the post')
        return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comments
    fields = ['content']
    template_name = 'blog/comment_create.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.author = self.request.user
        messages.success(self.request, 'You have made a comment')
        return super().form_valid(form)

class CommentDetailView(LoginRequiredMixin, DetailView):
    model = Comments
    template_name = 'blog/comment_detail.html'
    context_object_name = 'comments'


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comments
    fields = ['content']
    template_name = 'blog/comment_create.html'

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        else:
            return False

    def form_valid(self, form):
        messages.success(self.request, 'You have updated the post')
        return super().form_valid(form)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comments
    context_object_name = 'delete_comment'
    template_name = 'blog/comment_delete.html'

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        else:
            return False

    def form_valid(self, comment):
        messages.success(self.request, 'You have deleted the comment')
        return super().form_valid(comment)

    def get_success_url(self):
        post_pk = self.get_object().post.pk
        return reverse('post_detail', kwargs={'pk': post_pk})

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})