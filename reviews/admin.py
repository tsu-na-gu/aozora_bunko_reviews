from django.contrib import admin
from django.utils.html import format_html

from .models import Author, Review, Work


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'wikipedia_link')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('creator', 'short_content', 'date_created')
    autocomplete_fields = ['book']

    def short_content(self, obj):
        if len(obj.content) < 15:
            return format_html("<span title={}'>{}</span>", obj.content, obj.content[:15] + '...')

    short_content.short_description = 'Content'

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    search_fields = ['title']