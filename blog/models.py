# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
#from django.utils import timezone
import hashlib
import datetime
from ckeditor.fields import RichTextField 
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Tag(models.Model):
    """Tags (e.g. gaming, linux). """
    name = models.CharField('Name', max_length=100, unique=True, help_text='Tag name, e.g. programming, linux.')
    created_at = models.DateTimeField('Created at', auto_now_add=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    """The article / blog post model. """
    uuid = models.CharField(max_length=56, unique=True, null=True, editable=False)
    title = models.CharField('Title', max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, help_text='Automatically generated.')
    description = models.TextField(max_length=500)
    content = RichTextUploadingField()
    tag = models.ManyToManyField(Tag, blank=True)
    publish = models.BooleanField('Publish?', default=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    modified_at = models.DateTimeField('Modified at', auto_now=True)
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:article', kwargs={'year': self.created_at.year, 'slug': self.slug})

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def save(self):
        if self.uuid is None:
            string_seed = str(datetime.datetime.now()).encode('utf-8')
            self.uuid = hashlib.sha224(string_seed).hexdigest()
        if self.slug is None:
            self.slug = slugify(self.title)
        super(Article, self).save()

    def __str__(self):
        return self.title
