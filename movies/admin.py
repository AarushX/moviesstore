from django.contrib import admin

# Register your models here.
from .models import Movie, Review

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'user', 'date', 'is_hidden', 'like_count')
    list_filter = ('is_hidden', 'date', 'movie')
    search_fields = ('comment', 'user__username', 'movie__name')
    ordering = ('-date',)

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)