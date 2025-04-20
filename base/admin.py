from django.contrib import admin

# Register your models here.
from .models import Room, RoomMembership, ChatBox, Tag, StudyMaterials,UserProfile,Followrequest, Folder, ChatBoxMembership, RoomChatIndividual, Activity, InfoContent, InfoContentUrl, CodeSnippet, CodeFolder

admin.site.register(RoomMembership)
admin.site.register(StudyMaterials)
admin.site.register(ChatBox)
admin.site.register(Room)
admin.site.register(Tag)
admin.site.register(UserProfile)
admin.site.register(Followrequest)
admin.site.register(Folder)
admin.site.register(ChatBoxMembership)
admin.site.register(RoomChatIndividual)
admin.site.register(Activity)
admin.site.register(InfoContent)
admin.site.register(InfoContentUrl)
admin.site.register(CodeSnippet)
admin.site.register(CodeFolder)