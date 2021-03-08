from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import PhotoForm
from .models import Photo

def index(request):
    template = loader.get_template('carbike/index.html')
    context = {'form': PhotoForm()}
    return HttpResponse(template.render(context, request))

def inferencer(request):
    if not request.method == 'POST':
        return
        redirect('carbike:index')
    print(request.POST)
    print(request.FILES)
    form = PhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        raise ValueError('Formが不正です')

    
    if form.cleaned_data['image'] == None and form.cleaned_data['scraping'] == None:
        raise ValueError('Formが不正です')
    elif form.cleaned_data['image'] != None and form.cleaned_data['scraping'] == None:
        photo = Photo(image=form.cleaned_data['image'])
    elif form.cleaned_data['image'] == None and form.cleaned_data['scraping'] != None:
        photo = Photo(scraping_word=form.cleaned_data['scraping']).scraping()
    else:
        photo = Photo(image=form.cleaned_data['image'])

    style = form.cleaned_data['style']
    result = photo.inference(int(style) - 1)

    style_img = photo.style_image_src(int(style))

    template = loader.get_template('carbike/result.html')

    context = {
        'photo_name': photo.image.name,
        'photo_data': photo.image_src(),
        'result': result,
        'style': style_img,
    }

    return HttpResponse(template.render(context, request))

