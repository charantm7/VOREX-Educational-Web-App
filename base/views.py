from django.shortcuts import render, get_object_or_404, redirect

#models
from .models import Tag, Room, RoomMembership, ChatBox, StudyMaterials, RoomChatIndividual,UserProfile, Followrequest, Folder, ChatBoxMembership, Activity, InfoContent, InfoContentUrl, CodeSnippet, CodeFolder

#auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#forms
from .forms import RoomForm, ProfileForm, UserForm, ChatBoxForm, FolderForm, StudyMaterialForm, ChatBoxMemberForm, InfoContentForm, InfoContentUrlForm, CodeSnippetForm, CodeFolderForm

#django
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def home(request):
    activities = Activity.objects.order_by('-timestamp')[:10]

    if request.user.is_authenticated:
        if request.user.is_superuser:
            room = Room.objects.all().order_by('-created_at')
        else:
            room = Room.objects.filter(
                Q(is_private=False) | Q(members_count=request.user)
            ).distinct().order_by('-created_at')
    else:
        room = Room.objects.filter(
            Q(is_private=False)).order_by('-created_at')
    tag = Tag.objects.all()
    context = {'rooms': room, 'tags': tag, 'activities': activities}
    return render(request, 'base/home.html', context)


@login_required(login_url='User_login')
def rooms(request, room_id):
    
    room = get_object_or_404(Room, id=room_id)
    folder = Folder.objects.filter(room=room)
    members_joined = room.members_count.all()
    profile = get_object_or_404(UserProfile, user=room.created_by)
    group_chat = ChatBox.objects.filter(room=room)
    group_chat_member = ChatBoxMembership.objects.filter(chat_box__in=group_chat)
    code_folder = CodeFolder.objects.filter(room=room)
    info_content = InfoContent.objects.filter(room=room).order_by('-created_at')[:10]
    info_content_url = InfoContentUrl.objects.filter(room=room).order_by('-created_at')[:10]

    # Initialize forms  
    folder_form = FolderForm()
    group_chat_form = ChatBoxForm()
    group_chat_member_form = ChatBoxMemberForm()
    info_content_form = InfoContentForm()
    info_content_url_form = InfoContentUrlForm()
    code_folder_form = CodeFolderForm()

    #get form
    show_info_form = request.GET.get('form') == 'info'
    show_info_url_form = request.GET.get('form') == 'info-url'
    show_code_folder_form = request.GET.get('form') == 'code-folder'

    if request.method == 'POST':
        
        if 'folder_submit' in request.POST:
            folder_form = FolderForm(request.POST)
            if folder_form.is_valid():
                folder_instance = folder_form.save(commit=False)
                folder_instance.created_by = request.user
                folder_instance.room = room
                folder_instance.save()
                return redirect('Rooms', room_id=room_id)
            messages.error(request, 'Invalid Folder Form')

        elif 'group_chat_submit' in request.POST:
            group_chat_form = ChatBoxForm(request.POST)
            if group_chat_form.is_valid():
                chat = group_chat_form.save(commit=False)
                chat.created_by = request.user
                chat.room = room
                chat.save()
                return redirect('Rooms', room_id=room_id)
            messages.error(request, 'Invalid Group Chat Form')

        elif 'group_chat_member_submit' in request.POST:
            group_chat_member_form = ChatBoxMemberForm(request.POST)
            if group_chat_member_form.is_valid():
                group_member = group_chat_member_form.save(commit=False)
                group_member.message_by = request.user
                group_member.chat_box = chat  # Fixed assignment
                group_member.save()
                return redirect('Rooms', room_id=room_id)
            messages.error(request, "Invalid Member Form")

        elif 'info_content_submit' in request.POST:
            info_content_form = InfoContentForm(request.POST)
            if info_content_form.is_valid():
                info_content = info_content_form.save(commit=False)
                info_content.created_by = request.user
                info_content.room = room
                info_content.save()
                return redirect(f"{reverse('Rooms', args=[room_id])}#info-content-form")
            messages.error(request, 'Invalid Info Content Form')

        elif 'info_content_url_submit' in request.POST:
            info_content_url_form = InfoContentUrlForm(request.POST)
            if info_content_url_form.is_valid():
                info_content_url = info_content_url_form.save(commit=False)
                info_content_url.created_by = request.user
                info_content_url.room = room
                info_content_url.save()
                return redirect(f"{reverse('Rooms', args=[room_id])}#info-url-form")
            messages.error(request, 'Invalid Info Content URL Form')

        elif 'code_folder_submit' in request.POST:
            code_folder_form = CodeFolderForm(request.POST)
            if code_folder_form.is_valid():
                code_folder = code_folder_form.save(commit=False)
                code_folder.created_by = request.user
                code_folder.room = room
                code_folder.save()
                return redirect(f"{reverse('Rooms', args=[room_id])}#code-folder-form")
            messages.error(request, 'Invalid Code Folder Form')



    if request.user not in members_joined:
        messages.error(request, "You are not a member of this room! Join to continue.")
        return redirect("Home")



    context = {
        'rooms': room,
        'members': members_joined.count(),
        'profile': profile,
        'folders': folder,
        'form': folder_form,
        'group_chat': group_chat,
        'group_chat_member': group_chat_member,
        'group_chat_form': group_chat_form,
        'group_chat_member_form': group_chat_member_form,
        'show_info_form': show_info_form,
        'info_content_form': info_content_form,
        'info_content_url_form': info_content_url_form,
        'show_info_url_form': show_info_url_form,
        'info_content': info_content,
        'info_content_url': info_content_url,
        'code_folder': code_folder,
        'show_code_folder_form': show_code_folder_form,
        'code_folder_form': code_folder_form,
    }

    return render(request, 'base/room.html', context)



