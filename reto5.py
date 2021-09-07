import os
os.system("cls")
import time
from math import asin, cos, sin, sqrt, radians, degrees
#region VARIABLES GLOBALES
lista_opciones = ["Cambiar contraseña", "Ingresar coordenadas actuales", "Ubicar zona wifi más cercana", "Guardar archivo con ubicación cercana", "Actualizar registros de zonas wifi desde archivo", "Elegir opción de menú favorita","Cerrar sesión." ]
usuario_inicial = "51607"   #codigo grupo fundamentos
contraseña_inicial = "70615"   #codigo al inverso
captcha1 = 607    #ultimos 3 digitos del codigo
captcha2 = int((6*1)+(7-6)-7) #operacion matematica que da el antepenultimo digito del codigo (0)
captcha = captcha1 + captcha2
acumulador = 0
lista_coord = []        #reto 3, matriz vacia para ingresar coordenadas de 3 sitios mas usados (trabajo, casa, parque)
zonawifi_predefinida = [[-3.777, -70.302, 91],[-4.134, -69.983, 233],[-4.006, -70.123, 149],[-3.846, -70.222, 211]]   #reto4. RF01: matriz con ubicacion de 4 zonas wifi predefinidas (latitud, longitud, promedio usuarios)
R = 6372.795477598   #reto 4. radio de la tierra en kilometros
lista_distancias = []
zonawifi = None
distancia_tiempo = None
#endregion

def verificacion(dato1, dato2):
    if dato1 == dato2:
        return True
    else:
        return False

def imprimir_lista():   #RETO2 imprimir lista con todas las opciones
    for i in range (0,len(lista_opciones)):
        print (f"{i+1}. {lista_opciones[i]}")

def ordenar_favorito (posicion):    #RETO 2. RF02 ELEGIR OPCION FAVORITA
    mover = lista_opciones[posicion-1]
    lista_opciones.remove(mover)
    lista_opciones.insert(0,mover)

def mensajes_error (mensaje):
    os.system("cls")
    print(mensaje)
    time.sleep(2)

def ingresar_coord(lista_coord):
    lista_coord = []     #crear matriz de 3 filas por 2 columnas
    for i in range(3):  
        lista_coord.append([0]*2)    #adicionar 2 filas a la matriz
    for l in range (3):
        latitud = input(f"Ingrese Latitud {l+1}: ")   #pedir al usuario latitud 1...2...3
        if latitud != "" or latitud == 0:     #validar q dato ingresado no sea cero o espacio en blanco
            if float(latitud) <= -3.022 and float(latitud) >= -4.227:   #rango de latitudes segun penultimo numero de codigo fundamentos (0)
                lista_coord [l][0] = latitud   #asignar ubicacion de cada latitud dentro de la matriz
                longitud = input(f"Ingrese Longitud {l+1}: ")   #pedir al usuario longitud 1...2...3
                if longitud != "" or longitud == 0:  #validar q dato ingresado no sea cero
                    if float(longitud) <= -69.714 and float(longitud) >= -70.365:   #rango de longitudes segun penultimo numero de codigo fundamentos (0)
                        lista_coord [l][1] = longitud     #asignar ubicacion de cada longitud dentro de la matriz
                    else:
                        mensajes_error("Error coordenada")
                        exit()
                else:
                    mensajes_error ("Error")
            else:
                mensajes_error("Error coordenada")
                exit()        
        else:
            mensajes_error ("Error")
            exit()
    print ("Coordenadas ingresadas correctamente")
    time.sleep(2)
    return lista_coord

