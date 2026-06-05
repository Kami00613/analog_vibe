document.addEventListener('DOMContentLoaded', function () {
    const lightbox = document.getElementById('photo-lightbox');
    const lightboxImage = document.getElementById('photo-lightbox-image');
    const lightboxCaption = document.getElementById('photo-lightbox-caption');

    if (!lightbox || !lightboxImage || !lightboxCaption) {
        return;
    }

    const openButtons = Array.from(document.querySelectorAll('[data-lightbox-open]'));
    const closeButtons = Array.from(document.querySelectorAll('[data-lightbox-close]'));
    const prevButton = document.querySelector('[data-lightbox-prev]');
    const nextButton = document.querySelector('[data-lightbox-next]');

    const photos = openButtons.map(function (button) {
        return {
            src: button.dataset.lightboxSrc,
            title: button.dataset.lightboxTitle || ''
        };
    });

    let currentIndex = 0;

    function showPhoto(index) {
        if (!photos.length) {
            return;
        }

        if (index < 0) {
            currentIndex = photos.length - 1;
        } else if (index >= photos.length) {
            currentIndex = 0;
        } else {
            currentIndex = index;
        }

        const photo = photos[currentIndex];

        lightboxImage.src = photo.src;
        lightboxImage.alt = photo.title;
        lightboxCaption.textContent = photo.title;
    }

    function openLightbox(index) {
        showPhoto(index);

        lightbox.classList.add('is-visible');
        lightbox.setAttribute('aria-hidden', 'false');
        document.body.classList.add('lightbox-open');
    }

    function closeLightbox() {
        lightbox.classList.remove('is-visible');
        lightbox.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('lightbox-open');

        lightboxImage.src = '';
        lightboxImage.alt = '';
        lightboxCaption.textContent = '';
    }

    openButtons.forEach(function (button, index) {
        button.addEventListener('click', function () {
            openLightbox(index);
        });
    });

    closeButtons.forEach(function (button) {
        button.addEventListener('click', closeLightbox);
    });

    if (prevButton) {
        prevButton.addEventListener('click', function () {
            showPhoto(currentIndex - 1);
        });
    }

    if (nextButton) {
        nextButton.addEventListener('click', function () {
            showPhoto(currentIndex + 1);
        });
    }

    document.addEventListener('keydown', function (event) {
        if (!lightbox.classList.contains('is-visible')) {
            return;
        }

        if (event.key === 'Escape') {
            closeLightbox();
        }

        if (event.key === 'ArrowLeft') {
            showPhoto(currentIndex - 1);
        }

        if (event.key === 'ArrowRight') {
            showPhoto(currentIndex + 1);
        }
    });
});