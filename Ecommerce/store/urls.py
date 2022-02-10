
from django.urls import path
from . import views
# importamos static para mostrar las imagenes en pantalla
from django.conf.urls.static import static
from django.conf import settings
# creando las rutas para nuestras Vistas

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)