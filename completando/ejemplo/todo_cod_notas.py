##VERSION MEJORADA
import pandas as pd
#store municipios_snis
#municipios_snis.to_csv('completando/municipios_snis.csv', index=False)
# Carga el CSV en un DataFrame
tabla_incompleta = pd.read_csv('completando/2001_sospecha-diagnostica_tosferina.csv')
tabla_incompleta[:10]
# Convertir la columna "mes" a formato de fecha
tabla_incompleta['mes'] = pd.to_datetime(tabla_incompleta['mes'])

# Agregar columnas "año" y "departamento" basadas en la columna "mes"
tabla_incompleta['año'] = tabla_incompleta['mes'].dt.year
# Sumar los valores mensuales por municipio y año
tabla_sumada = tabla_incompleta.groupby(['codigo_municipio', 'municipio', 'grupo', 'variable','año']).sum().reset_index()

#cargando el CSV con la lista de departamentos y sus municipios
todos_municipios = pd.read_csv('completando/municipios_snis.csv')
# Renombrar las columnas para que coincidan con la tabla incompleta
todos_municipios = todos_municipios.rename(columns={'DEPARTAMENTO': 'departamento', 'COD_MUNICIPIO': 'codigo_municipio', 'MUNICIPIO': 'municipio'})
# Reorganizar las columnas para que "departamento" esté en la primera posición
todos_municipios = todos_municipios[['departamento', 'codigo_municipio', 'municipio']]


# Unir DataFrames y completar valores faltantes
tabla_completa = todos_municipios.merge(tabla_sumada, on=['codigo_municipio', 'municipio'], how='left')
tabla_completa['grupo'] = 'sospecha diagnostica'  # Asigna el nombre del grupo
tabla_completa['variable'] = 'tosferina'  # Asigna el nombre de la variable
tabla_completa['año'] = 2001  # Asigna el nombre de la variable

tabla_completa['grupo'] = tabla_incompleta['grupo'].unique()[0]  # Asigna el valor único de 'grupo' en tabla_incompleta
tabla_completa['variable'] = tabla_incompleta['variable'].unique()[0]  # Asigna el valor único de 'variable' en tabla_incompleta
tabla_completa['año'] = tabla_incompleta['año'].unique()[0]  # Asigna el valor único de 'año' en tabla_incompleta

# Rellena las columnas seleccionadas a partir del la sexta con 0 y las convierte a tipo entero
tabla_completa.iloc[:, 6:] = tabla_completa.iloc[:, 6:].fillna(0).astype(int)

# Guardar el DataFrame resultante como un archivo CSV
tabla_completa.to_csv('completando/tabla_completa.csv', index=False)

######
import pandas as pd

# Carga la tabla 2005 con los casos
tabla_2005 = pd.read_csv('ruta/tabla_2005.csv')

# Elimina los duplicados de la tabla 2005 en base al código de municipio
tabla_2005 = tabla_2005.drop_duplicates(subset=['COD_MUNICIPIO'])


# Carga la tabla de municipios con nombres y códigos
todos_municipios = pd.read_csv('completando/municipios_snis_corregido.csv')
# Realiza el merge usando how='left' para mantener todas las filas de tabla_2005
tabla_completa_2005 = todos_municipios.merge(tabla_2005, on=['codigo_municipio', 'municipio'], how='left')
tabla_completa_2005['grupo'] = tabla_2005['grupo'].unique()[0]  # Asigna el valor único de 'grupo' en tabla_incompleta
tabla_completa_2005['variable'] = tabla_2005['variable'].unique()[0]  # Asigna el valor único de 'variable' en tabla_incompleta
tabla_completa_2005['year'] = tabla_2005['year'].unique()[0]  # Asigna el valor único de 'año' en tabla_incompleta
tabla_completa_2005.iloc[:, 6:] = tabla_completa_2005.iloc[:, 6:].fillna(0).astype(int)


# Guarda el DataFrame resultante como un archivo CSV
tabla_completa_2005.to_csv('ruta/tabla_completa_2005.csv', index=False)



################""""
import pandas as pd
from translate import translate

df = pd.DataFrame({
    "columna_1": ["hola", "hola", "hola"],
    "columna_2": ["adios", "adios", "adios"]
})

# Obtenemos una lista de los valores únicos de cada columna
valores_unicos_1 = df["columna_1"].unique()
valores_unicos_2 = df["columna_2"].unique()

# Creamos diccionarios que mapean los valores originales a los valores traducidos
diccionario_1 = {
    "hola": "hello"
}
diccionario_2 = {
    "adios": "goodbye"
}

# Aplicamos la función de traducción a cada columna
df["columna_1"] = df["columna_1"].apply(lambda x: diccionario_1.get(x, x))
df["columna_2"] = df["columna_2"].apply(lambda x: diccionario_2.get(x, x))

print(df)
####

import pandas as pd
from IPython.display import clear_output

