// document.addEventListener('DOMContentLoaded', function () {
//     const marker = document.getElementById('marker');
//     const navigationLinks = document.querySelectorAll('.navigation a');

//     function setCurrentPage() {
//         const currentPage = window.location.pathname.split('/').pop();
//         navigationLinks.forEach(link => {
//             if (link.getAttribute('href') === currentPage) {
//                 marker.style.left = link.offsetLeft + 'px';
//                 marker.style.width = link.offsetWidth + 'px';
//             }
//         });
//     }

//     setCurrentPage();

//     navigationLinks.forEach(link => {
//         link.addEventListener('click', function (e) {
//             marker.style.left = e.target.offsetLeft + 'px';
//             marker.style.width = e.target.offsetWidth + 'px';
//         });
//     });
// });

document.addEventListener('DOMContentLoaded', function () {
    const marker = document.getElementById('marker');
    const navigationLinks = document.querySelectorAll('.navigation a');
    const stars = document.querySelectorAll('.star');
    const numericalRating = document.getElementById('numericalRating');
    let currentRating = 0;

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

    stars.forEach(star => {
        star.addEventListener('click', () => {
            const value = parseInt(star.getAttribute('data-value'));
            setRating(value);
        });
    });

    function setRating(value) {
        currentRating = value;
        numericalRating.textContent = currentRating;
        stars.forEach((star, index) => {
            if (index < value) {
                star.classList.add('active');
            } else {
                star.classList.remove('active');
            }
        });
    }

    document.getElementById('submitFeedback').addEventListener('click', () => {
        const feedback = document.getElementById('feedback').value.trim();
        if (feedback !== "") {
//             // Send email using EmailJS
//             emailjs.send("service_zpwnm3w", "template_nvxv5vl", {
//                 feedback: feedback,
//                 rating: currentRating
//             }).then(function(response) {
//                 alert("Feedback submitted successfully!");
//                 // Clear the textarea after submission
//                 document.getElementById('feedback').value = "";
//                 // Reset the rating
//                 setRating(0);
//             }, function(error) {
//                 alert("Failed to submit feedback. Please try again later.");
//                 console.error('EmailJS Error:', error);
//             });
//         } else {
//             alert("Please enter your feedback.");
//         }
//     });
// });
            // Handle feedback submission here
            console.log("Feedback submitted:", feedback);
            console.log("Numerical Rating:", currentRating);
            // Clear the textarea after submission
            document.getElementById('feedback').value = "";
            // Reset the rating
            setRating(0);
            alert("Thank you for your feedback!");
        }
    });
});
