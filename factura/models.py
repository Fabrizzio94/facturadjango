from django.db import models

from django.forms import model_to_dict

# Cliente
class Cliente(models.Model):

    id_cliente = models.CharField("Cédula", max_length=10, primary_key=True)
    nom_cliente = models.CharField("Nombre", max_length=30)
    direccion = models.TextField("Dirección", blank=True, null=True)
    telefono = models.CharField("Telefono", max_length=10)

    class Meta:
        verbose_name="Cliente"

    def __str__(self):
        return self.nom_cliente
    def toJSON(self):
        client = model_to_dict(self)
        return client
class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name="Factura"
    def __str__(self):
        return str(self.id_factura)


class Producto(models.Model):
    id_producto = models.CharField("id_producto", max_length=30)
    nom_producto = models.TextField("Producto",blank=False, null=False)
    precio = models.DecimalField("Precio", default=0.00, max_digits=9, decimal_places=2)
    stock = models.PositiveIntegerField("Stock",default=0)
    class Meta:
        verbose_name="Producto"
    def __str__(self):
        return self.nom_producto
    def toJSON(self):
        item = model_to_dict(self)
        return item
    

class DetalleFactura(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    class Meta:
        verbose_name="DetalleFactura"
    def __str__(self):
        return self.id_detalle
