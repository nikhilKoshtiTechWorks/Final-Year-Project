document.addEventListener('DOMContentLoaded', function () {
    const gallery = document.getElementById('imageGallery');
    const titleNames = gallery.querySelectorAll('.title-name');
    let lastHoveredIndex = 0;

    function showFullImage(index) {
        titleNames.forEach(title => title.classList.remove('active'));

        setTimeout(() => {
            titleNames[index].classList.add('active');
        }, 10);

        if (index > 0) {
            titleNames[index - 1].style.width = '10%';
            titleNames[index - 1].querySelector('img').style.width = '100%';
        }

        titleNames[lastHoveredIndex].style.width = '10%';
        titleNames[lastHoveredIndex].querySelector('img').style.width = '100%';

        if (index === titleNames.length - 1) {
            titleNames[0].style.width = '10%';
            titleNames[0].querySelector('img').style.width = '100%';
            titleNames[index].style.width = '100%';
            titleNames[index].querySelector('img').style.width = '100%';
        } else {
            titleNames[index].style.width = '100%';
            titleNames[index].querySelector('img').style.width = '100%';
        }

        lastHoveredIndex = index;
    }

    titleNames.forEach((titleName, index) => {
        const img = titleName.querySelector('img');
        const titleText = titleName.querySelector('.image-text');

        titleName.addEventListener('mouseover', function () {
            showFullImage(index);
        });

        titleName.addEventListener('click', function () {
            window.location.href = img.getAttribute('data-href');
        });
    });

    // Show the full image on initial page load
    showFullImage(0);

    gallery.addEventListener('mouseleave', function () {
        titleNames.forEach(title => {
            title.style.width = '';
            title.querySelector('img').style.width = '';
        });
        titleNames[lastHoveredIndex].style.width = '100%';
        titleNames[lastHoveredIndex].querySelector('img').style.width = '100%';
    });
});
