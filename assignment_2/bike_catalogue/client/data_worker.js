$(document).ready(function () {
    draw_cards()
});

function draw_cards() {
    $('#row').html('');
    $.getJSON('http://127.0.0.1:5000/', function (data) {
        $.each(data, function (key, val) {
            let card = "";
            let card_body = "";

            $.each(val, function (key, val) {
                if (key === "model") {
                    card_body += `<p class="card-text"> ${ val } </p>`;
                } else if (key === "img_link") {
                    card += `<img src="${ val }" class="card-img-top">`
                } else {
                    card_body += `<div class="d-flex justify-content-between align-items-center">
                        <h3 class="text-info">
                            ${ val }
                        </h3>
                    </div>
                    `;
                }
            });

            $('#row').append(`
                <div class="col-md-4">
                    <div class="card mb-4 p-4">
                        ${card}
                        <div class="card-body">
                            ${card_body}
                        </div>
                    </div>
                </div>
            `);
        });
    });
}