@login_required(login_url='User_login')
def chat(request, room_id, chat_name):
    
    room = get_object_or_404(Room, id=room_id)
    profile = get_object_or_404(UserProfile, user=room.created_by)
    group_chat = ChatBox.objects.filter(room=room)
    group_chat_member = ChatBoxMembership.objects.filter(chat_box__in=group_chat)

   

    search_query = request.GET.get('search', '') 
    users = User.objects.exclude(id=request.user.id) 
    chats = RoomChatIndividual.objects.filter(
        (Q(sender=request.user) & Q(receiver__username=chat_name)) |
        (Q(receiver=request.user) & Q(sender__username=chat_name))
    )

    if search_query:
        chats = chats.filter(Q(content__icontains=search_query))  

    chats = chats.order_by('timestamp') 
    user_last_messages = []

    for user in users:
        last_message = RoomChatIndividual.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()

        user_last_messages.append({
            'user': user,
            'last_message': last_message
        })

    user_last_messages.sort(
    key=lambda x: (x['last_message'] is not None, x['last_message'].timestamp if x['last_message'] else 0),
    reverse=True
)

    return render(request, 'base/chat.html', {
        'rooms':room,
        'room_name': chat_name,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'search_query': search_query 
    })


def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    room = Room.objects.filter(tags=tag)
    context = {'tag': tag, 'rooms': room}
    return render(request, 'base/tags.html', context)


def auth_page(request):
    return render(request, 'base/authentication/auth.html')


