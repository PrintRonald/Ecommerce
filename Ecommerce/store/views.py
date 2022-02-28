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


# Creando las vistas de la aplicación
def store(request):
	# renderizamos los productos registrados en nuestro modelos
	# para mostrarlos en nuestras vistas 
	products = Product.objects.all()
	context = {'products':products}
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
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# se seleccionan todos los articulos del carrito
		items = order.orderitem_set.all()
	else:
		# si el usuario no está registrado se mostrara una lista vacia llamada elementos
		# Create empty cart for now for non-logged in user
		items = []
		# creamos un objeto vacío para el usuario no registrado, configurados en 0
		order = {'get_cart_total':0, 'get_cart_items':0}

	context = {'items':items, 'order':order}
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
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# se seleccionan todos los articulos del carrito
		items = order.orderitem_set.all()
	else:
		# creamos un objeto vacío para el usuario no registrado, configurados en 0
		order = {'get_cart_total':0, 'get_cart_items':0}
		# si el usuario no está registrado se mostrara una lista vacia llamada elementos
		# Create empty cart for now for non-logged in user
		items = []
	
	context = {'items':items, 'order':order}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	return JsonResponse('Item was added', safe=False)