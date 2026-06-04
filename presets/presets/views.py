from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import PresetForm, PresetReviewForm
from .models import Preset, PresetReview


def preset_list(request):
    presets = Preset.objects.select_related('author').all()

    context = {
        'presets': presets,
    }

    return render(request, 'presets/list.html', context)


def preset_detail(request, preset_id):
    preset = get_object_or_404(
        Preset.objects.select_related('author'),
        id=preset_id
    )
    reviews = preset.reviews.filter(is_visible=True).select_related('author')
    form = PresetReviewForm()

    context = {
        'preset': preset,
        'reviews': reviews,
        'form': form,
    }

    return render(request, 'presets/detail.html', context)


@login_required
def preset_create(request):
    if request.method == 'POST':
        form = PresetForm(request.POST)

        if form.is_valid():
            preset = form.save(commit=False)
            preset.author = request.user
            preset.save()

            return redirect('presets:preset_detail', preset_id=preset.id)
    else:
        form = PresetForm()

    context = {
        'form': form,
        'title': 'Добавить пресет',
        'button_text': 'Сохранить пресет',
    }

    return render(request, 'presets/form.html', context)


@login_required
def preset_edit(request, preset_id):
    preset = get_object_or_404(
        Preset,
        id=preset_id,
        author=request.user
    )

    if request.method == 'POST':
        form = PresetForm(request.POST, instance=preset)

        if form.is_valid():
            form.save()
            return redirect('presets:preset_detail', preset_id=preset.id)
    else:
        form = PresetForm(instance=preset)

    context = {
        'form': form,
        'preset': preset,
        'title': 'Редактировать пресет',
        'button_text': 'Сохранить изменения',
    }

    return render(request, 'presets/form.html', context)


@login_required
def preset_delete(request, preset_id):
    preset = get_object_or_404(
        Preset,
        id=preset_id,
        author=request.user
    )

    if request.method == 'POST':
        preset.delete()
        return redirect('presets:preset_list')

    context = {
        'preset': preset,
    }

    return render(request, 'presets/confirm_delete.html', context)


@login_required
@require_POST
def add_preset_review(request, preset_id):
    preset = get_object_or_404(Preset, id=preset_id)
    form = PresetReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.preset = preset
        review.author = request.user
        review.author_name = request.user.username
        review.rating = 5
        review.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'comment': {
                    'author_name': review.author_name,
                    'text': review.text,
                    'created_at': timezone.localtime(review.created_at).strftime('%d.%m.%Y %H:%M'),
                    'edit_url': reverse('presets:edit_preset_review', args=[review.id]),
                    'delete_url': reverse('presets:delete_preset_review', args=[review.id]),
                }
            })

        return redirect('presets:preset_detail', preset_id=preset.id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'errors': form.errors.as_text()
        }, status=400)

    context = {
        'preset': preset,
        'reviews': preset.reviews.filter(is_visible=True).select_related('author'),
        'form': form,
    }

    return render(request, 'presets/detail.html', context)


@login_required
def edit_preset_review(request, review_id):
    review = get_object_or_404(
        PresetReview.objects.select_related('preset'),
        id=review_id,
        author=request.user
    )

    if request.method == 'POST':
        form = PresetReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            return redirect('presets:preset_detail', preset_id=review.preset.id)
    else:
        form = PresetReviewForm(instance=review)

    context = {
        'review': review,
        'form': form,
    }

    return render(request, 'presets/review_form.html', context)


@login_required
def delete_preset_review(request, review_id):
    review = get_object_or_404(
        PresetReview.objects.select_related('preset'),
        id=review_id,
        author=request.user
    )

    if request.method == 'POST':
        preset_id = review.preset.id
        review.delete()
        return redirect('presets:preset_detail', preset_id=preset_id)

    context = {
        'review': review,
    }

    return render(request, 'presets/review_confirm_delete.html', context)