document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll(".chapter-image");
    let currentIndex = 0;

    function loadNextImage() {
        if (currentIndex < images.length) {
            const img = images[currentIndex];
            img.src = img.getAttribute('data-src');
            img.onload = function() {
                img.style.display = 'block';
                currentIndex++;
                loadNextImage();
            };
            img.onerror = function() {
                console.error("Failed to load image:", img.getAttribute('data-src'));
                currentIndex++;
                loadNextImage();
            };
        }
    }

    loadNextImage();
});


document.addEventListener("DOMContentLoaded", function() {
    let lazyLoadInstance = new LazyLoad({
        elements_selector: ".lazy",
        callback_loaded: function(element) {
            element.style.display = 'block';
        }
    });
});

document.getElementById("readerarea").addEventListener("click", function(event) {
    if(event.clientY < window.innerHeight / 2) {
        window.scrollTo(0, window.scrollY - window.innerHeight * 0.5);
    }
    else {
        window.scrollTo(0, window.scrollY + window.innerHeight * 0.5);
    }
});
function toggleFullScreen() {
    const icon = document.querySelector('#FullScreen i');
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
        icon.classList.remove('fa-expand');
        icon.classList.add('fa-compress');
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
            icon.classList.remove('fa-compress');
            icon.classList.add('fa-expand');
        }
    }
}

var btns = document.getElementById('Button');
    var lastScrollTop = 0;
    window.addEventListener('scroll', function() {
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (scrollTop > lastScrollTop) {
            btns.classList.add('hidden');
        } else {
            btns.classList.remove('hidden');
        }
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    });

// function scrollToTop() {
//   window.scrollTo(0, 0);
// }
// window.onscroll = function() {scrollFunction()};
// function scrollFunction() {
//     if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
//         document.getElementById('scroll-top').style.display = "block";
//     } else {
//         document.getElementById('scroll-top').style.display = "none";
//     }
// }
// 
// function scrollToDown() {
//   window.scrollTo(0, document.body.scrollHeight);
// }