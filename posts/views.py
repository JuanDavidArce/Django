"""Post Views"""
#Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views.generic import ListView, DetailView,CreateView,UpdateView,RedirectView
from django.views import View
#Forms
from posts.forms import PostForm

#Models
from posts.models import Post, Like


# Create your views here.

class PostLike(View,LoginRequiredMixin):
    """Update Likes"""
    def post(self, request, *args, **kwargs):
        """Logic for the GET method"""
        ubication=request.POST['ubication']
        post=Post.objects.get(id = request.POST['post_id'])
        user= User.objects.get(id=request.user.pk)
        post_id= post.pk
        user_id= user.pk
        profile_id=user.profile.pk
        like= Like.objects.filter(post_id=post_id).filter(user_id=user_id).filter(profile_id=profile_id)
        if len(like)==0:
            new_like= Like(user_id=user_id,profile_id=profile_id,post_id=post_id)
            post.likes+=1
            post.save()
            new_like.save()
        else:
            like.delete()
            post.likes-=1
            post.save()
        if ubication=='feed':
            return redirect('posts:feed')
        else:
            return redirect('posts:detail',post_id)



class PostsFeedView(LoginRequiredMixin,ListView):
    """Return All Published posts"""
    template_name='posts/feed.html'
    Model=Post
    queryset=Post.objects.all()
    ordering=('-created')
    paginate_by=30
    context_object_name='posts'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PostsFeedView, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['ubication'] = 'feed'
        return context

class PostDetailView(LoginRequiredMixin,DetailView):
    """Return post detail"""
    template_name='posts/detail.html'
    queryset= Post.objects.all()
    context_object_name='post'
    
    


class CreatePostView(LoginRequiredMixin,CreateView):
    """Create new post view"""
    #DON'T FORGET THE VALIDATION OF A PREVIOUS LIKE
    template_name='posts/new.html'
    form_class=PostForm
    success_url=reverse_lazy('posts:feed')
    def get_context_data(self, **kwargs):
        """Add user and profile context"""
        context= super().get_context_data(**kwargs)
        context['user']=self.request.user
        context['profile']=self.request.user.profile
        return context
