document.addEventListener('DOMContentLoaded', function () {
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

    function showConfirmModal(title, text, onConfirm) {
        let modal = document.querySelector('[data-global-confirm-modal]');

        if (!modal) {
            modal = document.createElement('div');
            modal.className = 'confirm-modal-backdrop';
            modal.setAttribute('data-global-confirm-modal', '');
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

    document.addEventListener('click', function (event) {
        const deleteButton = event.target.closest('[data-object-delete]');

        if (!deleteButton) {
            return;
        }

        event.preventDefault();

        showConfirmModal(
            deleteButton.dataset.confirmTitle || 'Удалить запись?',
            deleteButton.dataset.confirmText || 'Отменить это действие нельзя.',
            async function () {
                const formData = new FormData();

                formData.append(
                    'csrfmiddlewaretoken',
                    deleteButton.dataset.csrf || getCookie('csrftoken')
                );

                const response = await fetch(deleteButton.dataset.deleteUrl, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                if (!response.ok) {
                    return;
                }

                let data = {};

                try {
                    data = await response.json();
                } catch (error) {
                    data = {};
                }

                const redirectUrl = deleteButton.dataset.deleteRedirect || data.redirect_url;

                if (redirectUrl) {
                    window.location.href = redirectUrl;
                    return;
                }

                const card = deleteButton.closest('[data-owned-card]');

                if (card) {
                    card.remove();
                }
            }
        );
    });
});