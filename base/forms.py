from django.forms import ModelForm
from .models import Room, UserProfile, ChatBox, Folder, StudyMaterials, ChatBoxMembership, InfoContent, InfoContentUrl, Tag, CodeSnippet, CodeFolder
from django.contrib.auth.models import User
from django import forms
from django_select2.forms import Select2Widget, ModelSelect2Widget
from django.core.exceptions import ValidationError

from django_select2.forms import ModelSelect2MultipleWidget  # use Multiple widget!



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'tags', 'is_private']
        widgets = {
            'tags': ModelSelect2MultipleWidget(
                model=Tag,
                search_fields=['name__icontains'],
                attrs={
                    'data-placeholder': 'Search and select up to 4 tags...',
                    'class': 'select2-multiple',
                    'data-maximum-selection-length': '4'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all().order_by('name')
        self.fields['tags'].required = False
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags and tags.count() > 4:
            raise ValidationError("You can select a maximum of 4 tags.")
        return tags


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


class CodeSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ['title', 'language', 'code']
        widgets = {
            'code': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': 'Paste your code here...',
                'style': 'font-family: monospace;'
            })
        }

class CodeFolderForm(forms.ModelForm):
    class Meta:
        model = CodeFolder
        fields = ['name']



