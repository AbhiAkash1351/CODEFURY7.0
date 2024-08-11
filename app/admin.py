from django.contrib import admin
from .models import Community, Post, ChatMessage


# class CommunityAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description', 'created_at')
#     search_fields = ('name',)


# class PostAdmin(admin.ModelAdmin):
#     list_display = ('user', 'community', 'created_at')
#     search_fields = ('user__username', 'community__name')
#     list_filter = ('community', 'created_at')


# class ChatMessageAdmin(admin.ModelAdmin):
#     list_display = ('user', 'community', 'message', 'created_at')
#     search_fields = ('user__username', 'community__name', 'message')
#     list_filter = ('community', 'created_at')


admin.site.register(Community)
admin.site.register(Post)
# admin.site.register(ChatMessage)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'community', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)
    fields = ('user', 'community', 'content', 'image', 'video', 'created_at')
    readonly_fields = ('created_at',)
