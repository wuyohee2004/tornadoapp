from django.shortcuts import render_to_response

# Create your views here.

from django.http import HttpResponseRedirect
from models import *

def home(request):
    # print request
    # print '+'*100
    # print dir(request)
    # print '+'*100
    # print request.environ['USERNAME']
    return  render_to_response('index.html')

def blog(request,id):
    # temp_str = "The Blog ID is {{ blog_id }}"
    # t = Template(temp_str)
    # c = Context({'blog_id':id})
    # html = t.render(c)
    article = Article.objects.get(id=id)
    comments = Comment.objects.filter(Article=id).order_by("-id").all()
    print comments
    return render_to_response('blog.html',{'article':article,'comments':comments})
    # return HttpResponse(html)

def add(request):
    if request.method == 'POST':
        content = request.POST.get('content',None)
        title = request.POST.get('title',None)
        new = Article(content=content.encode("utf-8"),title=title.encode("utf-8"))
        new.save()
        return HttpResponseRedirect('/list/')
    return render_to_response('add.html',{'method_str':request.method})

def list(request):
    articles = Article.objects.order_by("-id").all()
    return render_to_response('list.html',{'articles':articles})

def comment_add(request):
    if request.method== 'POST':
        article_id = request.POST.get('article','')
        detail = request.POST.get('detail','')
        print detail
        if article_id and detail:
            comment = Comment()
            comment.Article = Article(id = article_id)
            comment.detail = detail
            comment.save()
        return HttpResponseRedirect('/blog/topic_%s' % article_id)

