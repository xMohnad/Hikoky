$(document).ready(function() {
    $('.loading-dots').hide();
    
    $('#load-more').on('click', function() {
        let button = $(this);
        let next_page_url = button.data('url');
        
        var currentUrl = window.location.href;
        var parts = currentUrl.split('/');
        var source = parts[3];
        
        $('.loading-dots').show().addClass('show');
        
        $.ajax({
            url: window.location.pathname,
            type: "GET",
            data: {
                next_page_url: next_page_url,
                source: source
            },
            success: function(response) {
                $('.loading-dots').removeClass('show');
                setTimeout(function() {
                    $('.loading-dots').hide();
                }, 100); 
                
                // Append new results
                let newContent = '';response.results.forEach(function(result) {
                newContent += `<div class="box">
                    <div class="page-item-detail manga">
                        <div id="manga-item-${result.id}" class="item-thumb c-image-hover" data-post-id="${result.id}">
                            <a href="${window.location.pathname}/${result.manga_link}" title="${result.manga_name}">
                                ${result.translation_team ? `<span class="manga-title-badges">${result.translation_team}</span>` : ``}
                                <img src="${result.manga_cover}" alt="${result.manga_name}">
                            </a>
                        </div>
                        <div class="post-title">
                            <h3 class="h5">
                                <a href="${window.location.pathname}/${result.manga_link}">${result.manga_name}</a>
                            </h3>
                        </div>
                        <div class="list-chapter">
                            <div class="chapter-item has-thumb">
                                <span class="chapter font-meta">
                                    ${result.chapters_info.latest_chapter_number ? `<a href="${window.location.pathname}/${result.manga_link}/${result.chapters_info.latest_chapter_url}" class="btn-link">${result.chapters_info.latest_chapter_number}</a>` : ''}
                                </span>
                            </div>
                            <div class="chapter-item has-thumb">
                                <span class="chapter font-meta">
                                    ${result.chapters_info.penultimate_chapter_number ? `<a href="${window.location.pathname}/${result.manga_link}/${result.chapters_info.penultimate_chapter_url}" class="btn-link">${result.chapters_info.penultimate_chapter_number}</a>` : ''}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>`;
            });
                $('.manga-list').append(newContent);
                if (response.next_page_url) {
                    button.data('url', response.next_page_url);
                } else {
                    button.remove();
                }
            },
            error: function() {
                $('.dot').addClass('error');
                
                setTimeout(function() {
                    $('.loading-dots').removeClass('show');
                    setTimeout(function() {
                        $('.loading-dots').hide();
                    }, 500); 
                $('.dot').removeClass('error');
                }, 1500); 
            }
        });
    });
});

$(document).ready(function() {
    $('#load-more').on('click', function() {
        var button = $(this);
        button.removeClass('animate');
        setTimeout(function() {
            button.addClass('animate');
        }, 10); 
    });
});

$(document).ready(function() {
  $('#heading-title').on('click', function() {
    $(this).toggleClass('active');
  });
});