from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy
from ..models import PaletaColores
from ..crum import *

def update_config_dashboards(request):
    paleta_colores_ = PaletaColores.objects.all()
    lista_paleta = [(fila.id, fila.name_paleta) for fila in paleta_colores_]
    configurador, id_paleta = get_config_dashboard()
    if request.method == 'POST':
        get_ticklabel_color = request.POST.get('ticklabel_color')
        get_ticklabel_size = request.POST.get('ticklabel_size')
        get_plot_bgcolor = request.POST.get('plot_bgcolor')
        get_paper_bgcolor = request.POST.get('paper_bgcolor')
        get_paleta_colores = request.POST.get('paleta_colores')
        get_showticklabels = request.POST.get('showticklabels')
        
        configurador.ticklabel_color = get_ticklabel_color
        configurador.ticklabel_size = get_ticklabel_size
        configurador.plot_bgcolor = get_plot_bgcolor
        configurador.paper_bgcolor = get_paper_bgcolor
        configurador.paleta_colores = PaletaColores.objects.get(id=int(get_paleta_colores))
        configurador.showticklabels = True if get_showticklabels == 'on' else False
        configurador.save()
        return redirect('update_config_dashboard')
    context={'paleta':lista_paleta,'config_dash':configurador, 'id_paleta' :  id_paleta}#'config_dash':configurador,
    return render(request, 'Formularios/modificar_config.html',context)#, {'form': form}
