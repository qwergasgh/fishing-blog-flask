var csrftoken = $('meta[name=csrf-token]').attr('content')

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})

function get_images(id) {
    $.ajax({
        type: 'POST',
        url: '/blog/get_images',
        data: JSON.stringify({id_post: id}),
        contentType: 'application/json',
        success: function(response) {
            console.log('valid: ' + response.valid);
            for (i in response.path_images) {
                img = document.createElement('img');
                img.class = "img-rounded profile-thumbnail";
                img.src = "{{ url_for('static', filename='" + response.path_images[i] + "') }}";
                img.width = "256";
                img.height = "256";
                console.log(img)
                document.getElementById(id).append(img);
            }
        },
        error: function(error) {
            console.log(error.status + ' ' + error.valid);
        }
    });
}