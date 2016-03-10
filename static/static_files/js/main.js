var addShippingPrice = function(price) {
	$('#shippingPrice').html(price);
	var preTotal = $('#subTotal').attr('data-subtotal');
	var preTotalWithShipping = parseFloat(preTotal) + parseFloat(price);
	var newTotal = preTotalWithShipping.toFixed(2);
	$('#totalPrice').html(newTotal);
}

$(document).on('change', '#shippingRatesMenu', function(event){
	var newPrice = $('#shippingRatesMenu').find(":selected").attr('data-price');
	addShippingPrice(newPrice);
})

var parseShippingRates = function(ratesArray) {
	var listHTML = '';
	$.each(ratesArray, function(index, value) {
		item = "<option data-price="+ value.rate +" value="+value.rate_id+">"+ index + " "+value.rate +" "+value.currency + "</option>";
		listHTML += item;
	});
	$('#shippingRatesMenu').append(listHTML);
	addShippingPrice(ratesArray['First Class'].rate);
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
  			parseShippingRates(data);
  		},
  		error: function(error){
  			// console.log(error);
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

$('#submitOrder').on('click', function(e){
	e.preventDefault();
	console.log('order submitted');
})