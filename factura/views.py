from django.shortcuts import render, HttpResponse
from django.core import serializers
from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from .forms import FacturaFormulario
from .models import Producto, Cliente, DetalleFactura, Factura
from django.urls import reverse_lazy
# Create your views here.
import json
class ClienteView(TemplateView):
    template_name = 'factura/index.html'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Detalle cliente'
    #     return context
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'buscar_productos':
                data = []
                products = Producto.objects.filter(nom_producto__icontains=request.POST['term'])[0:10]
                #products_serializer = serializers.serialize('json', products)
                for i in products:
                    item = i.toJSON()
                    item["value"] = i.nom_producto
                    #print(item)
                    data.append(item)
            elif action == 'buscar_clientes':
                result = ''.join(filter(lambda i: i.isdigit(), request.POST['id_cliente']))
                id_ = str(result)
                clients = Cliente.objects.all().filter(id_cliente=id_)
                #print(clients)
                for i in clients:
                    cliente = i.toJSON()
                    data = cliente
            elif action == 'saveData':
                with transaction.atomic:
                    # save detallefactura
                    ventas = json.loads(request.POST['ventas'])
                   
                    # save factura
                    
                    cliente = Cliente.objects.get(pk=ventas['id_cliente'])
                    factura = Factura(id_cliente=cliente).save()
                    # save detalle -> Factura, Producto
                    venta = DetalleFactura()
                    f = Factura.objects.get(id_cliente=cliente)
                    venta.id_factura = f
                    for i in ventas['productos']:
                        venta.id_producto = Producto.objects.get(id_producto=i['id_producto'])
                        venta.cantidad = int(i['cant'])
                        venta.precio = float(ventas['total'])
                        venta.save()
                    #print(ventas)
                    #venta.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
   
    def get(self, request, *args, **kwargs):
        data = {
            'title': 'Detalle Cliente',
            'title_detalle': 'Detalle Factura 1',
            'clientes': Cliente.objects.all(),
            'productos': Producto.objects.all(),
            'action': 'saveData'
        }
        return render(request, self.template_name, data)

# class ProductListView(ListView):
#     model = Producto
#     template_name = 'factura/list.html'
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             data = Producto.objects.get(pk=request.POST['id']).toJSON()
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'producto'
#         return context