def user_signup(request):
    special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?~"
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation checks
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists! Try another username')
        elif len(username) < 3:
            messages.error(request, 'Username must be at least 3 characters long')
        elif len(username) > 15:
            messages.error(request, 'Username must be less than 15 characters')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
        elif len(password) > 20:
            messages.error(request, 'Password must be less than 20 characters')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists! Try another email')
        elif not any(char.isdigit() for char in password):
            messages.error(request, 'Password must contain at least one digit')
        elif not any(char.isupper() for char in password):
            messages.error(request, 'Password must contain at least one uppercase letter')
        elif not any(char.islower() for char in password):
            messages.error(request, 'Password must contain at least one lowercase letter')
        elif not any(char in special_characters for char in password):
            messages.error(request, 'Password must contain at least one special character')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match')
        elif username.lower() == "admin" or password.lower() == "admin":
            messages.error(request, 'Username or password cannot be "admin"')
        elif password == username or password == email:
            messages.error(request, 'Password cannot be the same as username or email')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            user.backend = 'allauth.account.auth_backends.AuthenticationBackend'

            login(request, user, backend=user.backend)

            return redirect('Home') 

        return redirect('User_signup')  

    return render(request, 'base/authentication/signup.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            return redirect('User_login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in')
            return redirect('Home')
        else:
            messages.error(request, 'Invalid password')
            return redirect('User_login')
    return render(request, 'base/authentication/login.html')


@login_required(login_url='User_login')
def user_logout(request):
    logout(request)
    messages.success(request, 'You are logged out')
    return redirect('Home')


@login_required(login_url='User_login')
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            try:
                room = form.save(commit=False)
                room.created_by = request.user
                room.save()
                form.save_m2m()  # Save tags relationship

                room.members_count.add(room.created_by)

                Activity.objects.create(
                    user=request.user,
                    activity=f"created a room '{room.name}'",
                    room=room
                )
                return redirect('Home')
            except Exception as e:
                messages.error(request, f'Error creating room: {str(e)}')
                return redirect('Create-room')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('Create-room')
    else:
        form = RoomForm()
    context = {'form': form}
    return render(request, 'base/createroom.html', context)


def edit_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Home')
        else:
            messages.error(request, 'Invalid form')
    else:
        form = RoomForm(instance=room)
    context = {'form': form}
    return render(request, 'base/editroom.html', context)


def delete_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    room.delete()
    messages.success(request, 'Room deleted successfully')
    return redirect('Home')


def join_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    if request.user in room.members_count.all():
        messages.error(request, 'You are already a member of this room')
        return redirect('Rooms', room_name=room_name)
    else:
        room.members_count.add(request.user)
        room.save()
        messages.success(request, 'You are now a member of this room')
        return redirect('Rooms', room_name=room_name)


def exit_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    room.members_count.remove(request.user)
    messages.success(request, 'Exited from the room successfully')
    return redirect('Home')


@login_required(login_url='User_login')
def profile(request, user_tag):
    user = User.objects.get(username=user_tag)
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            room = Room.objects.filter(created_by=user)
        elif request.user == user:
            room = Room.objects.filter(created_by=user)
        else:
            room = Room.objects.filter(is_private=False,created_by=user)

    if not UserProfile.objects.filter(user=user).exists():
        UserProfile.objects.create(user=user)
        profile = UserProfile.objects.get(user=user)
    else:
        profile = UserProfile.objects.get(user=user)

    if request.user.is_authenticated:
        is_follower = user.profile in request.user.profile.followers.all()

    send_follow_request = Followrequest.objects.filter(from_user=request.user).values_list('to_user__id', flat=True)
    context = {'user': user, 'room': room, 'profile': profile,'is_follower':is_follower,'send_follow_request':send_follow_request}
    return render(request, 'base/profile.html', context)


@login_required(login_url='User_login')
def profile_update(request, user_tag):
    user = User.objects.get(username=user_tag)
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('Profile', user_tag=user_tag)
        else:
            messages.error(request, 'Invalid form')

    else:   
        form = ProfileForm(instance=profile)

    context = {'form': form, 'profile': profile}
    return render(request, 'base/updateprofile.html', context)


@login_required(login_url='User_login')
def user_update(request, user_tag):
    user = User.objects.get(username=user_tag)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            updated_user = form.save()
            updated_user.save()
            messages.success(request, 'User updated successfully')
            return redirect('Profile', user_tag=updated_user.username)

        else:
            messages.error(request, 'Invalid form')
    else:
        form = UserForm(instance=user)
    context = {'form': form}
    return render(request, 'base/updateuser.html', context)


def room_member_count(request, room_tag):
    room = get_object_or_404(Room, name=room_tag)
    members = room.members_count.all()
    context = {'room':room,'members':members}
    return render(request, 'base/room_members.html', context)

@login_required(login_url='User_login')
def send_follow_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if Followrequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        return redirect('Profile', user_tag=to_user.username)
    request = Followrequest.objects.create(from_user=request.user, to_user=to_user)
    request.save()
    return redirect('Profile', user_tag=to_user.username)


def unfollow_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    to_user_profile = to_user.profile

    if request.user.is_authenticated:
        current_user = request.user.profile
    
        if current_user in to_user_profile.followers.all():
            to_user_profile.followers.remove(current_user)
            return JsonResponse({'success': True, 'message': 'Unfollowed successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'You are not following this user.'})
    return redirect('Profile', user_tag=to_user.username)

@login_required(login_url='User_login')
def accept_follow_request(request, request_id):
    followrequest = get_object_or_404(Followrequest, id=request_id , to_user=request.user)
    request.user.profile.followers.add(followrequest.from_user.profile  )
    followrequest.from_user.profile.followers.add(request.user.profile)
    followrequest.delete()
    return redirect('Profile', user_tag=request.user.username)


@login_required(login_url='User_login')
def reject_follow_request(request, request_id):
    follow_request = Followrequest.objects.filter(id=request_id, to_user=request.user).first() # Replace with an actual error page
    if follow_request:
        # If the follow request exists, delete it
        follow_request.delete()
        return redirect('Profile', user_tag=request.user.username)
    return redirect('Profile', user_tag=request.user.username)

def followers_list(request, user_tag):
    user = get_object_or_404(User, username=user_tag)
    followers = user.profile.followers.all()
    context = {'followers': followers}
    return render(request, 'base/follower_list.html', context)

def following_list(request, user_tag):
    user = get_object_or_404(User, username=user_tag)
    following = user.following.all()
    return render(request, 'base/follower_list.html', {'following': following})
    
def follow_request(request, user_tag):
    user = get_object_or_404(User, username=user_tag)
    follow_request = Followrequest.objects.filter(to_user=request.user)
    context = {'user': user, 'follow_request': follow_request}
    return render(request, 'base/follow_request.html', context)

def error_404(request):
    return render(request, 'base/error_page.html')

def chat_view(request, room_id):
    room = Room.objects.get(id=room_id)
    messages = ChatBox.objects.filter(room=room).order_by('created_at')

    if request.method == 'POST':
        form = ChatBoxForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.user = request.user
            chat_message.room = room
            chat_message.save()
            return redirect('chat_view', room_id=room_id)
    else:
        form = ChatBoxForm()

    return render(request, 'base/room.html', {'room': room, 'messages': messages, 'form': form})
    
def files_in_folder(request, room_id, f_name):
    room = get_object_or_404(Room, id=room_id)
    folder = get_object_or_404(Folder, name=f_name, room=room)
    study_materials = StudyMaterials.objects.filter(folder=folder)
    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form= form.save(commit=False)
            form.upload_by = request.user
            form.folder = folder
            form.room = folder.room
            form.save()
            return redirect('Folder', room_id=room_id, f_name=f_name)
        else:   
            messages.error(request, 'Invalid form')
            return redirect('Folder', room_id=room_id, f_name=f_name)
        
    else:
        form = StudyMaterialForm()
    context = { 'form': form, 'study_materials': study_materials, 'folder': folder, 'room': room}
    return render(request, 'base/files_in_folder.html', context)

def delete_file(request, file_id, room_id, f_name):
    room = get_object_or_404(Room, id=room_id)
    folder = get_object_or_404(Folder, name=f_name, room=room)
    study_materials = get_object_or_404(StudyMaterials,folder=folder, pk=file_id)
    study_materials.delete()
    return redirect("Folder", room_id=room_id, f_name=f_name)


def delete_folder(request, room_id, f_name):

    room = get_object_or_404(Room, id=room_id)
    folder = get_object_or_404(Folder, name=f_name, room=room)
    folder.delete()
    return redirect('Rooms', room_id=room_id)

def delete_group(request, room_id, g_name):
    room = get_object_or_404(Room, id=room_id)
    chat_box = get_object_or_404(ChatBox,group_name=g_name, room=room )
    chat_box.delete()
    return redirect('Rooms',room_id=room_id)



# your rooms and joined rooms views
def your_room(request, user_name):
    user = User.objects.get(username=user_name)
    room = Room.objects.filter(created_by=user)

    context = {
        'user': user,
        'rooms': room,
    }

    return render(request, 'base/your_room.html', context)

def joined_room(request):
    rooms = Room.objects.all()
    member = Room.objects.filter(members_count=request.user.id)
    joined_room = member.exists()
    context = {
        'rooms': rooms,
        'joined_room': joined_room,
        'member':member,
        
    }
    return render(request, 'base/joined_room.html', context)


#dashboard
@login_required(login_url='User_login')
def dashboard(request):
    room = Room.objects.all()
    context = {
        'rooms':room
    }

    return render(request, 'base/dashboard.html',context)

def user_dashboard(request):
    user = UserProfile.objects.all()
       
    context = {
        'users': user,
        
    }
    return render(request, 'base/user_dashboard.html', context)

def study_material_dashboard(request):
    return render(request, 'base/study_material_dashboard.html')


# Oauth 
def google_login_redirect(request):
    return redirect("/accounts/google/login/")

def search_tags(request):
    search = request.GET.get('search', '')
    logger.debug(f"Searching tags with term: {search}")
    
    if search:
        tags = Tag.objects.filter(name__icontains=search)
    else:
        tags = Tag.objects.all()
    
    results = [{'id': tag.id, 'text': tag.name} for tag in tags[:10]]
    logger.debug(f"Found tags: {results}")
    return JsonResponse({'results': results})

def debug_tags(request):
    tags = Tag.objects.all()
    return JsonResponse({'tags': list(tags.values('id', 'name'))})



def code_in_folder(request, room_id, folder_name):
    room = get_object_or_404(Room, id=room_id)
    folder = get_object_or_404(CodeFolder, name=folder_name, room=room)
    code_snippets = CodeSnippet.objects.filter(folder=folder)

    form = CodeSnippetForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.folder = folder
            snippet.room = room
            snippet.uploaded_by = request.user
            snippet.save()
            messages.success(request, "Code snippet uploaded!")
            return redirect('code-folder', room_id=room_id, folder_name=folder_name)
        else:
            messages.error(request, "Invalid form")

    return render(request, 'base/code_snippet.html', {
        'code_snippets': code_snippets,
        'folder': folder,
        'form': form,
        'room': room
    })




