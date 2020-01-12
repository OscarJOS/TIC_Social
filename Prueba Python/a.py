import pandas as pd
from cerberus import Validator
from datetime import date

#lee la linea de control
df_header = pd.read_csv('1234567892905201801.txt', sep='|', nrows=1, header=None, usecols=range(1,4))
#pasa la segunda columna a datetime
df_header[2] =  pd.to_datetime(df_header[2])
#Creo el diccionario y accedo al diccionario dentro del diccionario
data_dict = df_header.to_dict('index')
data_dict = data_dict[0]
#Validaciones
header_schema = {   1 : {'type': 'integer', 'min': 100000000, 'max': 999999999},
                    2 : {'type': 'date'},
                    3 : {'type': 'integer'}}
header_validator = Validator(header_schema)

header_results = header_validator.validate(data_dict)
header_errors = header_validator.errors

def errors(x, y):
    if x == True:
        return "Sin errores"
    else:
        return y

header_final = ("Linea de control",":", header_results, errors(header_results, header_errors))

def validations(x):
    #Verifica que el tipo de doc sea CC, TI o CE
    def t_doc(field, value, error):
        t_doc_list = ['CC', 'TI', 'CE']
        if not value in t_doc_list:
            error(field, "Valores permitidos(CC,TI,CE)")
    #Verifica rango de fechas
    def check_date(field, value, error):
        max_date = date.today()
        range_date = pd.date_range(start='1920-01-01', end = max_date)
        if not value in range_date:
            error(field, "Fecha no validas")
    #Verifica género
    def check_genre(field, value, error):
        genre_list = ['M', 'F']
        if not value in genre_list:
            error(field, "Valores permitidos(M ó F)")
    #Verifica estado de gestación
    def check_pregnancy(field, value, error):
        pregnancy_list = [1, 2, 3]
        if not value in pregnancy_list:
            error(field, "Valores permitidos(1, 2 ó 3)")
        genre = data_dict_users_index[9]
        doc = data_dict_users_index[2]
        if genre == "M" and value != 3:
            error(field, "M debe ser 3")
        elif doc == "TI" and genre == "F" and value != 3:
            error(field, "Debe ser 3")
        elif genre == "F" and value == 3 and doc != "TI":
            error(field, "Debe ser 1 ó 2")

    #Validaciones
    body_schema = { 0 : {'type': 'integer', 'min': 1, 'max': 999},
                    1 : {'type': 'integer', 'min': 100000000, 'max': 999999999},
                    2 : {'type': 'string', 'minlength': 2, 'maxlength': 2, 'check_with': t_doc},
                    3 : {'type': 'integer', 'min': 10000, 'max': 999999999999},
                    4 : {'type': 'string','maxlength': 20, 'regex': '^[a-zA-Z]+$'},
                    5 : {'type': 'string','maxlength': 20, 'regex': '^[a-zA-Z]+$'},
                    6 : {'type': 'string','maxlength': 20, 'regex': '^[a-zA-Z]+$'},
                    7 : {'type': 'string','maxlength': 20, 'regex': '^[a-zA-Z]+$'},
                    8 : {'type': 'date', 'check_with': check_date},
                    9 : {'type': 'string', 'check_with': check_genre, 'minlength': 1, 'maxlength': 1},
                    10 : {'type': 'integer', 'check_with': check_pregnancy, 'minlength': 1, 'maxlength': 1}}

    body_validator = Validator(body_schema)

    body_results = body_validator.validate(x)
    body_errors = body_validator.errors

    return body_results, errors(body_results, body_errors)

#lee los usuarios
df_users = pd.read_csv('1234567892905201801.txt', sep='|', skiprows=1, header=None)
#pasa la octava columna a datetime
df_users[8] =  pd.to_datetime(df_users[8])
#Creo el diccionario y accedo solo al diccionario dentro del diccionario
data_dict_users = df_users.to_dict('index')
#for por todos los usuarios
index = 0
print("Linea de control", header_results,":", errors(header_results, header_errors))
while index < len(data_dict_users):
    data_dict_users_index = data_dict_users[index]
    print("Linea", index + 1, ":", validations(data_dict_users_index))
    index += 1
