from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CameraReviewForm
from .models import Camera


def home_page(request):
    return render(request, 'cameras/home.html')


def camera_list(request):
    cameras = Camera.objects.all()

    context = {
        'cameras': cameras,
    }

    return render(request, 'cameras/list.html', context)


def camera_detail(request, camera_id):
    camera = get_object_or_404(Camera.objects.select_related('brand'), id=camera_id)
    reviews = camera.reviews.filter(is_visible=True).select_related('author')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'errors': 'Чтобы оставить комментарий, нужно войти в аккаунт.'
                }, status=403)

            return redirect('accounts:login')

        form = CameraReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.camera = camera
            review.author = request.user
            review.author_name = request.user.username
            review.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'comment': {
                        'author_name': review.author_name,
                        'text': review.text,
                        'rating': review.rating,
                        'created_at': timezone.localtime(review.created_at).strftime('%d.%m.%Y %H:%M'),
                    }
                })

            return redirect('cameras:camera_detail', camera_id=camera.id)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'errors': form.errors.as_text()
            }, status=400)

    else:
        form = CameraReviewForm()

    context = {
        'camera': camera,
        'reviews': reviews,
        'form': form,
    }

    return render(request, 'cameras/detail.html', context)