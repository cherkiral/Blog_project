from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from blog.models import Post, Comments
from users.models import User
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.shortcuts import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    authors = User.objects.all()

    context = {
        'posts': posts,
        'authors': authors,
    }
    return render(request, 'blog/home.html', context)

# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/home.html'
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#     paginate_by = 3

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data

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



def posts_fltered_by_user(request, pk):
    posts = Post.objects.filter(author__id=pk)
    context = {
        'posts': posts,
    }
    return render(request, 'blog/home.html', context)

def BlogPostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[pk]))

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})