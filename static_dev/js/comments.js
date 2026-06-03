document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('[data-comment-form]');

    forms.forEach(function (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            const submitButton = form.querySelector('[type="submit"]');
            const statusBox = form.querySelector('[data-form-status]');
            const commentsList = document.querySelector('[data-comments-list]');
            const emptyMessage = document.querySelector('[data-empty-comments]');

            if (statusBox) {
                statusBox.textContent = '';
            }

            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Отправляем...';
            }

            fetch(form.action || window.location.href, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(function (response) {
                    return response.json().then(function (data) {
                        return {
                            ok: response.ok,
                            data: data
                        };
                    });
                })
                .then(function (result) {
                    if (!result.ok) {
                        if (statusBox) {
                            statusBox.textContent = result.data.errors || 'Проверьте заполнение формы.';
                        }
                        return;
                    }

                    const comment = result.data.comment;

                    if (emptyMessage) {
                        emptyMessage.remove();
                    }

                    const card = document.createElement('article');
                    card.style.marginBottom = '16px';
                    card.style.padding = '18px';
                    card.style.background = '#f2d9b3';
                    card.style.border = '2px solid rgba(31, 23, 18, 0.18)';

                    const meta = document.createElement('p');
                    meta.className = 'item-meta';
                    meta.textContent = comment.author_name + ' · оценка ' + comment.rating + '/5 · ' + comment.created_at;

                    const text = document.createElement('p');
                    text.style.marginBottom = '0';
                    text.textContent = comment.text;

                    card.appendChild(meta);
                    card.appendChild(text);

                    if (commentsList) {
                        commentsList.prepend(card);
                    }

                    form.reset();

                    if (statusBox) {
                        statusBox.textContent = 'Комментарий добавлен.';
                    }
                })
                .catch(function () {
                    if (statusBox) {
                        statusBox.textContent = 'Не удалось отправить комментарий. Попробуйте ещё раз.';
                    }
                })
                .finally(function () {
                    if (submitButton) {
                        submitButton.disabled = false;
                        submitButton.textContent = submitButton.dataset.defaultText || 'Отправить комментарий';
                    }
                });
        });
    });
});