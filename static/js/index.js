$(document).ready(function(){
	$( "#goto" ).click(function() {
	  $( "#go" ).slideDown( "slow", function() {
		// Animation complete.
	  });
	});

	$("#btnFor2").click(function(){
		if ($("#etp2").css('display') == "none") {
			$("#etp2").show()
			$("#etp1").hide()
			$("#etp3").hide()
		} 
	});
	$("#btnBack2").click(function(){
		if ($("#etp1").css('display') == "none") {
			$("#etp1").show()
			$("#etp2").hide()
			$("#etp3").hide()
		} 
	});
	$("#btnFor3").click(function(){
		if ($("#etp3").css('display') == "none") {
			$("#etp3").show()
			$("#etp1").hide()
			$("#etp2").hide()
		} 
	});
	$("#btnBack2").click(function(){
		if ($("#etp1").css('display') == "none") {
			$("#etp1").show()
			$("#etp2").hide()
			$("#etp3").hide()
		} 
	});
	$("#btnBack3").click(function(){
		if ($("#etp2").css('display') == "none") {
			$("#etp2").show()
			$("#etp1").hide()
			$("#etp3").hide()
		} 
	});
});
