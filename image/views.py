from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm
from .models import Image
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

@login_required(login_url="account/login")
@csrf_exempt
@require_POST
def upload_image(request):
    form = ImageForm(data=request.POST)
    print(request.POST['url'])
    if form.is_valid():
        try:
            new_item=form.save(commit=False)
            new_item.user=request.user
            new_item.save()
            return JsonResponse({'status':"1"})
        except:
            return JsonResponse({"status":"0"})
    else:
        return JsonResponse({"status":"2"})

@login_required(login_url='account/login')
def list_images(request):
    image_list=Image.objects.filter(user=request.user)
    paginator = Paginator(image_list,4)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        images = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        images = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        images = current_page.object_list
    return render(request,'image/list_images.html',{"images":images,"page":current_page})

@login_required(login_url='account/login')
@csrf_exempt
@require_POST
def del_image(request):
    image_id=request.POST['image_id']
    try:
        image = Image.objects.get(id=image_id)
        image.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

def fall_images(request):
    image_list = Image.objects.all()
    paginator = Paginator(image_list,10)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        images = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        images = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        images = current_page.object_list
    return render(request,'image/fall_images.html',{"images":images,"page":current_page})