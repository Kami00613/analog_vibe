from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CameraForm, CameraReviewForm
from .models import Camera, CameraReview


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def form_errors_as_text(form):
    return form.errors.as_text() or 'Проверьте заполнение формы.'


def home_page(request):
    return render(request, 'cameras/home.html')


def camera_list(request):
    cameras = Camera.objects.select_related('brand', 'owner').all()

    context = {
        'cameras': cameras,
    }

    return render(request, 'cameras/list.html', context)


def camera_detail(request, camera_id):
    camera = get_object_or_404(
        Camera.objects.select_related('brand', 'owner'),
        id=camera_id
    )
    reviews = camera.reviews.filter(is_visible=True).select_related('author')
    form = CameraReviewForm()

    context = {
        'camera': camera,
        'reviews': reviews,
        'form': form,
    }

    return render(request, 'cameras/detail.html', context)


@login_required
def camera_create(request):
    if request.method == 'POST':
        form = CameraForm(request.POST)

        if form.is_valid():
            camera = form.save(commit=False)
            camera.owner = request.user
            camera.save()

            return redirect('cameras:camera_detail', camera_id=camera.id)
    else:
        form = CameraForm()

    context = {
        'form': form,
        'title': 'Добавить камеру',
        'button_text': 'Сохранить камеру',
    }

    return render(request, 'cameras/form.html', context)


@login_required
def camera_edit(request, camera_id):
    camera = get_object_or_404(
        Camera,
        id=camera_id,
        owner=request.user
    )

    if request.method == 'POST':
        form = CameraForm(request.POST, instance=camera)

        if form.is_valid():
            form.save()
            return redirect('cameras:camera_detail', camera_id=camera.id)
    else:
        form = CameraForm(instance=camera)

    context = {
        'form': form,
        'camera': camera,
        'title': 'Редактировать камеру',
        'button_text': 'Сохранить изменения',
    }

    return render(request, 'cameras/form.html', context)


@login_required
def camera_delete(request, camera_id):
    camera = get_object_or_404(
        Camera,
        id=camera_id,
        owner=request.user
    )

    if request.method == 'POST':
        camera.delete()

        if is_ajax(request):
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('cameras:camera_list'),
            })

        return redirect('cameras:camera_list')

    context = {
        'camera': camera,
    }

    return render(request, 'cameras/confirm_delete.html', context)


@login_required
@require_POST
def add_camera_review(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    form = CameraReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.camera = camera
        review.author = request.user
        review.author_name = request.user.username
        review.rating = 5
        review.save()

        if is_ajax(request):
            return JsonResponse({
                'comment': {
                    'id': review.id,
                    'author_name': review.author_name,
                    'text': review.text,
                    'created_at': timezone.localtime(review.created_at).strftime('%d.%m.%Y %H:%M'),
                    'edit_url': reverse('cameras:edit_camera_review', args=[review.id]),
                    'delete_url': reverse('cameras:delete_camera_review', args=[review.id]),
                }
            })

        return redirect('cameras:camera_detail', camera_id=camera.id)

    if is_ajax(request):
        return JsonResponse({
            'errors': form_errors_as_text(form)
        }, status=400)

    context = {
        'camera': camera,
        'reviews': camera.reviews.filter(is_visible=True).select_related('author'),
        'form': form,
    }

    return render(request, 'cameras/detail.html', context)


@login_required
def edit_camera_review(request, review_id):
    review = get_object_or_404(
        CameraReview.objects.select_related('camera'),
        id=review_id,
        author=request.user
    )

    if request.method == 'POST':
        form = CameraReviewForm(request.POST, instance=review)

        if form.is_valid():
            review = form.save()

            if is_ajax(request):
                return JsonResponse({
                    'success': True,
                    'text': review.text,
                })

            return redirect('cameras:camera_detail', camera_id=review.camera.id)

        if is_ajax(request):
            return JsonResponse({
                'success': False,
                'errors': form_errors_as_text(form),
            }, status=400)
    else:
        form = CameraReviewForm(instance=review)

    context = {
        'review': review,
        'form': form,
    }

    return render(request, 'cameras/review_form.html', context)


@login_required
def delete_camera_review(request, review_id):
    review = get_object_or_404(
        CameraReview.objects.select_related('camera'),
        id=review_id,
        author=request.user
    )

    if request.method == 'POST':
        camera_id = review.camera.id
        review.delete()

        if is_ajax(request):
            return JsonResponse({'success': True})

        return redirect('cameras:camera_detail', camera_id=camera_id)

    context = {
        'review': review,
    }

    return render(request, 'cameras/review_confirm_delete.html', context)
