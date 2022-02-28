/*
agregando controladores de evento
Creamos la variable updteBtns que contiene la etiqueta button del archivo store.html
*/
var updateBtns = document.getElementsByClassName('update-cart')
/*
con un ciclo for recorremos hasta encontrar el producto que hemos hecho click
para agregarlo al carrito
identificamos el producto, la accion y si el usuario está o no registrado
*/
for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
    
        console.log('USER:', user)
		if (user == 'AnonymousUser'){
			console.log('User is not authenticated')
			
		}else{
			updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    console.log('Data:', data)
		});
}