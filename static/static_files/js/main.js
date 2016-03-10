var parseShippingRates = function(ratesArray) {
	console.log(ratesArray);
	var listHTML = '';
	$.each(ratesArray, function(index, value) {
		console.log(index, value);
		item = "<option value="+value.rate_id+">"+ index + " "+value.rate +" "+value.currency + "</option>";
		listHTML += item;
	});
	console.log(listHTML);
	$('#shippingRatesMenu').append(listHTML);
}

$(document).ajaxStart(function(){
	$('#loading').show();
	$('#shippingRatesMenu').hide();
}).ajaxStop(function(){
	$('#loading').hide();
	$('#shippingRatesMenu').show();
});



var getShippingRates = function(){

	// setToken();
	$.ajax({
		url:'/shipping/rates/',
		type: 'GET',
		contentType: 'application/json;charset=UTF-8',
  		dataType: "json",
  		statusCode: {
  			302: function(xhr) {
  				var json = JSON.parse(xhr.responseText);
  				var url = json.redirect_to;
  				window.location = url;
  			}
  		},
  		success: function(data){
  			console.log(data)
  			parseShippingRates(data);
  		},
  		error: function(error){
  			console.log(error);
  		} 
	}) // end ajax

}

$(document).ready(function(){
	$('#updateBtn').hide();
	$('input[type="number"]').on('change', function(){
		$('#updateBtn').show();
	});


	getShippingRates();

});