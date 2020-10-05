from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Board,Topic,Post
from django.http import Http404
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.generic import UpdateView,ListView
from django.utils import timezone
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import NewTopicForm,PostForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
# this FBV
"""
def home(request):
    boards = Board.objects.all()
    
    boards_names = list()
    out_html =''
    for board in boards:
        boards_names.append(board.name)
    
    out_html = '<br>'.join(boards_names)

    return HttpResponse(out_html)
    
    return render(request,'home_base.html',{'boards':boards})
"""
# this is GCBV
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'board_list.html'

def home(request):
    boards = Board.objects.all()
    return render(request,'home_page.html',{'boards':boards})

def about(request):
    boards = Board.objects.all()
    return render(request,'about_me.html',{'boards':boards})

def stock(request):
    boards = Board.objects.all()
    return render(request,'stock_monitor.html',{'boards':boards})

# this is FBV for topics view
"""
def board_topics(request,pk):
    board = get_object_or_404(Board,pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
    
    page = request.GET.get('page',1)
    #page = 1

    paginator = Paginator(queryset,10)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # if in-valid page number-> return to last page
        topics = paginator.page(paginator.num_pages)

    return render(request,'topics_base.html',{'boards':Board.objects.all(),'board':board,'topics':topics})
"""
#this is GCBV for topics view
class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics_base.html'
    paginate_by = 20

    def get_context_data(self,**kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        self.board = get_object_or_404(Board,pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-views').annotate(replies=Count('posts')-1)
        return queryset

@login_required
def new_topic(request,pk):
    board = get_object_or_404(Board,pk=pk)

    if request.method =='POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )

            return redirect('topic_posts',pk=pk,topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    
    return render(request,'new_topic.html',{'boards':Board.objects.all(),'board':board,'form':form})

# GCBV for posts in topic
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 5

    def get_context_data(self,**kwargs):
        self.topic.views +=1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        self.topic = get_object_or_404(Topic,board__pk=self.kwargs.get('pk'),pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

@login_required
def reply_topic(request,pk,topic_pk):
    topic = get_object_or_404(Topic,board__pk=pk,pk=topic_pk)

    if request.method =='POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post  = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts',pk=pk,topic_pk=topic.pk)
    else:
        form = PostForm()
    
    return render(request,'reply_topic.html',{'boards':Board.objects.all(),'topic':topic,'form':form})

@method_decorator(login_required,name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self,form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk = post.topic.board.pk,topic_pk=post.topic.pk)

@method_decorator(login_required,name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name','last_name','email',)
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user

    def form_valid(self,form):
        # raising success alert
        messages.add_message(self.request,messages.SUCCESS,'Your profile is successfully changed!')
        return super().form_valid(form)
