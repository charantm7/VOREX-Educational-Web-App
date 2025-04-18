from django.forms import ModelForm
from .models import Room, UserProfile, ChatBox, Folder, StudyMaterials, ChatBoxMembership, InfoContent, InfoContentUrl
from django.contrib.auth.models import User
from django import forms

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'tags','is_private']
        

class ProfileForm(ModelForm):
    class Meta:
        model= UserProfile
        fields = ['profile_pic', 'bio']
        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'accept': 'profile_pic/*'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].initial = None
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name']


class ChatBoxForm(forms.ModelForm):
    class Meta:
        model = ChatBox
        fields = ['group_name']

class ChatBoxMemberForm(forms.ModelForm):

    class Meta:
        model = ChatBoxMembership
        fields = ['content']
        
        

class FolderForm(ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

class StudyMaterialForm(ModelForm):
    class Meta:
        model = StudyMaterials
        fields = ['title', 'file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': 'application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].initial = None


class InfoContentForm(forms.ModelForm):
    class Meta:
        model = InfoContent
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Enter content'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].initial = None
        
        
    

class InfoContentUrlForm(forms.ModelForm):
    class Meta:
        model = InfoContentUrl
        fields = ['title', 'url']
        
        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'Enter URL'}),  # Fix this line
            'title': forms.TextInput(attrs={'placeholder': 'Enter Title'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].initial = None