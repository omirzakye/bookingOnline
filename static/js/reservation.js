function addToOrder(itemId, bookingId, action){
	console.log('Adding to order')

	let url = '/add/'

	fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken': csrftoken,
			},
			body:JSON.stringify({'productId': itemId, 'action':action, 'bookingId': bookingId})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    console.log('data', data)
			location.reload()
		})
}