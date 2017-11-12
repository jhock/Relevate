/**
 * Created on 4/18/17.
 * This script handles the mobile preview of a created content dynamically.
 * As of the day of this scripts creation, we do not have a mobile version of the app.
    * Therefore the preview design does not necessarily reflect the actually mobile app once built.
    * This script should be agnostics of the html web design given that the
    * attribute name remains the same.
 */


$(document).ready(function() {

    $('#preview-modal-link').on({
        'beforeshow': function () {
            showLinkPreview();
        }
    })
    $('#preview-modal-info').on({
        'beforeshow': function () {
            showInfographicsPreview();
        }
    })
    $('#preview-modal-article').on({
        'beforeshow': function () {
            showArticlePreview();
        }
    });

    $("#id_image").change(function(){
        console.log("Image Loaded to Preview");
        readURL(this);
    });
    $("#id_contents").change(function(){
        console.log("Image Loaded to Preview");
        readURL(this);
    });
});
function todaysDate() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!
    var yyyy = today.getFullYear();

    if (dd < 10) {
        dd = '0' + dd
    }

    if (mm < 10) {
        mm = '0' + mm
    }

    today = mm + ':' + dd + ':' + yyyy;
    console.log(today);
    return today
}
function showLinkPreview(){
    /**
        Load user's input link data into mobile preview
     **/

    $("#preview_date").text(todaysDate());
        console.log("title hit");
        var content;
        var preview_length;
        var content_length;
        content = $("#id_title").val();
         $("#preview_title").text(content.substring(0, 100));
        content = $("#id_link").val();
         $("#preview_link").attr("href", content);

        $("#preview_content").empty();
        content_length =  CKEDITOR.instances['id_blurb'].getData().length;
        if(content_length > 200){
            preview_length = 196
        }else{
            preview_length = content_length - 4; // takes out the </p> from the string
        }
        content = CKEDITOR.instances['id_blurb'].getData().substring(3, preview_length);
        $("#preview_content").append(content.substring(0, preview_length));

        $("#topics_info").empty();
        var list_of_topics = 0;
        content = $('#id_topic_choices :checked');
        content.each(function () {
            if(list_of_topics > 3){
                return false;
            }
            list_of_topics += 1;
            var topic = $(this).parent().text();
            var val_html = "<a href='#'>"+topic+"</a>";
            $("#topics_info").append(val_html);
        });
        checkUpdateImage()
}
function showArticlePreview(){
    /**
        Load user's input article data into mobile preview
     **/
    $("#preview_date").text(todaysDate());
        console.log("title hit");
        var content;
        var preview_length;
        var content_length;
        content = $("#id_title").val();
        $("#preview_title").text(content.substring(0, 100));

        $("#preview_content").empty();
        content_length =  CKEDITOR.instances['id_content'].getData().length;
        if(content_length > 200){
            preview_length = 196
        }else{
            preview_length = content_length - 4; // takes out the </p> from the string
        }
        content = CKEDITOR.instances['id_content'].getData().substring(3, preview_length);
        $("#preview_content").append(content.substring(0, preview_length));

        $("#topics_info").empty();
        var list_of_topics = 0;
        content = $('#selected_item :checked');
        content.each(function () {
            if(list_of_topics > 3){
                return false;
            }
            list_of_topics += 1;
            var topic = $(this).parent().text();
            var val_html = "<a href='#'>"+topic+"</a>";
            $("#topics_info").append(val_html);
        });
        checkUpdateImage()
}
function showInfographicsPreview(){
    /**
        Load user's infographics data into mobile preview
     **/
    $("#preview_date").text(todaysDate());
        console.log("title hit");
        var content;
        var content_length;
        var preview_length;

        content = $("#id_title").val();
        $("#preview_title").text(content.substring(0, 100));

        $("#preview_content").empty();
        content_length =  CKEDITOR.instances['id_blurb'].getData().length;
        if(content_length > 150){
            preview_length = 146
        }else{
            preview_length = content_length - 4;
        }
        content = CKEDITOR.instances['id_blurb'].getData().substring(3, preview_length);
        $("#preview_content").append(content);


        $("#topics_info").empty();
        var list_of_topics = 0;
        content = $('#id_topic_choices :checked');
        content.each(function () {
            if(list_of_topics > 3){
                return false;
            }
            list_of_topics += 1;
            var topic = $(this).parent().text();
            var val_html = "<a href='#'>"+topic+"</a>";
            $("#topics_info").append(val_html);
        });
        checkUpdateImage();

}

function readURL(input) {
    /**
        * Load user's image data into mobile preview
     **/
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        console.log("loading picture");
        reader.onload = function (e) {
            $('#preview_image').attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}
function checkUpdateImage(){
    /**
     * For the update page. This checks if a file is already present.
    **/
    var src = $("#preview_image").attr('src');
    if(src=="#"){
        console.log("Checking Update's Page's Image");
        var src_ = $("#curr_image").attr('src');
        if(src_){
            $('#preview_image').attr('src', src_);
        }
    }
}