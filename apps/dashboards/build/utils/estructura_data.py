import pandas as pd

columns_drop_nsp_rpt_ventas_detallado = [
        'DOCUMENTO','IDCLIEPROV','MONEDA','TCAMBIO','PROYECTO','TCMONEDA','IDPRODUCTO','IDMEDIDA','VENTANA','IDCOBRARPAGARDOC', 
        'IDSERIE', 'UNDEX', 'EQUIVALENCIA','idtipocontenedor', 'idtipoprecio', 'DSC_PUERTODESTINO', 'DUA', 'glosa','IDCANAL',
        'CANAL', 'Lotep', 'ocompra','nro_contenedor','idconsumidor', 'IDCAMPANA', 'CONTADO', 'vencimiento'
    ]

columns_nsp_rpt_ventas_detallado = {
                                'SUCURSAL': 'Sucursal',
                                'FECHA': 'Fecha',
                                'RAZON_SOCIAL': 'Cliente',
                                'VENDEDOR':'Vendedor',
                                'TIPOMOVIMIENTO':'Tipo de Movimiento',
                                'TIPOVENTA': 'Tipo de Venta',
                                'CONDICION': 'Tipo de Condicion',
                                'DESCRIPCION': 'Producto',
                                'GRUPO': 'Grupo Producto',
                                'SUBGRUPO': 'Subgrupo Producto',
                                'MARCA': 'Marca Producto',
                                'CANTIDAD': 'Cantidad',
                                'PRECIOMOF':'P.U Soles',
                                'PRECIOMEX':'P.U Dolares',
                                'VVENTAMOF': 'Subtotal Soles',
                                'VVENTAMEX': 'Subtotal Dolares',
                                'IMPORTEMOF': 'Importe Soles',
                                'IMPORTEMEX': 'Importe Dolares',
                                'NroEmbarque': 'Número de Embarque',
                                'FechaEmbarque': 'Fecha de Embarque',
                                'PESONETO_PRODUCTO': 'Peso Producto', 
                                'DEPARTAMENTO': 'Departamento',
                                'PROVINCIA': 'Provincia', 
                                'DISTRITO': 'Distrito', 
                                'PAIS': 'Pais',
                                'CULTIVO': 'Cultivo', 
                                'VARIEDAD': 'Variedad', 
                                'FORMATO': 'Formato', 
                                'GRUPOCLIENTE': 'Grupo Cliente'
                                }

columns_nsp_stocks = {
                     'dsc_producto':'Producto',
                     'dsc_grupo': 'Grupo Producto',
                     'dsc_subgrupo': 'Sub Grupo Producto',
                     'unid_medida': 'Unidad de medida',
                     'stock_unidades':'Stock en unidades',
                     'costo_unitario_mof':'Costo Unitario Soles',
                     'costo_unitario_mex':'Costo Unitario Dolares',
                     'stock_valorizado_mof':'Stock Valorizado Soles',
                     'stock_valorizado_mex':'Stock Valorizado Dolares',
                     'año':'Año',
                     'mes':'Mes_',
                     'venta_prom_unidades':'Venta prom 12 meses en UN',
                     'venta_prom_mof':'Venta prom 12 meses en monto Soles',
                     'venta_prom_mex':'Venta prom 12 meses en monto Dolares',
                     'costo_venta_prom_mof':'Costo de Venta prom 12 meses en monto Soles',
                     'costo_venta_prom_mex':'Costo de Venta prom 12 meses en monto Dolares',
                     'ABC_ventas':'ABC Ventas',
                     'ABC_stock':'ABC Stock',
                     'rango_antiguedad_stock':'Rango antigüedad del stock',
                     'rotacion':'Rotación',
                     'meses_stock': 'Meses de stock',
                     
          }

columns_nsp_stockalmval = {
        'CODSUCURSAL': 'Código Sucursal', 
        'SUCURSAL'   : 'Sucursal',
        'CODALMACEN' : 'Código Almacén',
        'ALMACEN'    : 'Almacén',
        'codtipo'    : 'Código Tipo',
        'tipo'       : 'Tipo',
        'CODGRUPO'   : 'Código Grupo',
        'GRUPO'      : 'Grupo',
        'CODSUBGRUPO': 'Código Sub Grupo',
        'SUBGRUPO'   : 'Sub Grupo',
        'CODPRODUCTO': 'Código Producto',
        'PRODUCTO'   : 'Producto',
        'GRUPO2'     : 'Grupo 2',
        'RESPONSABLEINGRESO' : 'Responsable Ingreso',
        'RESPONSABLESALIDA'  : 'Responsable Salida',
        'MEDIDA'     : 'Unidad de Medida',
        'ESTADO'     : 'Estado',
        'STOCK'      : 'Stock',
        'IMPORTETOTALMOF' : 'Importe Soles',
        'IMPORTETOTALMEX' : 'Importe Dolares',
        'UBICACION'  : 'Ubicación',
        'ULTFECHAINGRESO' : 'Última Fecha Ingreso',
        'ULTFECHASALIDA'  : 'Última Fecha Salida',
        'MARCA'      : 'Marca',
        'TIPOMATERIAL': 'Tipo de Material',
        'desde'      : 'Desde',
        'hasta'      : 'Hasta'
    }