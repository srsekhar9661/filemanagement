import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string



global media_root, media_url

media_root = settings.MEDIA_ROOT
media_url = settings.MEDIA_URL

# Reminder of the view function
def file_manager_view(request):
    path = request.GET.get('path', '')
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    current_path = os.path.join(media_root, path)

    # Get folders and files
    folders = []
    files = []

    if os.path.exists(current_path):
        for item in os.listdir(current_path):
            item_path = os.path.join(path, item)
            if os.path.isdir(os.path.join(media_root, item_path)):
                folders.append(item_path)
            else:
                file_name = item_path.split('/')[-1]
                files.append({'file_path':item_path, 'file_name':file_name})

    # Generate breadcrumbs
    breadcrumbs = []
    if path:
        parts = path.split('/')
        for i, part in enumerate(parts):
            breadcrumbs.append({
                'name': part,
                'url': '/file-manager/?path=' + '/'.join(parts[:i+1])
            })

    context = {
        'current_path': path,
        'folders': folders,
        'files': files,
        'MEDIA_URL': media_url,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'app2/file_manager.html', context)



from django.http import JsonResponse
import os

def get_folder_contents(request):
    # import ipdb;ipdb.set_trace(context=9)
    original_path = path = request.GET.get('path')
    print(f"path ============= : {path}")
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    
    # Ensure the original_path is relative
    if os.path.isabs(original_path):
        # Remove leading slashes or backslashes
        path = original_path.lstrip('/\\')
    
    path = os.path.join(media_root, path)
    # List directories and files in the specified path
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    # files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            # file_url = os.path.join(settings.MEDIA_URL, path)
            file_path = f"{original_path}/{file}"
            file_name = file_path.split('/')[-1]
            files.append({
                'file_path' : file_path,
                'file_name' : file_name
            })
            print(f"File url ======== {original_path}/{file}")
    # Create the response data
    response_data = {
        'current_path': original_path,
        'folders': folders,
        'files': files,
        'MEDIA_URL':media_url
    }
    
    return JsonResponse(response_data)


from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

from django.http import JsonResponse
import os

def create_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        current_path = request.POST.get('current_path').lstrip('/')  # Remove leading slash if present
        
        # Construct the new folder path
        new_folder_path = os.path.join(media_root, current_path, folder_name)
        # import ipdb;ipdb.set_trace(context=9)
        try:
            os.makedirs(new_folder_path)  # Create the folder
            print(f"new folder path =============== {new_folder_path}")
            return JsonResponse({
                'success': True,
                'new_folder_path': new_folder_path
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)



from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        upload_path = request.POST.get('upload_path', '')
        
        # Check if file and upload_path are present
        if file is None or upload_path is None:
            return JsonResponse({'error': 'No file or path specified'}, status=400)
        
        # Ensure upload_path is within MEDIA_ROOT   
        safe_path = os.path.join(settings.MEDIA_ROOT, upload_path.lstrip('/'))
        safe_path = os.path.normpath(safe_path)
        # if not safe_path.startswith(os.path.join(settings.MEDIA_ROOT, 'uploads')):
        #     return JsonResponse({'error': 'Invalid path'}, status=400)
        
        print(f"safe_path === {safe_path}")
        # Save the file
        file_path = default_storage.save(os.path.join(safe_path, file.name), file)
        print('=========')
        print(file_path)

        # Return a response with the file URL and name
        return JsonResponse({
            'file_url': default_storage.url(file_path),
            'file_name': file.name
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def test_ui(request):
    return render(request, 'app2/files_list.html')