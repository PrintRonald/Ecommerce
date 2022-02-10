from django.shortcuts import render
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
	context = {}
	return render(request, 'store/cart.html', context)

def checkout(request):
	context = {}
	return render(request, 'store/checkout.html', context)