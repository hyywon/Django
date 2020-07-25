from django.shortcuts import render
from django.http import HttpResponseRedirect
from second.models import Post
from .forms import PostForm
# Create your views here.

def list(request):
    context = {
        'items' : Post.objects.all()
    }
    return render(request,'second/list.html',context)

def create(request):
    #request 검사
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid(): #정해진 조건 만족 확인
            #model schema에 자동으로 연결&저장
            new_item = form.save()
        # Post로 접근했을 때, list로 보냄
        return HttpResponseRedirect('/second/list/')

    #일반적으로 접근했을 때,create로 rendering
    form = PostForm()
    return render(request,'second/create.html', {'form': form})

def confirm(request):
    #POST data가 바로 confirm Instance로 전달됨
    form = PostForm(request.POST)
    if form.is_valid():
        return render(request, 'second/confirm.html',{'form': form})
    #문제가 있을 때, 특정 페이지로 자동으로 이동해줌 [create]
    return HttpResponseRedirect('/second/create/')