
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
