document.addEventListener('DOMContentLoaded', function () {
    const input = document.querySelector('input[type="file"][data-single-photo-input]');

    if (!input) {
        return;
    }

    const panel = document.getElementById('single-photo-panel');
    const image = document.getElementById('single-photo-preview-image');
    const removeButton = document.getElementById('single-photo-remove');

    if (!panel || !image || !removeButton) {
        return;
    }

    const initialSrc = image.getAttribute('src') || '';
    let selectedFile = null;

    function syncInputFile() {
        const dataTransfer = new DataTransfer();

        if (selectedFile) {
            dataTransfer.items.add(selectedFile);
        }

        input.files = dataTransfer.files;
    }

    function showPanel() {
        panel.hidden = false;
    }

    function hidePanel() {
        panel.hidden = true;
    }

    function renderInitialPhoto() {
        if (initialSrc) {
            image.src = initialSrc;
            showPanel();
            return;
        }

        image.removeAttribute('src');
        hidePanel();
    }

    input.addEventListener('change', function () {
        const files = Array.from(input.files);

        if (!files.length) {
            syncInputFile();

            if (!initialSrc) {
                hidePanel();
            }

            return;
        }

        selectedFile = files[0];

        const reader = new FileReader();

        reader.onload = function (event) {
            image.src = event.target.result;
            showPanel();
        };

        reader.readAsDataURL(selectedFile);
        syncInputFile();
    });

    removeButton.addEventListener('click', function () {
        selectedFile = null;
        syncInputFile();

        if (initialSrc) {
            image.src = initialSrc;
            showPanel();
        } else {
            image.removeAttribute('src');
            hidePanel();
        }
    });

    renderInitialPhoto();
});