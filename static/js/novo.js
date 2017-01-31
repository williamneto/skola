function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$(document).ready(function(){
  $("#get-location").click(function(){
        var map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: -34.397, lng: 150.644},
          zoom: 18
        });
        var infoWindow = new google.maps.InfoWindow({map: map});

        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('Location found.');
            map.setCenter(pos);

            showForm(pos)

          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }

        function showForm(pos) {
          $(".add-pd-form").css("visibility", "visible");
          
          $("#id_localizacao_0").val(pos.lat);
          $("#id_localizacao_1").val(pos.lng);
        }

        function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        	infoWindow.setPosition(pos);
        	infoWindow.setContent(browserHasGeolocation ?
            	                  'Error: The Geolocation service failed.' :
                	              'Error: Your browser doesn\'t support geolocation.');
      	}


	});

  $("#id_img").change(function(){
    if (document.getElementById("id_img").files[0]) {
      img = document.getElementById("id_img").files[0];
      var reader = new FileReader();

      reader.onload = function (e) {
          $('#preview-foto').attr('src', e.target.result);
      }

      reader.readAsDataURL(img);
    }
  });

  $('#btn_enviar').click(function(){
    if (document.getElementById("id_img").files[0] && $("#id_legenda").val() && $("#id_tags").val()){
      fotoData = {
        "img": document.getElementById("id_img").files[0],
        "legenda": $("#id_legenda").val(),
        "tags": $("#id_tags").val()
      };

      podraoData = {
        "lat": $("#id_localizacao_0").val(),
        "lng": $("#id_localizacao_1").val(),
        "nome": $("#id_nome").val(),
        "bairro": $("#id_bairro").val()
      };

      data = {
        foto_data: fotoData,
        podra_data: podraoData,
      };

      var formData = new FormData()
      formData.append("img", document.getElementById("id_img").files[0]);
      formData.append("legenda", $("#id_legenda").val());
      formData.append("tags", $("#id_tags").val());
      formData.append("lat", $("#id_localizacao_0").val());
      formData.append("lng", $("#id_localizacao_1").val());
      formData.append("nome", $("#id_nome").val());
      formData.append("bairro", $("#id_bairro").val());


      $.ajaxSetup({ 
           beforeSend: function(xhr, settings) {
               function getCookie(name) {
                   var cookieValue = null;
                   if (document.cookie && document.cookie != '') {
                       var cookies = document.cookie.split(';');
                       for (var i = 0; i < cookies.length; i++) {
                           var cookie = jQuery.trim(cookies[i]);
                           // Does this cookie string begin with the name we want?
                           if (cookie.substring(0, name.length + 1) == (name + '=')) {
                               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                               break;
                           }
                       }
                   }
                   return cookieValue;
               }
               if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                   // Only send the token to relative URLs i.e. locally.
                   xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
               }
           } 
      });
     
      $.ajax({
        url: ".",
        type: "POST",
        data: formData,
        mimeTypes:"multipart/form-data",
        contentType: false,
        processData: false,
        success: function(data){
          if (data.status == 1){
            alert("Enviado com successo!!")
          }
        }
      });
    }
  });

  $("#next-2").click(function(){
    if ($("#id_bairro").val() != "" && $("#id_nome").val() != "") {
        $("#etapa-1").css("display", "none");
        $("#etapa-2").css("display", "block");
    
        $("#marc-1").css("display", "none");
        $("#marc-2").css("display", "block");
    }else{
      alert();
    }
  });
});