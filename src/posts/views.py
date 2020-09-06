from django.shortcuts import render,redirect
from .models import Post,Like
from profiles.models import Profile
from .forms import PostForm,CommentForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView,DeleteView
# Create your views here.

def posts_list(request):
    user = request.user
    qs = Post.objects.all()
    profile = Profile.objects.get(user=user)

    #initials
    p_form = PostForm()
    c_form = CommentForm()

    if 'p_form' in request.POST:
        p_form = PostForm(request.POST,request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostForm()

    if 'c_form' in request.POST:
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentForm()
    context = {
        'qs': qs,
        'profile': profile,
        'p_form' : p_form,
        'c_form' : c_form,
        }



    return render(request,'posts/main.html',context)


def like_unlike_post(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like,created = Like.objects.get_or_create(user=profile,post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

        post_obj.save()
        like.save()
    return redirect('posts:posts-list')



class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:posts-list')

    def get_object(self,*args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            message.warning('you need to be the author of the post...')
        return obj


class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:posts-list')

    def form_invalid(self,form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None,'you need to be the author of the post...')
            return super().form_invalid(form)
