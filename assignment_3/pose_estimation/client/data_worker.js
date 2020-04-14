$(document).ready(function () {
    $('#submit').on('click', function () {
        const formData = new FormData();
        $('#output-img').attr(
            'src',
            ''
        );
        attachments = document.getElementById('img').files
        if(attachments.length === 0){
            console.log("No files selected");
            $('#upload-help').html("Select at least one file");
            return;
        }

        formData.append("file", attachments[0]);
        console.log("File apppended");
        $('#upload-help').html("File appended, processing...");
        $.ajax({
            "url": "http://127.0.0.1:5000/upload_img",
            "method": "POST",
            "timeout": 0,
            "processData": false,
            "mimeType": "multipart/form-data",
            "contentType": false,
            "dataType": "json",
            "data": formData,
            success: function (response) {
                console.log("Processing done");
                console.log(response)
                $('#upload-help').html("");
                $('#output-img').attr(
                    'src',
                    `data:image/jpg;base64,${response["image"]}`
                );
            },
            error: function (response, status, error) {
                console.log("Processing failed");
                console.log(response)
                $('#upload-help').html(`Processing failed. ${response.responseJSON["message"]}`);
                return;
            }
        });
    });
});