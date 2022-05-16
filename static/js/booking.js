// function addToCart(item, action, bookingID, user){
//     var itemId = item;
// 	var action = action;
// 	var bookingId = bookingID;
// 	console.log('itemId:', itemId, 'Action:', action, 'bookingId:', bookingId)
// 	console.log('USER', user)
// 	if (user === 'AnonymousUser'){
// 		console.log('Not logged in')
// 		//addCookieItem(itemId, action)
// 	}else
// 		updateUserOrder(itemId, action, bookingId)
// }
//
// function updateUserOrder(itemId, action, bookingId){
// 	console.log('User is authenticated for cart, sending data...')
//
// 		var url = 'order/add'
//
// 	fetch(url, {
// 			method:'POST',
// 			headers:{
// 				'Content-Type':'application/json',
// 				'X-CSRFToken': csrftoken,
// 			},
// 			body:JSON.stringify({'productId': itemId, 'action':action, 'bookingId': bookingId})
// 		})
// 		.then((response) => {
// 		   return response.json();
// 		})
// 		.then((data) => {
// 		    console.log('data', data)
// 			location.reload()
// 		})
// }