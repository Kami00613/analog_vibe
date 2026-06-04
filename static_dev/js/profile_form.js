document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('[data-profile-form]');

    if (!form) {
        return;
    }

    const submitButton = form.querySelector('button[type="submit"]');
    const globalErrors = form.querySelector('[data-profile-form-errors]');

    function clearErrors() {
        const errorBoxes = form.querySelectorAll('[data-field-error]');
        const fields = form.querySelectorAll('input, textarea, select');

        errorBoxes.forEach(function (box) {
            box.textContent = '';
        });

        fields.forEach(function (field) {
            field.classList.remove('field-invalid');
        });

        if (globalErrors) {
            globalErrors.textContent = '';
            globalErrors.style.display = 'none';
        }
    }

    function showErrors(errors) {
        let firstInvalidField = null;

        Object.keys(errors).forEach(function (fieldName) {
            const messages = errors[fieldName].join(' ');

            if (fieldName === '__all__') {
                if (globalErrors) {
                    globalErrors.textContent = messages;
                    globalErrors.style.display = 'block';
                }

                return;
            }

            const errorBox = form.querySelector('[data-field-error="' + fieldName + '"]');
            const field = form.querySelector('[name="' + fieldName + '"]');

            if (errorBox) {
                errorBox.textContent = messages;
            }

            if (field) {
                field.classList.add('field-invalid');

                if (!firstInvalidField) {
                    firstInvalidField = field;
                }
            }
        });

        if (firstInvalidField) {
            firstInvalidField.focus();
        }
    }

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        clearErrors();

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = 'Сохраняем...';
        }

        try {
            const response = await fetch(window.location.href, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (!response.ok) {
                showErrors(data.errors || {});
                return;
            }

            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            }
        } catch (error) {
            if (globalErrors) {
                globalErrors.textContent = 'Не удалось сохранить профиль. Попробуйте ещё раз.';
                globalErrors.style.display = 'block';
            }
        } finally {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = submitButton.dataset.defaultText || 'Сохранить профиль';
            }
        }
    });
});