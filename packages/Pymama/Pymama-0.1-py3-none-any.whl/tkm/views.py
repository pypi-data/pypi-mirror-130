from typing import Counter
from django.shortcuts import render,redirect,get_object_or_404
from tkm.forms import *
from tkm.models import *
# Create your views here.


def index(request):
    return render(request, 'index.html')




def dashboard(request):
    return render(request, 'userpost.html',)

def profile(request):
    posts = Post.objects.filter(author=request.user, published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'profile.html', {'data':posts})







def customerregistration(request):
    if request.method=='POST':
        form=CustomerRegisterationsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form=CustomerRegisterationsForm()
    args={'form':form}
    return render(request,'register.html',args)    




def post_list(request):
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

