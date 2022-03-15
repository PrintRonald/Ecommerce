from django.shortcuts import render
# shortcuts nos permite usar funciones auxiliares y clases que abarcan
# varios niveles del modelo vista controlador
# render combina una plantilla dada cn un dicc de contexto dado y devuelve
# un httpresponse objeto con ese texto representado
from django.shortcuts import render
# http usa objetos de solicitud y respuesta para pasar el estado a través del sistema
# en este caso obtenemos un Json
from django.http import JsonResponse
# importamos todo del archivo modelo
from .models import *
# importamos json para traer los datos y analizarlos
import json
import datetime 


# Creando las vistas de la aplicación
def store(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		#Crear carrito vacío por ahora para usuarios no registrados
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
	# renderizamos los productos registrados en nuestro modelos
	# para mostrarlos en nuestras vistas
	products = Product.objects.all()
	context = {'products': products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	# verificamos que el usuario se haya registrado
	if request.user.is_authenticated:
		# si esta registrado
		# instanciamos al usuario registrado
		customer = request.user.customer
		# el usuario crea la orden usando el metodo get_or_create(default=none, **kwargs)
		# conveniente para buscar objetos con el dado kwards, devuelve una tupla (object, created)objectcreated
		# esto sirve para que no se creen objetos duplicados cuando las solicitudes se hacen en paralelo
		order, created = Order.objects.get_or_create(
		    customer=customer, complete=False)
		# se seleccionan todos los articulos del carrito
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		# los usuarios que visitan por primera vez el sitio 
		# veran un error para evitarlo creamos esta excepción
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}
			print('CART:', cart)
		# si el usuario no está registrado se mostrara una lista vacia llamada elementos
		# Create empty cart for now for non-logged in user
		items = []
		# creamos un objeto vacío para el usuario no registrado, configurados en 0
		order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
		cartItems = order['get_cart_items']
		# para ver el total de articulos del visitante en su carrito
		for i in cart:
			cartItems += cart[i]['quantity']

	context = {'items': items, 'order': order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)


def checkout(request):
		# verificamos que el usuario se haya registrado
	if request.user.is_authenticated:
		# si esta registrado
		# instanciamos al usuario registrado
		customer = request.user.customer
		# el usuario crea la orden usando el metodo get_or_create(default=none, **kwargs)
		# conveniente para buscar objetos con el dado kwards, devuelve una tupla (object, created)objectcreated
		# esto sirve para que no se creen objetos duplicados cuando las solicitudes se hacen en paralelo
		order, created = Order.objects.get_or_create(
		    customer=customer, complete=False)
		# se seleccionan todos los articulos del carrito
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		# si el usuario no está registrado se mostrara una lista vacia llamada elementos
		# Create empty cart for now for non-logged in user
		items = []
		# creamos un objeto vacío para el usuario no registrado, configurados en 0
		order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
		cartItems = order['get_cart_items']
		

	context = {'items': items, 'order': order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)


def updateItem(request):
	# asignamos a la variable data la solicitud de datos para transformarla
	# de json a dicc
	data = json.loads(request.body)
	# asiganamos a productId y action los datos recopilados 
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)
	# instanciamos al cliente registrado
	customer = request.user.customer
	# el metodo get nos devuelve un objeto que coincide con los parametros de búsqueda 
	# proporcionados, que deben tener el formato de busqueda de campo ( es la forma 
	# de especificar una formato WHERE clausula SQL)
	product = Product.objects.get(id=productId)
	# obtenemos la orden creada, con get_or_created creamos una instancia de customer y lo
	# obtenemos de la base de datos ya que el argumento bool esta definido como falso
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	# luego para modificar los items hacemos lo mismo que el paso anterior pero referente 
	# a la orden creada y el producto que se desea agregar o modificar
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
	# luego si la accion es agregar, sumamos un item a orderItem
	# de caso contrario se resta
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	# se registra la accion 
	orderItem.save()
	# si la orderItem es menor que 0 se elimina de la misma
	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	# para identificar el id de la transacción utilizamos una marca de tiempo
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id
		# ejecutamos una comparacíon entre total enviado y total carrito
		if total == order.get_cart_total:
			order.complete = True
		order.save()
		# si se envia una direccion de envío creamos una instancia de direccion
		if order.shipping == True:
			ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
	else:
		print('User is not logged in')
	return JsonResponse('Pyment subbmitted...', safe=False)