def imprimir_coord (lista_coord):   #RETO 3. RF03 mostrar en consola las coordenadas ingresadas 
    coord = list(lista_coord)
    print ("Las coordenas actuales son: ")
    for x in range (0, len(coord)):
        print (f"coordenada [latitud, longitud] {x+1}: {coord[x][0:]}") 
    longitud = (((coord [0][1]), (coord [1][1]), (coord [2][1]))) #RETO 3. calcular coordenada mas al oriente y al occidente 
    long_maxima = max(longitud)
    x = longitud.index(long_maxima)
    print ("La coordenada", x+1, "es la que esta mas al occidente")   
    longitud = (((coord [0][1]), (coord [1][1]), (coord [2][1]))) #RETO 3. calcular coordenada mas al oriente y al occidente 
    long_minima = min(longitud)
    y = longitud.index(long_minima)
    print ("La coordenada", y+1, "es la que esta mas al oriente")
    lista = ["Presione 1, 2 o 3 para actualizar la respectiva coordenada", "Presione 0 para regresar al menu"]
    print (lista[0])
    print (lista[1])
    actualizar = int(input("Seleccione una opcion: ")) 
    if actualizar is 0:
        return
    else:
        actualizar_coor(actualizar, lista_coord)

def actualizar_coor(actualizar, lista_coord):   #RETO3. RF03 actualizar coordenadas actuales
    coord = list(lista_coord) 
    if actualizar == 1 or actualizar == 2 or actualizar == 3: #cambio coordenadas
        actualizar = actualizar - 1
        latitud = input("Ingrese Latitud: ")
        if float(latitud) <= -3.022 and float(latitud) >= -4.227:
            longitud = input("Ingrese Longitud: ")
            if float(longitud) <= -69.714 and float(longitud) >= -70.365:
                coord [actualizar][0] = latitud
                coord [actualizar][1] = longitud
                print("Actualización de coordenadas exitosa.")
            else:
                mensajes_error("Error coordenada")
                exit()
        else:
            mensajes_error ("Error coordenada")
            exit()
    else:
        mensajes_error("Error actualización")
        exit()

def imprimir_ubicacion (lista_coord):     #RETO4. imprimir coordenadas con la ubicacion de los 3 sitios favoritos
    coord = list(lista_coord)
    print ("Las coordenas de sitios frecuentes son: ")
    for x in range (0, len(coord)):
        print (f"coordenada [latitud, longitud] {x+1}: {coord[x][0:]}")
    ubicacion = int(input("Por favor elija su ubicación actual (1, 2 ó 3) para calcular la distancia a los puntos de conexión: ")) 
    if ubicacion == 1 or ubicacion == 2 or ubicacion == 3:
        global zonawifi
        zonawifi = coord[ubicacion-1]
        datos(ubicacion, coord, zonawifi_predefinida)
    else:    
        mensajes_error("Error ubicación")  
        exit()

def datos(indice_zonawifi, lista_coord, zonawifi_predefinida):      #reto4. paso a radianes de las coordenadas de la ubicacion actual
    coord = list(lista_coord)
    predefinida = list(zonawifi_predefinida)
    lat1 = radians(float(coord[indice_zonawifi-1][0]))
    long1 = radians(float(coord[indice_zonawifi-1][1]))
    for x in range (0, len(predefinida)):
        for y in range (0,2):
            predefinida[x][y]= radians(float(predefinida[x][y]))
    calcular_distancias(lat1, long1, predefinida)

def calcular_distancias (lat1, long1, lista_radianes):      #reto4. calculo de distancias desde el punto donde esta el usuario a cada coordenada de zona wifi predefinida
    for x in range (0, 4):
        lat2 = lista_radianes[x][0]
        long2 = lista_radianes[x][1]
        delta_lat = lat2 - lat1
        delta_long = long2 - long1
        distancia = (2*R)*(asin(sqrt((sin(delta_lat/2)**2)+(((cos(lat1))*(cos(lat2)))*(sin(delta_long/2)**2)))))
        distancia = round(distancia * 1000)    #pasar el resultado de kilometros a metros y redondear decimales    
        lista_distancias.append(distancia)
    ordenar_distancias(lista_distancias)

