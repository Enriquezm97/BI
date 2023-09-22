
import apps.graph.models as gm
import apps.users.models as um

def RegistrarIndicador(tipo,nombre,formula,desde1,hasta1,color1,desde2,hasta2,color2,desde3,hasta3,color3,comentario,favorito,empresa,id_usuario):
    #from home.models import Ratios
    TipoIndicador=gm.TipoIndicador
    Indicador=gm.Indicador()
    #Usuario=um.Usuario()
    #cliente.tipo_cliente = TipoCliente.objects.get(codigo = request.POST['tipo_cliente'])
    Indicador.indicador_tipo=TipoIndicador.objects.get(id=tipo)
    Indicador.name=nombre
    Indicador.formula=formula

    
    Indicador.rango_desde_1=desde1
    Indicador.rango_hasta_1=hasta1
    Indicador.rango_color_1=color1

    Indicador.rango_desde_2=desde2
    Indicador.rango_hasta_2=hasta2
    Indicador.rango_color_2=color2

    Indicador.rango_desde_3=desde3
    Indicador.rango_hasta_3=hasta3
    Indicador.rango_color_3=color3

    Indicador.indicador_comentario=comentario
    Indicador.indicador_favorito= favorito
    Indicador.dataframe=empresa
    Indicador.usuario=um.Usuario.objects.get(id=id_usuario)

    return Indicador.save()


def ActualizarIndicador(tipo,nombre,formula,desde1,hasta1,color1,desde2,hasta2,color2,desde3,hasta3,color3,comentario, pk_indicador):
    #Indicador=gm.Indicador()
    actualizar_indicador = gm.Indicador.objects.filter(id = pk_indicador)
    #.update(edad=30)
    actualizar_indicador.update(indicador_tipo=tipo)#=tipo#indicador_tipo
    actualizar_indicador.update(name=nombre)
    actualizar_indicador.update(formula=formula)

    
    actualizar_indicador.update(rango_desde_1=desde1)
    actualizar_indicador.update(rango_hasta_1=hasta1)
    actualizar_indicador.update(rango_color_1=color1)

    actualizar_indicador.update(rango_desde_2=desde2)
    actualizar_indicador.update(rango_hasta_2=hasta2)
    actualizar_indicador.update(rango_color_2=color2)

    actualizar_indicador.update(rango_desde_3=desde3)
    actualizar_indicador.update(rango_hasta_3=hasta3)
    actualizar_indicador.update(rango_color_3=color3)

    actualizar_indicador.update(indicador_comentario=comentario)
    return print("ACTUALIZADO")

def EliminarIndicador(pk_indicador):
    #Indicador=gm.Indicador()
    eliminar_indicador = gm.Indicador.objects.filter(id = pk_indicador)
    eliminar_indicador.delete()
    return print("ELIMINADO")