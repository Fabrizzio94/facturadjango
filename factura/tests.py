from django.test import TestCase
from .models import DetalleFactura, Producto, Factura, Cliente
# Create your tests here.
#c = Cliente.objects.all().filter(id_cliente='172337375')
c = Cliente.objects.get(pk='172337375')
#p = Producto.objects.filter(id_producto='1')
##f = Factura.objects.get(id_cliente=c)
f = Factura.objects.filter(id_cliente=c).values()
#fact = f.objects.all()
print('------------------k')
lis = []
for i in f:
    lis.append(i['id_factura'])
    #print(i['id_factura'])
print(lis)







#f = Factura(id_cliente=c.first())
#f = Factura.objects.get(pk=1)
#r = DetalleFactura.objects.get(pk='1')
#f.delete()
# f1 = Factura.objects.get(pk=1)
# #f.save()
# r = DetalleFactura(id_factura=f1, id_producto=p.first(),cantidad=4,precio=0.80)

# r.save()