def ordenar_distancias(distancias):     #reto4. ordenar distancias con las dos menores 
    distan = list(distancias)
    min1 = distan.index(min(distan))
    distan.pop(min1)
    min2 = distancias.index(min(distan))
    imprimir_zonawifi_cercana(min1, min2, zonawifi_predefinida, distancias)

def imprimir_zonawifi_cercana(min1, min2, zonawifi_predefinida, lista_distancias):      #reto4. imprimir las dos zonas wifi mas cercanas y con menos usuarios
    for x in range (0,4):
        zonawifi_predefinida[x][0] = degrees(zonawifi_predefinida[x][0])
        zonawifi_predefinida[x][1] = degrees(zonawifi_predefinida[x][1])
    global wifi_cercana
    global distancia_tiempo
    print ("Zonas wifi cercanas con menos usuarios")
    if zonawifi_predefinida[min1][2] < zonawifi_predefinida[min2][2]:
        print (f"La zona wifi 1: ubicada en {zonawifi_predefinida[min1][0:2]} a {lista_distancias[min1]} metros, tiene en promedio {zonawifi_predefinida[min1][2]} usuarios")    
        print (f"La zona wifi 2: ubicada en {zonawifi_predefinida[min2][0:2]} a {lista_distancias[min2]} metros, tiene en promedio {zonawifi_predefinida[min2][2]} usuarios")    
        punto_destino = int(input("Elija 1 o 2 para recibir indicaciones de llegada: "))
        if punto_destino == 1:
            distancia_tiempo = (lista_distancias[min1])
            indicaciones_destino(zonawifi, zonawifi_predefinida[min1])
        elif punto_destino == 2:
            distancia_tiempo = (lista_distancias[min2])
            indicaciones_destino(zonawifi, zonawifi_predefinida[min2])
        else:
            mensajes_error("Error zona wifi")
            exit() 
    else:
        print (f"La zona wifi 1: ubicada en {zonawifi_predefinida[min2][0:2]} a {lista_distancias[min2]} metros, tiene en promedio {zonawifi_predefinida[min2][2]} usuarios")    
        print (f"La zona wifi 2: ubicada en {zonawifi_predefinida[min1][0:2]} a {lista_distancias[min1]} metros, tiene en promedio {zonawifi_predefinida[min1][2]} usuarios")     
        punto_destino = int(input("Elija 1 o 2 para recibir indicaciones de llegada: "))
        if punto_destino == 1:
            distancia_tiempo = (lista_distancias[min2])
            indicaciones_destino(zonawifi,zonawifi_predefinida[min2])
        elif punto_destino == 2:
            distancia_tiempo = (lista_distancias[min1])
            indicaciones_destino(zonawifi,zonawifi_predefinida[min1])
        else:
            mensajes_error("Error zona wifi")
            exit()
    wifi_cercana = zonawifi_predefinida[min1]

def indicaciones_destino (zonawifi, punto_destino):     #reto4. indicar al usuario hacia donde se debe dirigir para llegar a la zona wifi seleccionada
    lat_origen = float(zonawifi[0])
    long_origen = float(zonawifi[1])
    lat_destino = float(punto_destino[0])
    long_destino = float(punto_destino[1])
    if lat_origen > lat_destino:
        mover = "sur"
    elif lat_origen < lat_destino:
        mover = "norte"
    else:
        print("")    
        
    if long_origen > long_destino:
        mover1 = "occidente"
    elif long_origen < long_destino:
        mover1 = "oriente"
    else:
        print("")
        
    print(F"Para llegar a la zona wifi dirigirse primero al {mover1} y luego hacia el {mover}")
    tiempo_viaje()

def tiempo_viaje ():        #reto 4. distancia entre punto de origen y la zona wifi mas cercana seleccionada por el usuario
    global tiempo
    if distancia_tiempo == 0:
        print("")
    else:
        a_pie = round((distancia_tiempo/0.483),2)
        auto = round((distancia_tiempo/20.83),2)
        print (f"El tiempo promedio que tardaría a pie son {a_pie} segundos y en carro serian {auto} segundos.")
    tiempo = auto
    while True:
        menu = input("Presione 0 para salir ")
        if menu == "0":
            break

