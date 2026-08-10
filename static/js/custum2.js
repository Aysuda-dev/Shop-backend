
function three_digit_currency(value) {
    if (value === null || value === undefined) return '';

    return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') + 'ریال';
}


document.addEventListener("DOMContentLoaded", function () {
    const sizeSelect = document.getElementById("sizeSelect");
    const colorSelect = document.getElementById("colorSelect");
    const variantInfo = document.getElementById("variantInfo");
    const variantPrice = document.getElementById("price_id");
    const addBtt = document.getElementById("add-btt");
    const productId= document.getElementById("productId").value;

    sizeSelect.value = '';


    sizeSelect.addEventListener("change", function () {
        const sizeId = this.value;

        if (!sizeId) {
            colorSelect.innerHTML = "<option value=''>اول سایز را انتخاب کنید</option>";
            variantInfo.innerHTML = "<p style='color:#666'>سایز انتخاب نشده</p>";
            return;
        }

        fetch(`/product/colors/${productId}/?size_id=${sizeId}`)
            .then(res => res.json())
            .then(data => {
                colorSelect.innerHTML = "<option value=''>انتخاب رنگ</option>";
                data.colors.forEach(c => {
                    colorSelect.innerHTML += `<option value="${c.color_id}">${c.color__name}</option>`;
                });
                variantInfo.innerHTML = "<p style='color:#666'>حالا رنگ را انتخاب کنید</p>";
            });
    });

    colorSelect.addEventListener("change", () => {
        const sizeId = sizeSelect.value;
        const colorId = colorSelect.value;

        if (!colorId) {
            addBtt.disabled = true;
            return;
        }

        fetch(`/product/variant/${productId}/?size_id=${sizeId}&color_id=${colorId}`)
            .then(res => res.json())
            .then(data => {
                variantInfo.innerHTML = "<p style='color:#666'></p>";

                if (!data.variant_id) {
                    addBtt.disabled = true;
                    return;
                }

                addBtt.disabled = false;
                addBtt.setAttribute("data-variant-id", data.variant_id);

                variantPrice.innerHTML = `<h3><b>قیمت :</b> ${three_digit_currency(data.price)}</h3>`;
                addBtt.dataset.variantStock = data.stock;
            });
    });

    addBtt.addEventListener("click", () => {
        const count = parseInt($('#product-count').val(), 10);
        const stock = parseInt(addBtt.dataset.variantStock, 10);
        if (count > stock) {
            Swal.fire({
                title: 'خطا',
                text: "تعداد مورد نظر موجود نیست",
                icon: 'warning',
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'باشه ممنون'
            });
            return;
        }
        const vid = addBtt.getAttribute("data-variant-id");
        addProductToOrder(vid, count);
    });


});