def completando1 (indice_tab, municipios):
    errores = []
    len_seleccion = len(indice_tab)
    translated_filenames = []  # Lista para almacenar los nombres de archivo traducidos
    
    for i, f in enumerate(indice_tab.filename):
        clear_output(wait=True)
        print('{} / {}'.format(i+1, len_seleccion))
        try:
            dfi = pd.read_csv('{}'.format(f))
            
            #traduzco
            dfi = dfi.rename(columns={'codigo_municipio':'code_municipality', 'municipio' :'municipality', 'grupo':'group' })
            # Convertir la columna "mes" a formato de fecha
            dfi['mes'] = pd.to_datetime(dfi['mes'])
            # Agregar columnas "año" y "departamento" basadas en la columna "mes"
            dfi['year'] = dfi['mes'].dt.year
            # Sumar los valores mensuales por municipio y año
            dfi_sumado = dfi.groupby(['code_municipality', 'municipality', 'group', 'variable','year']).sum().reset_index()
            
            #traduciendo grupo 
            valores_unicos = dfi_sumado["group"].unique()
            valores_unicos
            # Creamos un diccionario que mapea los valores originales a los valores traducidos
            grupo_dict = {
                            "clasificacion general sistemica": "systemic classification",
                            "sospecha diagnostica": "diagnostic suspicion",
                            "inmunoprevenibles": "immunization preventable",
                            "otras infecciones": "other infections",
                            "tuberculosis (casos confirmados)": "tuberculosis confirmed cases",
                            "mortalidad en el establecimiento ( leatalidad)": "institutional mortality lethality",
                            "enfermedades metaxenicas": "metazoan diseases",
                            "tuberculosis": "tuberculosis",
                            "mortalidad institucional": "institutional mortality"
                        }
               
            # Aplicamos la función de traducción a la columna
            dfi_sumado["group"] = dfi_sumado["group"].apply(lambda x: grupo_dict.get(x, x))
            
            #traduciendo variable
            valores_unicos = dfi_sumado["variable"].unique()
            valores_unicos
            # Creamos un diccionario que mapea los valores originales a los valores traducidos
            
            variables_dict = {
                "enfermedades del ojo y anexos": "eye and adnexal diseases",
                "enfermedades del sistema cardio circulatorio": "cardiovascular system diseases",
                "enfermedades del sistema respiratorio": "respiratory system diseases",
                "tosferina": "whooping cough",
                "difteria": "diphtheria",
                "fiebre hemorragica": "hemorrhagic fever",
                "hantavirus": "hantavirus",
                "tosferina (3*)": "whooping cough 3",
                "difteria (4*)": "diphtheria 4",
                "neumonia": "pneumonia",
                "sintomatico respiratorio": "respiratory symptomatic",
                "fiebre hemorragica (13*)": "hemorrhagic fever 13",
                "enfermedad respiratoria hanta (14*)": "Hanta respiratory disease 14",
                "tuberculosis pulmonar baar (+) nuevos": "pulmonary tuberculosis smear positive new cases",
                "tuberculosis pulmonar baar (-)": "pulmonary tuberculosis smear negative",
                "tuberculosis pulmonar baar (+) prevamente tratados": "pulmonary tuberculosis smear positive previously treated",
                "tuberculosis pulmonar baar + nuevos":"pulmonary tuberculosis smear positive new cases",
                "tuberculosis pulmonar baar - nuevos":"pulmonary tuberculosis smear negative new cases",
                "muerte menor de 5 anos por neumonia": "under 5 mortality due to pneumonia",
                "muerte por malaria (p. falciparum)": "mortality due to malaria plasmodium falciparum",
                "malaria": "malaria",
                "leishmaniasis": "leishmaniasis",
                "enfermedades de chagas aguda": "acute Chagas disease",
                "ira sin neumonia": "acute respiratory infection without pneumonia",
                "fiebre hemorrag. bol": "Bolivian hemorrhagic fever",
                "enfer. por hanta virus": "hantavirus disease"
            }


            # Aplicamos la función de traducción a la columna
            dfi_sumado["variable"] = dfi_sumado["variable"].apply(lambda x: variables_dict.get(x, x))

            #agregando municipios faltantes
            dfi_com = municipios.merge(dfi_sumado, on=['code_municipality', 'municipality'], how='left')
            dfi_com['group'] = dfi_sumado['group'].unique()[0]  # Asigna el valor único de 'grupo' en tabla_incompleta
            dfi_com['variable'] = dfi_sumado['variable'].unique()[0]  # Asigna el valor único de 'variable' en tabla_incompleta
            dfi_com['year'] = dfi_sumado['year'].unique()[0]  # Asigna el valor único de 'año' en tabla_incompleta
            dfi_com.iloc[:, 6:] = dfi_com.iloc[:, 6:].fillna(0).astype(int)

            # Guardar el archivo con nombre traducido en la carpeta "completando"
            translated_filename = '{}_{}_{}.csv'.format(
                dfi_sumado['year'].unique()[0],
                dfi_sumado['group'].unique()[0].replace(' ', '_'),
                dfi_sumado['variable'].unique()[0].replace(' ', '_')
            )
            dfi_com.to_csv('completando/{}'.format(translated_filename), index=False)
            
            # Agregar el nombre de archivo traducido a la lista
            translated_filenames.append(translated_filename)
            
            # Crear el DataFrame para el nuevo índice y guardarlo como archivo CSV
            indice_new = pd.DataFrame({
                'year': [name.split('_')[0] for name in translated_filenames],
                'filename': ['completando/' + name for name in translated_filenames],
                'group': [name.split('_')[1] for name in translated_filenames],
                'subvar': indice_tab.iloc[i].subvar,  # Usar el valor de subvar de la fila actual
                'variable': [name.split('_')[2].split('.')[0] for name in translated_filenames]
            })
            indice_new.to_csv('completando/indice_new.csv', index=False)
    
        except Exception as e:
            errores.append({'filename': f, 'error': e})

    return errores
######################
