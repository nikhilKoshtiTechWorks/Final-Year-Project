document.addEventListener('DOMContentLoaded', function () {
    const gallery = document.getElementById('imageGallery');
    const images = gallery.querySelectorAll('img');
    let lastHoveredIndex = 0; // Track the index of the last hovered image

    images.forEach((image, index) => {
        image.addEventListener('mouseover', function () {
            // Remove 'active' class from all images
            images.forEach(img => img.classList.remove('active'));

            // Add 'active' class to the hovered image
            this.classList.add('active');

            // Set the width of the previous image to 10%
            if (index > 0) {
                images[index - 1].style.width = '10%';
            }

            // Set the width of the last hovered image to 10%
            images[lastHoveredIndex].style.width = '10%';

            // Set the width of the first image to 10% when hovering over the last image
            if (index === images.length - 1) {
                images[0].style.width = '10%';
                this.style.width = '100%'; // Set the width of the last hovered image to 100%
            } else {
                this.style.width = '100%'; // Set the width of the hovered image to 100%
            }

            lastHoveredIndex = index; // Update the last hovered index
        });

        // Add click event for redirection
        image.addEventListener('click', function () {
            window.location.href = this.getAttribute('data-href');
        });
    });

    // Set the width of the first image to 100% initially
    images[0].classList.add('active');

    // Reset the width of all images to 10% when mouse leaves the gallery
    gallery.addEventListener('mouseleave', function () {
        images.forEach(img => img.style.width = '');
        images[lastHoveredIndex].style.width = '100%'; // Retain 100% width for the last hovered image
    });
});
