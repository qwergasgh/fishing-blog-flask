var csrftoken = $('meta[name=csrf-token]').attr('content')

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})

function get_images(id) {
    id_element = id.toString();
    if (document.getElementById(id_element + "_button").textContent == "Remove Images") {
        document.getElementById(id_element + "_button").textContent = "Show Images";
        document.getElementById(id_element + '_div').remove();
    } else {
        $.ajax({
            type: 'POST',
            url: '/blog/get_images',
            data: JSON.stringify({id_post: id}),
            contentType: 'application/json',
            success: function(response) {
                console.log('valid: ' + response.valid);
                if (response.path_images.length > 0) {
                    div = document.createElement('div');
                    div.id = id_element + '_div';
                    document.getElementById(id_element).append(div)
                    console.log(response.path_images.length, div.id)
                    for (i in response.path_images) {
                        img = document.createElement('img');
                        img.class = "img-rounded profile-thumbnail";
                        // img.src = "{{ url_for('static', filename='" + response.path_images[i] + "') }}";
                        img.src = '/static/' + response.path_images[i];
                        img.width = "256";
                        img.height = "256";
                        document.getElementById(div.id).append(img);
                    }
                    document.getElementById(id_element + "_button").textContent = "Remove Images";
                }
            },
            error: function(error) {
                console.log(error.status + ' ' + error.valid);
            }
        });
    }
}
