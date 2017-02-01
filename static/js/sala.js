$(document).ready(function(){
	
	$("#submit").click(function(){
		var tema = $("#id_tema").val()
		var cont = {
			"tema": tema,
			"cont": $("#id_cont").val(),
			"usr": $("#usr_field").val()
		}
		
		data = {'data': JSON.stringify(cont)}
		$.ajax({
        	url: ".",
        	type: "GET",
        	data: data,
        	success: function(data){
        	  $("#id_cont").val("")
        	  $("#id_tema").val("")
        	}
     	});

	});

	$(".tems").click(function(){
		$("#id_tema").val($(this).text())
	});

	$('#conts').on('click', '.tems-c', function() {
		data = {"update-conts": $(this).text() }
		$.ajax({
        	url: ".",
        	type: "GET",
        	data: data,
        	success: function(data){
        	  $("#conts").html(data)
        	}
     	});
	});

	$('#conts').on('click', '.btnApv', function() {
		var i = parseInt($(this).val()) - 1
		data = {"avl": "apv", "cont":  i}
		$.ajax({
        	url: ".",
        	type: "GET",
        	data: data,
        	success: function(data){
				if ( data['fail'] ){
					alert(data['fail'])
				} else {
					i = i + 1
					$("#modal-content-"+i).attr('class', data['color'] + '-2 modal-content')
					$("#"+i).attr('class', data['color'])
				}
        	}
     	});
	});
	$("#conts").on('click', 'article', function(){
		$("#mod-"+$(this).attr("id")).modal('show')
	})
	$('#conts').on('click', '.btnRep', function() {
		var i = parseInt($(this).val()) - 1
		data = {"avl": "rep", "cont":  i}
		$.ajax({
        	url: ".",
        	type: "GET",
        	data: data,
        	success: function(data){
				if ( data['fail'] ){
					alert(data['fail'])
				} else {
					i = i +1
					$("#modal-content-"+i).attr('class', data['color'] + '-2 modal-content')
					$("#"+i).attr('class', data['color'])
				}
        	}
     	});
	});


	$("#btnCont").click(function(){
		if ($("#vid").css('display') == "none") {
			$("#vid").show()
			$("#deb").hide()
			$("#conts").hide()
		} 
	});
	$("#btnEsc").click(function(){
		if ($("#deb").css('display') == "none") {
			$("#deb").show()
			$("#vid").hide()
			$("#conts").hide()
		} 
	});
	$("#btnConts").click(function(){
		if ($("#conts").css('display') == "none") {
			$("#conts").show()
			$("#deb").hide()
			$("#vid").hide()

			data = {"update-conts": "Todos" }
			$.ajax({
	        	url: ".",
	        	type: "GET",
	        	data: data,
	        	success: function(data){
	        	  $("#conts").html(data)
	        	}
	     	});
		} 
	});
});
