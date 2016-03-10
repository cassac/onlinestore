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
	$('#submitOrder').attr("disabled", true);
	$('#loading').show();
	$('#shippingRatesMenu').hide();
}).ajaxStop(function(){
	$('#submitOrder').attr("disabled", false);
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

// using jQuery
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
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('#submitOrder').on('click', function(e){
	e.preventDefault();
	var totalPrice = $('#totalPrice').text();
	var selectedShippingPrice = $('#shippingRatesMenu').find(":selected").attr('data-price');
	var selectedShippingID = $('#shippingRatesMenu').find(":selected").val();
	console.log('order submitted');
	console.log(totalPrice, selectedShippingPrice, selectedShippingID);

	$.ajax({
		url:'/mycart/',
		type: 'PUT',
		contentType: 'application/json;charset=UTF-8',
  		dataType: "json",
  		data: JSON.stringify({'rate': selectedShippingPrice, 'rate_id': selectedShippingID}),
  		success: function(r) {
  			console.log(r);
  		},
  		error: function(r) {
  			console.log(r);
  		}	
	})// end ajax

})