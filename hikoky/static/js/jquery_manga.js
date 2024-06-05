$(document).ready(function() {
    function load_more() {
        let moreDiv = $('.more');
        let nextPageUrl = moreDiv.data('url');
        $('.loading-dots').hide();
        if (nextPageUrl) {
            var currentUrl = window.location.href;
            var parts = currentUrl.split('/');
            var source = parts[3];

            // إظهار الرسوم المتحركة
            $('.loading-dots').show();

            $.ajax({
                url: '/load_more',
                type: "GET",
                data: {
                    nextPageUrl: nextPageUrl,
                    source: source
                },
                success: function(response) {
                    // إخفاء الرسوم المتحركة بعد الانتهاء من التحميل
                    $('.loading-dots').hide();

                    // Append new results
                    let newContent = '';
                    response.chapters.forEach(function(chapter) {
                        newContent += `<li class="chapter-item">
                            <a href="${window.location.pathname}/${chapter.number}">
                                الفصل ${chapter.number}
                                ${chapter.date ? `<span class="date">${chapter.date}</span>` : ''}
                            </a>
                        </li>`;
                    });

                    $('.list').append(newContent);

                    // Update next page URL
                    if (response.next_page_link) {
                        moreDiv.data('url', response.next_page_link);
                        // تكرار إرسال الطلب بانتظام بعد فترة زمنية معينة
                        setTimeout(load_more, 2600); // هنا يتم إرسال الطلب كل ثانية واحدة (يمكن تغيير الفترة الزمنية حسب الحاجة)
                    } else {
                        moreDiv.remove();
                    }
                },
                error: function(xhr, status, error) {
                    // إخفاء الرسوم المتحركة عند حدوث خطأ
                    $('.loading-dots').hide();
                    console.error('Error:', error);
                }
            });
        }
    }

    // تنفيذ الدالة لأول مرة عند تحميل الصفحة
    load_more();
});

$(function() {
    $('.chapter-item').hover(function() {
        $(this).css('background-color', '#444');
    }, function() {
        $(this).css('background-color', '#333');
    });
});
