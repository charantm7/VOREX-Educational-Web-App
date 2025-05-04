from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import cloudinary
import cloudinary.uploader
import cloudinary.api




class Tag(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name 

class Room(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="rooms",null=True)
    name = models.CharField(max_length=50)
    tags = models.ManyToManyField(Tag, related_name="rooms", blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    members_count = models.ManyToManyField(User, related_name="member_count")
    def __str__(self):
        return self.name
    def member_count(self):
        return self.members_count.count()
    


class RoomMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Folder(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="folders",null=True, blank=True)  # 📁 Folder belongs to Room

    def __str__(self):
        return self.name

from cloudinary.api import resource

class StudyMaterials(models.Model):
    upload_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="myuploads", null=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='study_materials', null=True, blank=True)
    title = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    file = CloudinaryField('file', folder='study_material', null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.room != self.folder.room:
            raise ValueError("The study material's room must match the folder's room.")
        
        # Ensure file is treated as raw resource type if not an image
        if self.file:
            self.file.resource_type = 'raw'
        
        super().save(*args, **kwargs)

    @property
    def file_size_kb(self):
        """Returns the file size in KB."""
        if self.file:
            try:
                # Fetch file metadata from Cloudinary
                metadata = resource(self.file.public_id, resource_type='raw')
                return round(metadata['bytes'] / 1024, 2)  # Convert bytes to KB
            except Exception as e:
                print(f"Error fetching file metadata: {e}")
                return None
        return None
    
    @property
    def file_url(self):
        """Returns the URL for the file."""
        if self.file:
            try:
                # Get a direct URL for the file using Cloudinary's helper function
                url, options = cloudinary.utils.cloudinary_url(self.file.public_id, resource_type='raw')
                return url
            except Exception as e:
                print(f"Error generating file URL: {e}")
        return None

    @property
    def file_type(self):
        """Returns the file extension (type) of the uploaded file."""
        if self.file:
            try:
                # Get the extension from the public_id (cloudinary file name)
                return self.file.public_id.split('.')[-1].upper()
            except IndexError:
                return None  # Handle case when there is no extension
        return None


class ChatBox(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages", null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="groupcreation", null=True)
    group_name = models.CharField(max_length=20,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.group_name or "No-Name"
    
class ChatBoxMembership(models.Model):
    message_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chatbox", null=True)
    chat_box = models.ForeignKey(ChatBox, on_delete=models.CASCADE, related_name="members",null=True)
    content = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f'{self.message_by.username if self.message_by else "Unknown user"} : {self.content or ""}'
    
    class Meta:
        ordering = ['created_at']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_pic = CloudinaryField('image', folder='profile_pic', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rooms = models.ManyToManyField(Room, related_name="profile-rooms+")
    study_materials = models.ManyToManyField(StudyMaterials, related_name="study_materials")
    bio = models.TextField(blank=True, null=True, max_length=100)
    followers = models.ManyToManyField("self", related_name="following", symmetrical=False, blank=True)
    def __str__(self):
        return self.user.username

class Followrequest(models.Model):
    from_user = models.ForeignKey(User, related_name="send_follow_request", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="recieved_follow_request", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"
    

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="activities", null=True, blank=True)
    activity = models.CharField(max_length=50)
    activity_description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity} at {self.timestamp}"
    
class InfoContent(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="info_content", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="info_content_creator", null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class InfoContentUrl(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="info_content_url", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="info_content_url_creator", null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

class CodeFolder(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="code_folders", null=True, blank=True)

    def __str__(self):
        return self.name
    

class CodeSnippet(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='code_snippets')
    folder = models.ForeignKey(CodeFolder, on_delete=models.CASCADE, related_name='code_snippets', null=True, blank=True)
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=50, choices=[
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('c', 'C'),
        ('cpp', 'C++'),
        ('java', 'Java'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('sql', 'SQL'),
        ('php', 'PHP'),
        ('ruby', 'Ruby'),
        ('swift', 'Swift'),
        ('kotlin', 'Kotlin'),
        ('go', 'Go'),
        ('rust', 'Rust'),
        ('typescript', 'TypeScript'),
        ('c#', 'C#'),
        # add more if you want
    ])
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title} ({self.language})"
