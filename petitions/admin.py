from django.contrib import admin
from .models import Petition, PetitionVote


@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'requested_movie_title', 'created_by', 'created_at', 'yes_count')
    search_fields = ('title', 'requested_movie_title', 'description')
    list_filter = ('created_at',)


@admin.register(PetitionVote)
class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'petition', 'user', 'value', 'created_at')
    list_filter = ('created_at', 'value')
