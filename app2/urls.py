from django.urls import path
from .views import file_manager_view, get_folder_contents, create_folder, upload_file, test_ui

urlpatterns = [
    path('file-manager/', file_manager_view, name='file_manager'),
    # path('file-manager/<path:path>/', file_management_view, name='file_manager_folder'),
    path('get-folder-contents/', get_folder_contents, name='get_folder_contents'),
    path('create-folder/', create_folder, name='create_folder'),
    path('upload-file/', upload_file, name='upload_file'),
    
    
    path('test/', test_ui),
]