print("Bienvenido al sistema de ubicación para zonas públicas WIFI")    #RF01 mensaje de bienvenida
usuario_ingresado = input("Nombre de usuario: ") 
if verificacion (usuario_ingresado, usuario_inicial):
    contraseña = input ("Contraseña: ")
    if contraseña == contraseña_inicial:
        validacion = int(input(f"Ingrese el valor de la suma {captcha1} + {captcha2} = "))
        if verificacion (validacion, captcha):
            print ("Sesión iniciada")
            time.sleep(2)
        else:
            mensajes_error("Error") 
            exit()
    elif contraseña == "m1s10nt1c": #easter egg reto 5: 1.1
        cantidad = int(input("Cuántas latitudes vas a ingresar? "))
        numeros = []
        suma = 0
        for i in range(0, cantidad):
            dato = float(input(f"Ingrese latitud {i+1}: "))
            numeros.append(dato)
            suma += dato
        promedio = suma/cantidad
        print(f"El promedio es: {promedio}")
        exit()
    else:
        mensajes_error("Error")
        exit()
elif usuario_ingresado == "Tripulante2022": #easter egg reto 4: 1.1
    print("Este fue mi primer programa y vamos por más")
    exit()
else:
    mensajes_error("Error")  
    exit()           
while acumulador < 3:   #RETO 2. RF03 ALERTA POR OPCION INCORRECTA (3 INTENTOS) 
    imprimir_lista()
    opc_elegida = int(input("Elija una opción: "))
    if opc_elegida > 0 and opc_elegida < 8:
        if lista_opciones[opc_elegida-1] == "Cambiar contraseña":   #RETO 3. opcion 1: Cambiar contraseña actual
            print(f"Usted ha elegido la opción {opc_elegida}")
            if (input ("Contraseña actual: ")) == contraseña_inicial:
                contraseña_nueva = int(input("Ingrese nueva contraseña: "))
                if contraseña_nueva != contraseña_inicial:
                    contraseña_inicial = contraseña_nueva
                    print ("Contraseña actualizada correctamente")
                    time.sleep(2)
                else:
                    mensajes_error("Error")
                    exit()
            else:
                mensajes_error("Error")
                exit()
        elif lista_opciones[opc_elegida-1] == "Ingresar coordenadas actuales": #RETO 3. opcion 2. Ingresar coordenadas actuales
            print(f"Usted ha elegido la opción {opc_elegida}")
            if lista_coord == []:
                lista_coord = ingresar_coord(lista_coord)
            else: 
                imprimir_coord(lista_coord)
        elif lista_opciones[opc_elegida-1] == "Ubicar zona wifi más cercana":     #reto 4 opcion 3: Ubicar zona wifi más cercana
            print(f"Usted ha elegido la opción {opc_elegida}")
            if lista_coord == []:
                print ("Error sin registro de coordenadas")
                exit()
            else:
                imprimir_ubicacion(lista_coord)
        elif lista_opciones[opc_elegida-1] == "Guardar archivo con ubicación cercana":      #RETO 5. opcion 4: Guardar archivo con ubicación cercana
            print(f"Usted ha elegido la opción {opc_elegida}")
            if lista_coord == [] and zonawifi == None:
                mensajes_error("Error de alistamiento")
                exit()
            else:
                wifi_cercana = {"actual": zonawifi, "zonawifi1": wifi_cercana[0:3], "recorrido": [distancia_tiempo, "auto", tiempo]}
                print(wifi_cercana)
                while True:
                    confirmar = input("¿Está de acuerdo con la información a exportar? Presione 1 para confirmar, 0 para regresar al menú principal: ")
                    if confirmar == "1":
                        try:
                            archivo = open(r"C:\Users\joseocamposerna\Documents\python\wificercana.txt","w")
                            archivo.write(str(wifi_cercana))               
                            print("Exportando archivo")
                            time.sleep(2)
                            exit()
                        except IOError:             
                            print("Exportando archivo")
                            time.sleep(2)
                            exit()
                    else:
                        break
        elif lista_opciones[opc_elegida-1] == "Actualizar registros de zonas wifi desde archivo":     #RETO 5. opcion 5: Actualizar registros de zonas wifi desde archivo
            print(f"Usted ha elegido la opción {opc_elegida}")
            try:
                archivo = open(r"C:\Users\joseocamposerna\Documents\python\actualizar.txt").readline()
                archivo = archivo.split(";")
                listatemporalcoord = []
                for x in range(0,4):
                    listatemporalcoord.append([])
                    tmp = archivo[x].split(",")
                    for y in range(0,3):
                        listatemporalcoord[x].append(tmp[y])
                for x in range(len(listatemporalcoord)):
                    for y in range(0,len(listatemporalcoord[x])):
                        listatemporalcoord[x][y]= float(listatemporalcoord[x][y])
                        if y == 2:
                            listatemporalcoord[x][y]=int(listatemporalcoord[x][y])
                zonawifi_predefinida = listatemporalcoord
                print("Estas son las zonas wifi actualizadas")
                print(zonawifi_predefinida)
                while True:
                    submenu = input("Datos de coordenadas para zonas wifi actualizados, presione 0 para regresar al menú principal ")
                    if submenu == "0":
                        break
            except IOError:
                while True:
                    submenu = input("Datos de coordenadas para zonas wifi actualizados, presione 0 para regresar al menú principal ")
                    if submenu == "0":
                        break
        elif opc_elegida == 6:    #RETO 2. RF02 opcion 6: ELEGIR OPCION FAVORITA
            print(f"Usted ha elegido la opción {opc_elegida}")
            opc_favorita = int(input("Seleccione opción favorita: "))
            if opc_favorita==1 or opc_favorita==2 or opc_favorita==3 or opc_favorita==4 or opc_favorita==5:
                if int(input("Para confirmar por favor responda: Redondo soy y es cosa anunciada. Si estoy a la derecha algo valgo, pero a la izquierda soy nada. ¿Cuál número soy?: ")) == 0:
                    if int(input("Para confirmar por favor responda: Si le sumas su hermano gemelo al tres, mas uno mas, ya sabes cuál es: ")) ==7:
                        ordenar_favorito(opc_favorita)
                    else:
                        mensajes_error("Error")
                else:
                    mensajes_error("Error")    
            else:
                mensajes_error("Opcion invalida")
                exit()
        elif opc_elegida == 7:   #RETO 2. RF05 opcion7: SALIR DEL MENU 
            print(f"Usted ha elegido la opción {opc_elegida}")
            print ("Hasta pronto")
            exit() 
    elif opc_elegida == 2021:   #easter egg reto 4: 1.2
        lat = float(input("Dame una latitud y te diré cual hemisferio es... "))
        if lat > 0:
            print("Usted está en hemisferio norte")
            exit()
        elif lat < 0:
            print("Usted está en hemisferio sur")
            exit()
        else:
            print("Usted está sobre la linea del Ecuador")
            exit()
    elif opc_elegida == 2022:   #easter egg reto 5: 1.2
        long = float(input("Escribe una la coordenada de una longitud en Sudamérica y te diré su huso horario "))
        if long >= -81.296 and long <= -67.401:
            print ("El huso horario es -5")
            exit()
        elif long >= -67.402 and long <= -54.316:
            print ("El huso horario es -4")
            exit()
        elif long > -54.316 and long <= -35.833: 
            print ("El huso horario es -3")
            exit()
        else:
            mensajes_error("Error coordenada")
            exit()
    else:
        acumulador = acumulador + 1  #RETO 2. RF03 ALERTA POR OPCION INCORRECTA (3 INTENTOS) 
        mensajes_error("Error menu")
        continue