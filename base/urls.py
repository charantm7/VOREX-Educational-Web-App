from django.urls import path, re_path, include
from . import views


urlpatterns = [
    # home pattern
    path('',views.home, name='Home'),
    
    # room pattern
    path('rooms/<int:room_id>/',views.rooms, name='Rooms'),
    
    # chat pattern
    path('chat/<int:room_id>/',views.chat, name='chat'),

    # your rooms and joined rooms
    path("your-rooms/<str:user_name>/",views.your_room, name='Your-Room'),
    path('joined-room/',views.joined_room, name='Joined-Room'),
    path('dashboard/',views.dashboard, name='Dashboard'),
    path('user-dashboard/',views.user_dashboard, name='User-dashboard'),
    path('study-materials-dashboard/',views.study_material_dashboard, name='Study-dashboard'),

    #sidebar
    path('about/', views.about, name='About'),
    path('service/', views.service, name='Service'),
    
    # authentication
    path('authentication/',views.auth_page, name='auth_page'),
    path('user_login/',views.user_login, name='User_login'),
    path('user_signup/',views.user_signup, name='User_signup'),
    path('user_logout/',views.user_logout, name='User_logout'),

    # profile section
    path('profile/<str:user_tag>/',views.profile, name='Profile'),
    path('update_user/<str:user_tag>/',views.user_update, name='Update-user'),
    path('update_profile/<str:user_tag>/',views.profile_update, name='Update-profile'),
    
    # creation, deletion and edition
    path('create_room/',views.create_room, name='Create-room'),
    path('edit_room/<int:room_id>/',views.edit_room, name='Edit-room'),
    path('delete_room/<int:room_id>/',views.delete_room, name='Delete-room'),
    path('<str:tag_name>/',views.tag, name='Tag'),
    
    # join and exit 
    path('join_room/<int:room_id>/',views.join_room, name='Join-room'),
    path('exit_room/<int:room_id>/',views.exit_room, name='Exit-room'),
    path('room-members/<str:room_tag>/',views.room_member_count, name='Room-members'),

    # follow and unfollow concept
    path('send-follow-request/<int:user_id>/', views.send_follow_request, name='send-follow-request'),
    path('unfollow-/<str:user_id>/', views.unfollow_request, name='Unfollow'),
    path('accept-follow-request/<int:request_id>/', views.accept_follow_request, name='accept-follow-request'),
    path('decline-follow-request/<int:request_id>/', views.reject_follow_request, name='decline-follow-request'),
    path('followers/<str:user_tag>/', views.followers_list, name='followers-list'),
    path('following/<str:user_tag>/', views.following_list, name='following-list'),
    path('follow-request/<str:user_tag>', views.follow_request, name='follow-request'),
    path('404-error/',views.error_404, name='Error-page'),

    # folder creation, deletion
    path('create-folder/<int:room_id>/',views.rooms, name='Create-folder'),
    path('folder/<int:room_id>/<str:f_name>/',views.files_in_folder, name='Folder'),
    path('delete-folder/<int:room_id>/<str:f_name>/',views.delete_folder,name='Delete-folder'),

    # file upload and deletion
    path('upload-file/<int:room_id>/<str:f_name>/',views.files_in_folder, name='Upload-file'),
    path('delete-file/<int:room_id>/<str:f_name>/<str:file_id>',views.delete_file, name='Delete-file'),

    # Oauth authentication url
    path("accounts/login/", views.google_login_redirect),  # Redirect login page to Google
    path("accounts/signup/", views.google_login_redirect),

    #Code snippet upload url
    path('code-snippet/<int:room_id>/<str:folder_name>/', views.code_in_folder, name='code-snippet'),
 
    #Code folder url
    path('room/<int:room_id>/code-folder/<str:folder_name>/', views.code_in_folder, name='code-folder'),

    #Code snippet deletion url
    path('delete-code-snippet/<int:room_id>/<str:folder_name>/<str:code_snippet_id>/', views.delete_code_snippet, name='delete-code-snippet'),

    #Code snippet edition url
    path('edit-code-snippet/<int:room_id>/<str:folder_name>/<str:code_snippet_id>/', views.edit_code_snippet, name='edit-code-snippet'),

    #Code folder deletion url
    path('delete-code-folder/<int:room_id>/<str:folder_name>/', views.delete_code_folder, name='delete-code-folder'),

    #Code snippet upload url
    path('upload-code/<int:room_id>/<str:folder_name>/', views.upload_code, name='upload-code'),

    

    
 

]

