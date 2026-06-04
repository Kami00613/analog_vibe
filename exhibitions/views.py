from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import ExhibitionForm, ExhibitionReviewForm
from .models import Exhibition, ExhibitionReview


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def form_errors_as_text(form):
    return form.errors.as_text() or 'Проверьте заполнение формы.'


def exhibition_list(request):
    exhibitions = Exhibition.objects.select_related('curator').all()

    context = {
        'exhibitions': exhibitions,
    }

    return render(request, 'exhibitions/list.html', context)


def exhibition_detail(request, exhibition_id):
    exhibition = get_object_or_404(
        Exhibition.objects.select_related('curator'),
        id=exhibition_id
    )

    reviews = exhibition.reviews.filter(is_visible=True).select_related('author')
    form = ExhibitionReviewForm()

    context = {
        'exhibition': exhibition,
        'reviews': reviews,
        'form': form,
    }

    return render(request, 'exhibitions/detail.html', context)


@login_required
def exhibition_create(request):
    if request.method == 'POST':
        form = ExhibitionForm(request.POST)

        if form.is_valid():
            exhibition = form.save(commit=False)
            exhibition.curator = request.user
            exhibition.is_published = True
            exhibition.save()

            return redirect('exhibitions:exhibition_detail', exhibition_id=exhibition.id)
    else:
        form = ExhibitionForm()

    context = {
        'form': form,
        'title': 'Добавить выставку',
        'button_text': 'Сохранить выставку',
    }

    return render(request, 'exhibitions/form.html', context)


@login_required
def exhibition_edit(request, exhibition_id):
    exhibition = get_object_or_404(
        Exhibition,
        id=exhibition_id,
        curator=request.user
    )

    if request.method == 'POST':
        form = ExhibitionForm(request.POST, instance=exhibition)

        if form.is_valid():
            exhibition = form.save(commit=False)
            exhibition.is_published = True
            exhibition.save()

            return redirect('exhibitions:exhibition_detail', exhibition_id=exhibition.id)
    else:
        form = ExhibitionForm(instance=exhibition)

    context = {
        'form': form,
        'exhibition': exhibition,
        'title': 'Редактировать выставку',
        'button_text': 'Сохранить изменения',
    }

    return render(request, 'exhibitions/form.html', context)


@login_required
def exhibition_delete(request, exhibition_id):
    exhibition = get_object_or_404(
        Exhibition,
        id=exhibition_id,
        curator=request.user
    )

    if request.method == 'POST':
        exhibition.delete()

        if is_ajax(request):
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('exhibitions:exhibition_list'),
            })

        return redirect('exhibitions:exhibition_list')

    context = {
        'exhibition': exhibition,
    }

    return render(request, 'exhibitions/confirm_delete.html', context)


@login_required
@require_POST
def add_exhibition_review(request, exhibition_id):
    exhibition = get_object_or_404(Exhibition, id=exhibition_id)
    form = ExhibitionReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.exhibition = exhibition
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
                    'edit_url': reverse('exhibitions:edit_exhibition_review', args=[review.id]),
                    'delete_url': reverse('exhibitions:delete_exhibition_review', args=[review.id]),
                }
            })

        return redirect('exhibitions:exhibition_detail', exhibition_id=exhibition.id)

    if is_ajax(request):
        return JsonResponse({
            'errors': form_errors_as_text(form)
        }, status=400)

    context = {
        'exhibition': exhibition,
        'reviews': exhibition.reviews.filter(is_visible=True).select_related('author'),
        'form': form,
    }

    return render(request, 'exhibitions/detail.html', context)


@login_required
def edit_exhibition_review(request, review_id):
    review = get_object_or_404(
        ExhibitionReview.objects.select_related('exhibition'),
        id=review_id,
        author=request.user
    )

    if request.method == 'POST':
        form = ExhibitionReviewForm(request.POST, instance=review)

        if form.is_valid():
            review = form.save(commit=False)
            review.rating = 5
            review.save()

            if is_ajax(request):
                return JsonResponse({
                    'success': True,
                    'text': review.text,
                })

            return redirect('exhibitions:exhibition_detail', exhibition_id=review.exhibition.id)

        if is_ajax(request):
            return JsonResponse({
                'success': False,
                'errors': form_errors_as_text(form),
            }, status=400)
    else:
        form = ExhibitionReviewForm(instance=review)

    context = {
        'review': review,
        'form': form,
    }

    return render(request, 'exhibitions/review_form.html', context)


@login_required
def delete_exhibition_review(request, review_id):
    review = get_object_or_404(
        ExhibitionReview.objects.select_related('exhibition'),
        id=review_id,
        author=request.user
    )

    if request.method == 'POST':
        exhibition_id = review.exhibition.id
        review.delete()

        if is_ajax(request):
            return JsonResponse({'success': True})

        return redirect('exhibitions:exhibition_detail', exhibition_id=exhibition_id)

    context = {
        'review': review,
    }

    return render(request, 'exhibitions/review_confirm_delete.html', context)