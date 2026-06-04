document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('[data-comment-form]');

    function getCookie(name) {
        const cookies = document.cookie ? document.cookie.split(';') : [];

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + '=')) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }

        return '';
    }

    function getCsrfToken() {
        if (form) {
            const csrfInput = form.querySelector('input[name="csrfmiddlewaretoken"]');

            if (csrfInput) {
                return csrfInput.value;
            }
        }

        return getCookie('csrftoken');
    }

    function autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    }

    function showConfirmModal(title, text, onConfirm) {
        let modal = document.querySelector('[data-confirm-modal]');

        if (!modal) {
            modal = document.createElement('div');
            modal.className = 'confirm-modal-backdrop';
            modal.setAttribute('data-confirm-modal', '');
            modal.innerHTML = `
                <div class="confirm-modal">
                    <p class="confirm-modal-kicker">confirm action</p>
                    <h3 data-confirm-title></h3>
                    <p data-confirm-text></p>
                    <div class="confirm-modal-actions">
                        <button type="button" class="review-button review-delete-button" data-confirm-yes>
                            Да, удалить
                        </button>
                        <button type="button" class="modal-cancel-button" data-confirm-no>
                            Отмена
                        </button>
                    </div>
                </div>
            `;

            document.body.appendChild(modal);
        }

        modal.querySelector('[data-confirm-title]').textContent = title;
        modal.querySelector('[data-confirm-text]').textContent = text;
        modal.classList.add('is-visible');

        const yesButton = modal.querySelector('[data-confirm-yes]');
        const noButton = modal.querySelector('[data-confirm-no]');

        function close() {
            modal.classList.remove('is-visible');
            yesButton.removeEventListener('click', confirmHandler);
            noButton.removeEventListener('click', close);
        }

        async function confirmHandler() {
            yesButton.disabled = true;

            try {
                await onConfirm();
            } finally {
                yesButton.disabled = false;
                close();
            }
        }

        yesButton.addEventListener('click', confirmHandler);
        noButton.addEventListener('click', close);
    }

    function buildReviewCard(comment) {
        const card = document.createElement('article');
        card.className = 'review-card';
        card.setAttribute('data-review-card', '');

        const meta = document.createElement('p');
        meta.className = 'item-meta';
        meta.textContent = `${comment.author_name} · ${comment.created_at}`;

        const text = document.createElement('p');
        text.textContent = comment.text;
        text.setAttribute('data-review-text', '');

        const actions = document.createElement('div');
        actions.className = 'review-actions';

        const editButton = document.createElement('button');
        editButton.type = 'button';
        editButton.className = 'inline-action-button';
        editButton.textContent = 'Редактировать';
        editButton.setAttribute('data-review-edit', '');
        editButton.setAttribute('data-edit-url', comment.edit_url);
        editButton.setAttribute('data-csrf', getCsrfToken());

        const deleteButton = document.createElement('button');
        deleteButton.type = 'button';
        deleteButton.className = 'inline-action-button danger-inline';
        deleteButton.textContent = 'Удалить';
        deleteButton.setAttribute('data-review-delete', '');
        deleteButton.setAttribute('data-delete-url', comment.delete_url);
        deleteButton.setAttribute('data-csrf', getCsrfToken());

        actions.appendChild(editButton);
        actions.appendChild(deleteButton);

        card.appendChild(meta);
        card.appendChild(text);
        card.appendChild(actions);

        return card;
    }

    if (form) {
        form.addEventListener('submit', async function (event) {
            event.preventDefault();

            const submitButton = form.querySelector('button[type="submit"]');
            const statusBox = form.querySelector('[data-form-status]');
            const commentsList = document.querySelector('[data-comments-list]');
            const emptyMessage = document.querySelector('[data-empty-comments]');

            if (statusBox) {
                statusBox.textContent = '';
                statusBox.classList.remove('is-success');
            }

            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Отправляем...';
            }

            try {
                const response = await fetch(form.action || window.location.href, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();

                if (!response.ok) {
                    if (statusBox) {
                        statusBox.textContent = data.errors || 'Проверьте заполнение формы.';
                    }

                    return;
                }

                if (emptyMessage) {
                    emptyMessage.remove();
                }

                const card = buildReviewCard(data.comment);

                if (commentsList) {
                    commentsList.prepend(card);
                }

                form.reset();
            } catch (error) {
                if (statusBox) {
                    statusBox.textContent = 'Не удалось отправить комментарий. Попробуйте ещё раз.';
                }
            } finally {
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = submitButton.dataset.defaultText || 'Отправить комментарий';
                }
            }
        });
    }

    document.addEventListener('click', async function (event) {
        const editButton = event.target.closest('[data-review-edit]');
        const deleteButton = event.target.closest('[data-review-delete]');

        if (editButton) {
            const card = editButton.closest('[data-review-card]');
            const textNode = card.querySelector('[data-review-text]');
            const actions = card.querySelector('.review-actions');
            const oldText = textNode.textContent.trim();

            if (card.querySelector('[data-inline-review-form]')) {
                return;
            }

            const formBox = document.createElement('div');
            formBox.className = 'inline-review-edit';
            formBox.setAttribute('data-inline-review-form', '');
            formBox.innerHTML = `
                <textarea class="inline-review-textarea" data-inline-review-text></textarea>
                <div class="form-status" data-inline-review-status></div>
                <div class="review-actions-panel inline-review-actions-panel">
                    <button type="button" class="review-button inline-save-button" data-inline-save>
                        Сохранить
                    </button>
                    <button type="button" class="modal-cancel-button inline-cancel-button" data-inline-cancel>
                        Отмена
                    </button>
                </div>
            `;

            const textarea = formBox.querySelector('[data-inline-review-text]');
            textarea.value = oldText;

            textNode.replaceWith(formBox);
            actions.style.display = 'none';

            textarea.focus();
            autoResizeTextarea(textarea);

            textarea.addEventListener('input', function () {
                autoResizeTextarea(textarea);
            });

            formBox.querySelector('[data-inline-cancel]').addEventListener('click', function () {
                formBox.replaceWith(textNode);
                actions.style.display = '';
            });

            formBox.querySelector('[data-inline-save]').addEventListener('click', async function () {
                const statusBox = formBox.querySelector('[data-inline-review-status]');
                const formData = new FormData();

                formData.append('csrfmiddlewaretoken', editButton.dataset.csrf || getCsrfToken());
                formData.append('text', textarea.value);

                try {
                    const response = await fetch(editButton.dataset.editUrl, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        statusBox.textContent = data.errors || 'Проверьте текст комментария.';
                        return;
                    }

                    textNode.textContent = data.text;
                    formBox.replaceWith(textNode);
                    actions.style.display = '';
                } catch (error) {
                    statusBox.textContent = 'Не удалось сохранить комментарий.';
                }
            });
        }

        if (deleteButton) {
            const card = deleteButton.closest('[data-review-card]');

            showConfirmModal(
                'Удалить комментарий?',
                'Комментарий исчезнет со страницы. Отменить это действие нельзя.',
                async function () {
                    const formData = new FormData();

                    formData.append(
                        'csrfmiddlewaretoken',
                        deleteButton.dataset.csrf || getCsrfToken()
                    );

                    const response = await fetch(deleteButton.dataset.deleteUrl, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });

                    if (response.ok && card) {
                        card.remove();
                    }
                }
            );
        }
    });
});