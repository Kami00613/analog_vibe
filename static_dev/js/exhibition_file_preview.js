document.addEventListener('DOMContentLoaded', function () {
    const input = document.querySelector('input[type="file"][name="images"]');

    if (!input) {
        return;
    }

    const maxFiles = 25;
    const selectedFiles = [];

    const panel = document.getElementById('exhibition-photos-panel');
    const grid = document.getElementById('exhibition-photos-grid');
    const count = document.getElementById('selected-photos-count');
    const limitMessage = document.getElementById('selected-photos-limit-message');
    const deleteInputsContainer = document.getElementById('deleted-photo-inputs');

    function getExistingCards() {
        return Array.from(document.querySelectorAll('[data-existing-photo-card]'));
    }

    function getSelectedCards() {
        return Array.from(document.querySelectorAll('[data-selected-photo-card]'));
    }

    function getFileKey(file) {
        return [
            file.name,
            file.size,
            file.lastModified
        ].join('__');
    }

    function getExistingCount() {
        return getExistingCards().length;
    }

    function getTotalPhotosCount() {
        return getExistingCount() + selectedFiles.length;
    }

    function updateCount() {
        if (count) {
            count.textContent = getTotalPhotosCount();
        }

        if (panel) {
            panel.hidden = getTotalPhotosCount() === 0;
        }
    }

    function showLimitMessage(message) {
        if (!limitMessage) {
            return;
        }

        limitMessage.textContent = message;
        limitMessage.hidden = false;
    }

    function hideLimitMessage() {
        if (!limitMessage) {
            return;
        }

        limitMessage.textContent = '';
        limitMessage.hidden = true;
    }

    function syncInputFiles() {
        const dataTransfer = new DataTransfer();

        selectedFiles.forEach(function (file) {
            dataTransfer.items.add(file);
        });

        input.files = dataTransfer.files;
    }

    function removeSelectedPhotoCards() {
        getSelectedCards().forEach(function (card) {
            card.remove();
        });
    }

    function addDeleteInput(photoId) {
        if (!deleteInputsContainer) {
            return;
        }

        const exists = deleteInputsContainer.querySelector(
            'input[name="delete_photo_ids"][value="' + photoId + '"]'
        );

        if (exists) {
            return;
        }

        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'delete_photo_ids';
        hiddenInput.value = photoId;

        deleteInputsContainer.appendChild(hiddenInput);
    }

    function renderSelectedPhotos() {
        if (!grid || !panel) {
            syncInputFiles();
            return;
        }

        removeSelectedPhotoCards();

        selectedFiles.forEach(function (file, index) {
            const card = document.createElement('div');
            card.className = 'current-exhibition-photo selected-photo-card';
            card.setAttribute('data-selected-photo-card', 'true');

            const image = document.createElement('img');
            image.alt = file.name;

            const reader = new FileReader();

            reader.onload = function (event) {
                image.src = event.target.result;
            };

            reader.readAsDataURL(file);

            const removeButton = document.createElement('button');
            removeButton.type = 'button';
            removeButton.className = 'current-photo-remove selected-photo-remove';
            removeButton.setAttribute('aria-label', 'Убрать фото');
            removeButton.textContent = '×';

            removeButton.addEventListener('click', function () {
                selectedFiles.splice(index, 1);
                syncInputFiles();
                renderSelectedPhotos();
                hideLimitMessage();
            });

            card.appendChild(image);
            card.appendChild(removeButton);

            grid.appendChild(card);
        });

        syncInputFiles();
        updateCount();
    }

    function initExistingPhotoRemoveButtons() {
        getExistingCards().forEach(function (card) {
            const removeButton = card.querySelector('[data-existing-photo-remove]');
            const photoId = card.dataset.photoId;

            if (!removeButton || !photoId) {
                return;
            }

            removeButton.addEventListener('click', function () {
                addDeleteInput(photoId);

                card.remove();

                renderSelectedPhotos();
                updateCount();
                hideLimitMessage();
            });
        });
    }

    input.addEventListener('change', function () {
        const newFiles = Array.from(input.files);
        let skippedByLimit = 0;

        newFiles.forEach(function (file) {
            const fileKey = getFileKey(file);

            const alreadyExists = selectedFiles.some(function (savedFile) {
                return getFileKey(savedFile) === fileKey;
            });

            if (alreadyExists) {
                return;
            }

            if (getTotalPhotosCount() >= maxFiles) {
                skippedByLimit += 1;
                return;
            }

            selectedFiles.push(file);
        });

        renderSelectedPhotos();

        if (skippedByLimit > 0) {
            showLimitMessage('Можно оставить максимум 25 фото. Лишние файлы не добавлены.');
        } else {
            hideLimitMessage();
        }
    });

    initExistingPhotoRemoveButtons();
    updateCount();
});