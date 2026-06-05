from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils import timezone
from django.views.decorators.http import require_POST

from exhibitions.models import Exhibition

from .forms import CameraForm, CameraReviewForm
from .models import Camera, CameraReview


RECENT_EXHIBITIONS_SESSION_KEY = 'recent_exhibitions'
HOME_RECENT_EXHIBITIONS_LIMIT = 3


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def form_errors_as_text(form):
    return form.errors.as_text() or 'Проверьте заполнение формы.'


def get_recent_exhibitions_for_home(request):
    recent_ids = request.session.get(RECENT_EXHIBITIONS_SESSION_KEY, [])

    if not recent_ids:
        return []

    recent_ids = [int(exhibition_id) for exhibition_id in recent_ids]
    recent_ids = recent_ids[:HOME_RECENT_EXHIBITIONS_LIMIT]

    exhibitions = (
        Exhibition.objects
        .select_related('curator')
        .prefetch_related('photos')
        .filter(id__in=recent_ids)
    )

    exhibitions_by_id = {
        exhibition.id: exhibition
        for exhibition in exhibitions
    }

    return [
        exhibitions_by_id[exhibition_id]
        for exhibition_id in recent_ids
        if exhibition_id in exhibitions_by_id
    ]


def home_page(request):
    recent_exhibitions = get_recent_exhibitions_for_home(request)

    context = {
        'recent_exhibitions': recent_exhibitions,
    }

    return render(request, 'cameras/home.html', context)


def toggle_theme(request):
    current_theme = request.COOKIES.get('theme', 'light')

    if current_theme == 'dark':
        new_theme = 'light'
    else:
        new_theme = 'dark'

    next_url = request.META.get('HTTP_REFERER')

    if not next_url or not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure()
    ):
        next_url = reverse('cameras:home')

    response = redirect(next_url)

    response.set_cookie(
        key='theme',
        value=new_theme,
        max_age=60 * 60 * 24 * 365,
        samesite='Lax'
    )

    return response


def camera_list(request):
    cameras = (
        Camera.objects
        .select_related('brand', 'owner')
        .order_by('id')
    )

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
        form = CameraForm(request.POST, request.FILES)

        if form.is_valid():
            camera = form.save(commit=False)
            camera.owner = request.user
            camera.save()

            form.save_image(camera)

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
        form = CameraForm(request.POST, request.FILES, instance=camera)

        if form.is_valid():
            camera = form.save()
            form.save_image(camera)

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