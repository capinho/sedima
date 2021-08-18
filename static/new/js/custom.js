
$(document).ready(function(){

    // // Show the price according to selected size
    // $(".choose-size").on('click', function(){
    //     //$(".choose-size").removeClass('active');
    //     //$(this).addClass('active');
    //     var _price=$(this).attr('data-price');
    //     $(".product-price").text(_price);
	// 	var _size=$(this).attr('data-size');
	// 	$("#product-size").val(_size);
	// 	console.log(_size)
	// 	console.log(_price)

	
    // })
	$("#basic-form").validate({

		rules: {
			size : {
				required: true,
			},
		},
		messages : {
			size: {
				required: "Veuillz renseigner la taille du produit"
			}
		},
		
	});
	$("#submit").click(function(){
		$("#basic-form").submit();
		return false;
	});
	$("select")
	.change(function() {
	  $( "select option:selected" ).each(function() {
		var _price=$(this).attr('data-price');
		$(".product-price").text(_price);
	  });
	})
	.trigger("change");


	$("#showAlert").click(function() {
		$("#alert").toast("show");
	  });
	  
	$("#showSuccess").click(function() {
	$("#success").toast("show");
	});
	
	$("#showInfo").click(function() {
	$("#info").toast("show");
	});
			  
});


