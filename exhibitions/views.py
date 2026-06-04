from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ExhibitionCommentForm
from .models import Exhibition


def exhibition_list(request):
    exhibitions = Exhibition.objects.all()

    context = {
        'exhibitions': exhibitions,
    }

    return render(request, 'exhibitions/list.html', context)


def exhibition_detail(request, exhibition_id):
    exhibition = get_object_or_404(Exhibition.objects.select_related('curator'), id=exhibition_id)
    comments = exhibition.comments.filter(is_visible=True).select_related('author')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'errors': 'Чтобы оставить комментарий, нужно войти в аккаунт.'
                }, status=403)

            return redirect('accounts:login')

        form = ExhibitionCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.exhibition = exhibition
            comment.author = request.user
            comment.author_name = request.user.username
            comment.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'comment': {
                        'author_name': comment.author_name,
                        'text': comment.text,
                        'rating': comment.rating,
                        'created_at': timezone.localtime(comment.created_at).strftime('%d.%m.%Y %H:%M'),
                    }
                })

            return redirect('exhibitions:exhibition_detail', exhibition_id=exhibition.id)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'errors': form.errors.as_text()
            }, status=400)

    else:
        form = ExhibitionCommentForm()

    context = {
        'exhibition': exhibition,
        'comments': comments,
        'form': form,
    }

    return render(request, 'exhibitions/detail.html', context)