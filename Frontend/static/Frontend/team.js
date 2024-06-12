document.addEventListener('DOMContentLoaded', function () {
    const marker = document.getElementById('marker');
    const navigationLinks = document.querySelectorAll('.navigation a');

    function setCurrentPage() {
        const currentPage = window.location.pathname.split('/').pop();
        navigationLinks.forEach(link => {
            if (link.getAttribute('href') === currentPage) {
                marker.style.left = link.offsetLeft + 'px';
                marker.style.width = link.offsetWidth + 'px';
            }
        });
    }

    setCurrentPage();

    navigationLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            marker.style.left = e.target.offsetLeft + 'px';
            marker.style.width = e.target.offsetWidth + 'px';
        });
    });
});

