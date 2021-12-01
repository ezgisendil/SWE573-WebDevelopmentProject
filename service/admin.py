from django.contrib import admin
from .models import Post, Event

# Register your models here.
admin.site.register(Post)
admin.site.register(Event)