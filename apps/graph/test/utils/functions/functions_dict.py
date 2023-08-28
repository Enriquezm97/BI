

def extraer_list_value_dict(dict_input = {}, dict_componentes ={}, tipe_value = 'componente', for_title = False):
        lista_values= []
        if for_title == False:
            if tipe_value == 'id':
                for key, value in dict_input.items():
                    if key != 'Moneda':
                        lista_values.append(dict_componentes[key][value['tipo_componente']][tipe_value])
            else :
                for key, value in dict_input.items():
                        lista_values.append(dict_componentes[key][value['tipo_componente']][tipe_value])
        else :
            for key, value in dict_input.items():
                        lista_values.append(dict_componentes[key][value['tipo_componente']][tipe_value])
        return lista_values