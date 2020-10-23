$(document).ready(function(){
    var tblProductos;
    // facturacion
    var ventas = {
        items: {
            id_cliente: '',
            cli: '',
            subtotal: 0.00,
            iva: 0.00,
            total: 0.00,
            productos: []
        },
        calcularFactura: function() {
            var subtotalProductos = 0.00;
            var iva = 0.12;
            $.each(this.items.productos, function(pos, dict) {
                dict.subtotal = dict.cant * parseFloat(dict.precio);
                subtotalProductos+=dict.subtotal;
            });
            this.items.subtotal = subtotalProductos;
            this.items.iva = this.items.subtotal * iva;
            this.items.total = this.items.subtotal + this.items.iva;
            $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
            $('input[name="iva"]').val(this.items.iva.toFixed(2));
            $('input[name="total"]').val(this.items.total.toFixed(2));
        },
        add: function(item) {
            this.items.productos.push(item);
            this.list();
        },
        list: function() {
            this.calcularFactura();
            tblProductos = $('#tabla1').DataTable({
                responsive: true,
                destroy: true,
                data: this.items.productos,
                columns: [
                    //{'data' : 'id_producto'},
                    {'data': 'nom_producto'},
                    {'data': 'precio'},
                    {'data': 'cant'},
                    {'data': 'subtotal'},
                    {'data': 'id'}
                ],
                columnDefs: [
                    {
                        targets: [1, 3],
                        class: 'text-center',
                        render: function(data, type, row) {
                            return '$'+parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [2],
                        class: 'text-center',
                        render: function(data, type, row) {
                            return '<input type="text" class="form-control form-control-sm" value="'+data+'" autocomplete="off" name="cantidad" id="cantidad">';
                        }
                    },
                    {
                        targets: [4],
                        class: 'text-center',
                        render: function(data, type, row) {
                            return '<a rel="remove" class="btn btn-danger btn-xs"><i class="fa fa-times-circle" aria-hidden="true"></i></a>';
                        }
                    },
                ]
            })
        },

    }

    $('.removeAll').on('click', function(){
        if(ventas.items.productos.length === 0) return false;
        $('#staticBackdrop').on('shown.bs.modal', function () {
            $('#btn-confirm').on('click', function(){
                ventas.items.productos = [];
                ventas.list();
                $("#staticBackdrop").modal('hide');
            });
            
          })
        
    })
    // input cantidad
    $('#tabla1 tbody')
        .on('click', 'a[rel="remove"]', function() {
            var tr = tblProductos.cell($(this).closest('td, li')).index();
            ventas.items.productos.splice(tr.row, 1);
            ventas.list();
        })
        .on('change keyup', 'input[name="cantidad"]', function(){
            var cant = parseInt($(this).val());
            var tr = tblProductos.cell($(this).closest('td, li')).index();
            // var data = tblProductos.row(tr.row).data();
            // var data = tblProductos.row(tr.row).node();
            ventas.items.productos[tr.row].cant = cant;
            ventas.calcularFactura();
            $('td:eq(3)', tblProductos.row(tr.row).node()).html('$'+ventas.items.productos[tr.row].subtotal.toFixed(2));
    });
  
    // Buscar Producto, autocomplete
    $(function() {
        
        $('input[name="search"]').autocomplete({
            source: function(request, response) {
                $.ajax({
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'buscar_productos',
                        'term': request.term,
                    },
                    dataType: 'json'
                }).done(function(data){
                    //console.log(data);
                    response(data);
                }).fail(function(data){
                    
                });
            },
            delay: 500,
            minLength: 1,
            select: function(event, ui) {
                event.preventDefault();
                //console.clear();
                ui.item.cant = 1;
                ui.item.subtotal = 0.00;
                ventas.add(ui.item);
                //console.log(ventas.items.productos.id_producto);
                $(this).val('');
            }
        });
    });
    

    // DataTable config
    $('#tabla1').DataTable({
        responsive: true,
        ordering: false,
        bFilter: false,
        paging: false
    });
    // List clientes from imput select
    $("#inputGroupSelect01").change(function(){
        var seleccion = $(this).val();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: 
            {
                'action': 'buscar_clientes',
                'id_cliente': seleccion
            },
            dataType: 'json',
        }).done(function(data){
            //console.log(data);
            ventas.items.cli = data.nom_cliente;
            ventas.items.id_cliente = data.id_cliente;
            $('#address').text(data.direccion);
            seleccion = '';
        })
        
        
    });
    // save data factura
    $('form').on('submit', function(e){
        //ventas.items.cli = $('#inputGroupSelect01')
        e.preventDefault();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('ventas', JSON.stringify(ventas.items));
        // for (var key of parameters.entries()) {
        //     console.log(key[0] + ', ' + key[1]);
        // }
        $.ajax({
            url: window.location.pathname,
            data: {
                'action': 'saveData',
                'ventas': JSON.stringify(ventas.items)
            },
            type: 'POST',
            success: function(response) {
                //console.log(response);
                
                //response()
            },
            error: function(error) {
                console.log(error);
            }
        });
        window.location.href = "/"
        
    })
    
    
});


