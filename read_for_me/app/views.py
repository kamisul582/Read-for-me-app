from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import FileUploadForm
import pytesseract
from PIL import Image

def home(request):
    return redirect('pages:upload_file')


def get_text_form_image(file):
    img = Image.open(file)
    text = pytesseract.image_to_string(img)
    print(text)
    return text

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        file_extension = uploaded_file.name.split('.')[-1].lower()
        form = FileUploadForm(request.POST, request.FILES)
        print(file_extension)
        if form.is_valid():
            get_text_form_image(uploaded_file)
            return render(request, 'pages/file_upload.html', {'form': form, 'message': text})
        return render(request, 'pages/file_upload.html', {'form': form,'message':"not valid"})
        
    else:
        form = FileUploadForm()
        return render(request, 'pages/file_upload.html', {'form': form})

