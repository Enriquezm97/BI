from celery import shared_task
from apps.graph.test.utils.frame import Column, Row, Div, Store, Download, Modal,Modal
from ..graph.build.containers.index import card_index
@shared_task()
def row_index(rubro):
    if rubro == 'Comercial':
        row = Row([
                
                Column([
                    card_index(img = "finanzas.jpeg",title_card= "Estado de Resultados",url='estado-resultados')
                ], size=3),
                Column([
                    card_index(img = "ventas.png",title_card= "Ventas Clientes", url= 'comercial-cliente')
                ], size=3),
                Column([
                    card_index(img = "inventario.jpeg",title_card= "Inventarios", url= 'inventario')
                ], size=3),
            ])
    else :
        row = Row([
                Column([
                    card_index(img = "agricola.jpg",title_card= "Costos Agrícola", url='costos-campaña')
                ], size=3),#apps/graph/build/containers/assets/agricola.png
                Column([
                    card_index(img = "finanzas.jpeg",title_card= "Estado de Resultados",url='estado-resultados')
                ], size=3),
                Column([
                    card_index(img = "ventas.png",title_card= "Ventas Clientes", url= 'comercial-cliente')
                ], size=3),
                Column([
                    card_index(img = "inventario.jpeg",title_card= "Inventarios", url= 'inventario')
                ], size=3),
            ])
    return row