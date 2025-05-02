from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Room, RoomMembership, ChatBox, Tag, StudyMaterials, UserProfile, Followrequest, Folder, ChatBoxMembership, Activity, InfoContent, InfoContentUrl, CodeSnippet, CodeFolder

admin.site.register(Room)
admin.site.register(RoomMembership)
admin.site.register(ChatBox)
admin.site.register(Tag)
admin.site.register(StudyMaterials)
admin.site.register(Folder)
admin.site.register(ChatBoxMembership)
admin.site.register(Activity)
admin.site.register(InfoContent)
admin.site.register(InfoContentUrl)
admin.site.register(CodeSnippet)
admin.site.register(CodeFolder)
admin.site.register(Followrequest)

class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)