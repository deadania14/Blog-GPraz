# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from blog.models import Tag, Article

# Create your views here.
def home(request):
    tag_list = Tag.objects.filter(article__gt=0).distinct().order_by('name')
    article_list = Article.objects.exclude(publish=False).order_by('-created_at')
    paginator = Paginator(article_list, 10, 3)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # Page number is not int, return first page
        articles = paginator.page(1)
    except EmptyPage:
        # Page num out of range, return last page
        articles = paginator.page(paginator.num_pages)

    context = {'tags': tag_list, 'articles': articles, 'page_title': 'Blog'}
    response = render(request, 'blog/index.html', context)
    return response

def blog(request, year, slug):
    from django.conf import settings
    article = get_object_or_404(Article, created_at__year=int(year), slug=str(slug), publish=True)
    recent_articles = Article.objects.exclude(pk=article.pk).exclude(publish=False).order_by('-views', '-created_at')[:10]
    
    context = {'article': article, 'recent_articles': recent_articles, 'show_comments': not settings.DEBUG}
    response = render(request, 'blog/view_article.html', context)

    # Page view counter cookies
    if request.COOKIES.get("view_%s" % str(article.uuid)) is None and not request.user.is_authenticated:
        response.set_cookie("view_%s" % str(article.uuid), value=str(article.title), expires=(datetime.datetime.now()+datetime.timedelta(days=2)))
        article.views += 1
        article.save()
    
    return response

def archive(request):
    return HttpResponse('todo')

def tag(request, tag_name):
    article_list = get_list_or_404(Article, tag__name=str(tag_name))
    tag_list = Tag.objects.filter(article__gt=0).distinct().order_by('name')

    paginator = Paginator(article_list, 10, 3)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # Page number is not int, return first page
        articles = paginator.page(1)
    except EmptyPage:
        # Page num out of range, return last page
        articles = paginator.page(paginator.num_pages)

    context = {'articles': articles, 'tags': tag_list, 'page_title': "Tag: '%s'" % tag_name}
    response = render(request, 'blog/index.html', context)
    return response
