function sendArticleComment(articleId) {

    var comment = $("#commentText").val();
    var parentId = $('#parent_id').val();

    $.get('/article/add-article-comment', {
        article_comment: comment, article_id: articleId, parent_id: parentId

    }).then(res => {
        console.log(res);
        $('#comments_area').html(res);
        $("#commentText").val('');
        $('#parent_id').val('');
        if (parentId !== null && parentId !== '') {
            document.getElementById('single_comment_box_' + parentId).scrollIntoView({behavior: "smooth"})

        } else {
            document.getElementById('commnets_area').scrollIntoView({behavior: "smooth"})
        }
    });

}


function fillParentId(parent_id) {
    $('#parent_id').val(parent_id)
    document.getElementById('comment_form').scrollIntoView({behavior: "smooth"})
}

function filterProduct() {
    const filterPrice = $('#sl2').val()
    const start_price = filterPrice.split(',')[0]
    const end_price = filterPrice.split(',')[1]
    $('#start_price').val(start_price);
    $('#end_price').val(end_price);

    $('#page').val(1)
    $('#filter_form').submit();
}

function fillpage(page) {
    $('#page').val(page);
    $('#filter_form').submit();
}


function showLargeImage(imageSrc) {
    $('#main_image').attr('src', imageSrc);
    $('#show_large_image_modal').attr('href', imageSrc);

}


function addProductToOrder(variantid, count) {
    $.get('/order/add-to-order?variant_id=' + variantid + "&count=" + count).done(res => {
        Swal.fire({
            title: 'اعلان',
            text: res.text,
            icon: res.icon,
            confirmButtonColor: '#3085d6',
            confirmButtonText: res.confirm_button_text
        }).then(() => {
            if (res.status === 'not_auth') {
                window.location.href = '/account/login';
            }
        })


        // if (res.status === 'success') {
        //     Swal.fire({
        //         title: 'اعلان',
        //         text: "محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد",
        //         icon: 'success',
        //         showCancelButton: false,
        //         confirmButtonColor: '#3085d6',
        //         confirmButtonText: 'باشه ممنون'
        //     });
        // } else if (res.status === 'not_found') {
        //     Swal.fire({
        //         title: 'اعلان',
        //         text: "محصول مورد نظر یافت نشد",
        //         icon: 'error',
        //         showCancelButton: false,
        //         confirmButtonColor: '#3085d6',
        //         confirmButtonText: 'باشه ممنون'
        //     });
        // }
    });
}

function removeOrderDetail(detailId) {
    $.get('/user/remove-order-detail?detail_id=' + detailId).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}


// detail id => order detail id
// state => increase , decrease
function changeOrderDetailCount(detailId, state) {
    $.get('/user/change-order-detail?detail_id=' + detailId + '&state=' + state).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}



function pay() {
    const btn = document.getElementById('pay-success');

    btn.disabled = true;
    btn.innerText = 'در حال پرداخت...';

    fetch('/order/verify-payment/?status=success')
        .then(res => res.json())
        .then(data => {
            // btn.disabled = false;
            // btn.innerText = 'پرداخت (دمو)';

            if (data.status === true) {
                // نمایش پیام موفقیت با کد رهگیری
                Swal.fire({
                    icon: 'success',
                    title: 'پرداخت موفق',
                    text: 'کد رهگیری: ' + data.ref_id,
                    confirmButtonText: 'باشه'
                }).then(() => {
                    // بعد از کلیک روی "باشه" → برگشت به صفحه سبد خرید
                    window.location.href = '/user/user-basket';
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'پرداخت ناموفق',
                    text: data.message || 'خطا'
                });
            }
        })
        .catch(() => {
            btn.disabled = false;
            btn.innerText = 'پرداخت (دمو)';
            Swal.fire('خطا', 'مشکل ارتباط با سرور', 'error');
        });
}



document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('search-input');
    const box = document.getElementById('search-results');
    let timer = null;

    if (!input || !box) return;

    input.addEventListener('keyup', () => {
        clearTimeout(timer);
        timer = setTimeout(() => {
            const q = input.value.trim();
            if (!q) {
                box.style.display = 'none';
                return;
            }

            fetch(`/product/search/?query=${encodeURIComponent(q)}`)
                .then(res => res.json())
                .then(data => {
                    box.innerHTML = '';
                    box.style.display = 'block';

                    data.forEach(item => {
                        const div = document.createElement('div');
                        div.className = 'search-item';

                        let imgHTML = item.image ? `<img src="${item.image}" alt="${item.title}" style="width:30px;height:30px;margin-right:5px;vertical-align:middle;">` : '';

                        div.innerHTML = `${imgHTML} <span>${item.title} (${item.type})</span>`;
                        div.onclick = () => window.location.href = item.url;
                        box.appendChild(div);
                    });
                })
                .catch(err => console.error(err));
        }, 300);
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-form')) {
            box.style.display = 'none';
        }
    });
});