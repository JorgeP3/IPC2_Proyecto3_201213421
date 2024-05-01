from flask import Flask, request
from clases.Cliente import Cliente
from clases.Banco import Banco

import re, xmltodict, dicttoxml #convertir xml a un diccionario o

def create_app():
    app = Flask(__name__)
    return app
app = create_app()

lista_clientes = []
lista_bancos=[]

def validarNit(nit):#si lo encuentra retorna true, si no falso.
    encontrado=False
    for cliente in lista_clientes:
        if nit==cliente.nit:
            encontrado=True
            break
    return encontrado

def validarCodigoBanco(codigo):#si lo encuentra retorna true, si no falso.
    encontrado=False
    for banco in lista_bancos:
        if codigo==banco.codigo:
            encontrado=True
            break
    return encontrado

@app.route('/prueba', methods=['get'])
def prueba():

    return "get succesful" 

@app.route('/limpiar', methods=['POST'])
def limpiar():

    lista_clientes.clear()
    lista_bancos.clear()

    return "se borraron las listas"


@app.route('/GuardarConfiguraciones', methods=['POST'])
def create_clientes():              #archivo xml que se convierte en un diccionario
    clientes_y_bancos_dict = xmltodict.parse(request.data)

    clientes_dict=clientes_y_bancos_dict['config']['clientes']['cliente']
    bancos_dict = clientes_y_bancos_dict['config']['bancos']['banco']

    #este for extrae la informacion de los clientes
    clientes_nuevos=0
    clientes_actualizados=0

    if isinstance(clientes_dict, list):
        for cliente in clientes_dict:
            patronNit=r'[0-9-]+'
            patronNombre = r'[a-zA-Z0-9ZÁÉÍÓÚáéíóúÜüÑñ\s]+' #duda sobre la expresion regular
        
            nit = re.search(patronNit, cliente['NIT'])
            nombre = re.search(patronNombre, cliente['nombre'])

            if nit and nombre:
                if validarNit(nit.group())==False:
                    lista_clientes.append(Cliente(str(nit.group()), str(nombre.group())))
                    clientes_nuevos+=1
                else:
                    for clienteG in lista_clientes:
                        if nit.group()==clienteG.nit:
                            clienteG.nombre=nombre.group()
                            clientes_actualizados+=1
                            break  
    else:  
        cliente = clientes_dict
        patronNit=r'[0-9]+'
        patronNombre = r'[a-zA-Z0-9ZÁÉÍÓÚáéíóúÜüÑñ\s]+' #duda sobre la expresion regular
    
        nit = re.search(patronNit, cliente['NIT'])
        nombre = re.search(patronNombre, cliente['nombre'])

        if nit and nombre:
            if validarNit(nit.group())==False:
                lista_clientes.append(Cliente(str(nit.group()), str(nombre.group())))
                clientes_nuevos+=1
            else:
                for clienteG in lista_clientes:
                    if nit.group()==clienteG.nit:
                        clienteG.nombre=nombre.group()
                        clientes_actualizados+=1
                        break  

    #este for extrae la informacion de los bancos, cuando solo hay un banco o un cliente se va todo al carajo
    bancos_nuevos=0
    bancos_actualizados=0

    if isinstance(bancos_dict, list):  # Si hay una lista de bancos
        for banco in bancos_dict:
            patronCodigo=r'[0-9]+'
            patronNombre = r'[a-zA-Z0-9ZÁÉÍÓÚáéíóúÜüÑñ\s]+' #duda sobre la expresion regular
        
            codigo = re.search(patronCodigo, banco['codigo'])
            nombre = re.search(patronNombre, banco['nombre'])
    
            if codigo and nombre:
                if validarCodigoBanco(codigo.group())==False:
                    lista_bancos.append(Banco(str(codigo.group()), str(nombre.group())))
                    bancos_nuevos+=1
                else:
                    for bancoG in lista_bancos:
                        if codigo.group()==bancoG.codigo:
                            bancoG.nombre=nombre.group()
                            bancos_actualizados+=1
                            break  
    else:  #cuando el xml tra solo un banco
        banco = bancos_dict
        patronCodigo=r'[0-9-]+'
        patronNombre = r'[a-zA-Z0-9ZÁÉÍÓÚáéíóúÜüÑñ\s]+' #duda sobre la expresion regular
    
        codigo = re.search(patronCodigo, banco['codigo'])
        nombre = re.search(patronNombre, banco['nombre'])
    
        if codigo and nombre:
            if validarCodigoBanco(codigo.group())==False:
                lista_bancos.append(Banco(str(codigo.group()), str(nombre.group())))
                bancos_nuevos+=1
            else:
                for bancoG in lista_bancos:
                    if codigo.group()==bancoG.codigo:
                        bancoG.nombre=nombre.group()
                        bancos_actualizados+=1
                        break 

    
    respuesta= {'clientes':{"creados":clientes_nuevos,"actualizados":clientes_actualizados},
                'bancos':{"creados":bancos_nuevos,"actualizados":bancos_actualizados}}
    xml=dicttoxml.dicttoxml(respuesta,custom_root='respuesta',attr_type=False)
    print("------------------------------------------------")
    for cliente in lista_clientes:
        print("Nit:",cliente.nit,"| nombre:",cliente.nombre)
    print("------------------------------------------------")
    for banco in lista_bancos:
        print("Codigo:",banco.codigo,"| Nombre:",banco.nombre)
    return  xml

@app.route('/GuardarTransacciones', methods=['POST'])
def create_trans():              #archivo xml que se convierte en un diccionario
    clientes_y_bancos_dict = xmltodict.parse(request.data)

    
    return  "prueba Transacciones"


if __name__=="__main__":
  app.run(threaded=True,port=5000,debug=True)