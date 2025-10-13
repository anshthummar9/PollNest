from django.contrib import admin
from .models import Poll, Choice, Vote

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    list_display = ['question', 'created_by', 'created_at', 'is_active', 'total_votes']
    list_filter = ['is_active', 'created_at']
    search_fields = ['question']
    inlines = [ChoiceInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'choice', 'voted_at']
    list_filter = ['voted_at']
    search_fields = ['user__username']

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)
admin.site.register(Vote, VoteAdmin)
