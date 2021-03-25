from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from Blog.models import Post, Comment
from Blog.forms import PostForm, CommentForm

# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):  ### Main Page view, listing all the posts
    model = Post

    def get_queryset(self):   ### query the data from the Post model, get the published posts
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin, CreateView):  ### Create Post Page view,
    ### Since we don't want anyone to be able to access "Creating Post", we require login
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):  ### Update Post Page view,
    ### Since we don't want anyone to be able to access "Creating Post", we require login
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):  ### Delete Post Page view,
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'Blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).order_by('created_date')

#########################################################################################################3
###################################################################################################################

### pk stands for "primary key"
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.publish()
    return redirect('post_detail', pk = pk)  ### takes you to the "post_detail.html" page

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk = pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = CommentForm()
    return render(request, 'Blog/comment_form.html', context = {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    comment.approve()
    return redirect('post_detail', pk = comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk = post_pk)
