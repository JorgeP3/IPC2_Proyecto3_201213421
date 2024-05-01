#clases
from clases.Cliente import Cliente
from clases.Banco import Banco
from clases.Factura import Factura


#bibliotecas
from flask import Flask, request
import re, xmltodict, dicttoxml #convertir xml a un diccionario o

def create_app():
    app = Flask(__name__)
    return app
app = create_app()

lista_clientes = []
lista_bancos=[]
lista_facturas=[]
lista_pagos=[]

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

def validarNumeroFactura(numeroFactura):#si lo encuentra retorna true, si no falso.
    encontrado=False
    for factura in lista_facturas:
        if numeroFactura==factura.numeroFactura:
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
    lista_facturas.clear()
    lista_pagos.clear()

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
    facturas_y_pagos_dict = xmltodict.parse(request.data)

    facturas_dic=facturas_y_pagos_dict['transacciones']['facturas']['factura']
    pagos_dic=facturas_y_pagos_dict['transacciones']['pagos']['pago']

    factuas_nuevas=0
    facturas_duplicadas=0
    factuas_con_error=0

    if isinstance(facturas_dic,list):
        for factura in facturas_dic:
            patronFactura= r'[a-zA-Z0-9-]+'
            patronNit=r'[0-9-]+'
            patronFecha=r'^(0[1-9]|[1-2][0-9]|3[0-1])/(0[1-9]|1[0-2])/\d{4}$'
            patronValor=r'^-?\d+(?:\.\d+)?$'

            numeroFactura=re.search(patronFactura, factura['numeroFactura']).group()
            nitCliente=re.search(patronNit, factura['NITcliente']).group()
            fecha=re.search(patronFecha, factura['fecha']).group()
            valor=re.search(patronValor, factura['valor']).group()

            if numeroFactura and nitCliente and fecha and valor:
                if validarNumeroFactura(numeroFactura)==False:
                    if validarNit(nitCliente)==True:
                        lista_facturas.append(Factura(numeroFactura,nitCliente,fecha,float(valor)))
                        factuas_nuevas+=1
                    else:
                        factuas_con_error+=1
                else:#si si encuentra el numero de factura
                    facturas_duplicadas+=1
    else:#si solo viene una factura
        factura=facturas_dic
        patronFactura= r'[a-zA-Z0-9-]+'
        patronNit=r'[0-9-]+'
        patronFecha=r'^(0[1-9]|[1-2][0-9]|3[0-1])/(0[1-9]|1[0-2])/\d{4}$'
        patronValor=r'^-?\d+(?:\.\d+)?$'

        numeroFactura=re.search(patronFactura, factura['numeroFactura']).group()
        nitCliente=re.search(patronNit, factura['NITcliente']).group()
        fecha=re.search(patronFecha, factura['fecha']).group()
        valor=re.search(patronValor, factura['valor']).group()

        if numeroFactura and nitCliente and fecha and valor:
            if validarNumeroFactura(numeroFactura)==False:
                if validarNit(nitCliente)==True:
                    lista_facturas.append(Factura(numeroFactura,nitCliente,fecha,float(valor)))
                    factuas_nuevas+=1
                else:
                    factuas_con_error+=1
            else:#si si encuentra el numero de factura
                facturas_duplicadas+=1
    print("------------------------------------------------")
    for factura in lista_facturas:
        print("#factura:",factura.numeroFactura,"| NitCliente:",factura.nitCliente,"| Fecha:",factura.fecha,"| valor",factura.valor)
    
    return  "prueba Transacciones"


if __name__=="__main__":
  app.run(threaded=True,port=5000,debug=True)