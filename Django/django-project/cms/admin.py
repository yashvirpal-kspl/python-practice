from django.contrib import admin
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'is_published',
        'updated_at',
        'seo_title',
    )
  
    list_filter = ('is_published','title')
    search_fields = ('title', 'content','seo_title')
    prepopulated_fields = {'slug': ('title',)}