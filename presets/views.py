from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import PresetReviewForm
from .models import Preset


def preset_list(request):
    presets = Preset.objects.all()

    context = {
        'presets': presets,
    }

    return render(request, 'presets/list.html', context)


def preset_detail(request, preset_id):
    preset = get_object_or_404(Preset.objects.select_related('author'), id=preset_id)
    reviews = preset.reviews.filter(is_visible=True)

    if request.method == 'POST':
        form = PresetReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.preset = preset
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

            return redirect('presets:preset_detail', preset_id=preset.id)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'errors': form.errors.as_text()
            }, status=400)

    else:
        form = PresetReviewForm()

    context = {
        'preset': preset,
        'reviews': reviews,
        'form': form,
    }

    return render(request, 'presets/detail.html', context)