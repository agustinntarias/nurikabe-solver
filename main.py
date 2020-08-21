import numpy
import sys
import time
class Grilla:
    ########PUBLICO############

    def __init__(self, nombre_archivo, timer = 0):
        '''
        Se encarga de crear una
        instancia de la clase Grilla.
        '''
        self.nombre_archivo = nombre_archivo
        self.grilla = self._construir_grilla()
        self.total_puntos = self._suma_numeros_menos_1()
        self.cantidad_de_numerales = self._contar_simbolo('#')
        self.hay_cuadrado_booleano = self._hay_cuadrado_auxiliar()
        self.grilla_solucion = []
        self.se_encontro_sol = False
        self.ya_esta_solucion = self.ya_hay_sol()
        self.timer = timer

    def ya_hay_sol(self):
        sol = False
        archivo = open(self.nombre_archivo, 'r')
        lineas = archivo.readlines()
        for linea in lineas:
            if linea.strip("\n") == "Solucion:":
                sol = True
                break
        archivo.close()
        return sol

    def es_posicion_valida(self, pos):
        '''Dice si la posición pos está definida en la grilla g. En O(1)'''
        return pos[0] < self.ancho() and pos[1] < self.alto() and pos[0] >= 0 and pos[1] >= 0  # O(1)

    def es_numero(self, pos):
        '''Dice si la posición pos de la grilla g corresponde a un número. En O(1).Precondición:g.es_posicion_valida(pos)'''
        return self.grilla[pos[1]][pos[0]] in "123456789"

    def es_pared(self, pos):
        '''Dice si la posición pos de la grilla g corresponde a una pared. En O(1).Precondición:g.es_posicion_valida(pos)'''
        return self.grilla[pos[1]][pos[0]] == '#'

    def valor(self, pos):
        '''Devuelve el valor númerico de la pos de la grilla g. En O(1).Precondición:g.es_numero(pos)'''
        return int(self.grilla[pos[1]][pos[0]])

    def alto(self):
        '''Devuelve el alto de la grilla g. En O(1)'''
        return len(self.grilla)

    def ancho(self):
        '''Devuelve el ancho de la grilla g. En O(1)'''
        return len(self.grilla[0])

    def cantidad_no_paredes(self):
        '''Devuelve la cantidad de celdas de la grilla g que no corresponden a una celda de tipo pared.O(1).'''
        return self.alto()*self.ancho() - self.cantidad_de_numerales

    def hay_cuadrado(self):
        '''Determina si en g hay un cuadrado de 2×2 de paredes. En O(1).'''
        return self.hay_cuadrado_booleano  # O(1)

    def print_grilla(self):
        for line in self.grilla:
            for char in line:
                print(char, end = " ")
            print()

    def resolver_nurikabe(self, nombre_archivo_salida):
        x = (0, 0)
        self._encerrar_unos()
        self._pintar_casi_adyacentes()
        self._pintar_islas_vacias()
        self.nombre_archivo_salida = nombre_archivo_salida
        self._resolver(x)
        if self.se_encontro_sol:
            solucion = Grilla(self.nombre_archivo)
        else:
            print("No se pudo encontrar una solucion")
            return []


    ########PRIVADO############

    def _construir_grilla(self):
        output = []
        archivo = open(self.nombre_archivo, 'r')
        lineas = archivo.readlines()
        indice_linea, longitud_1er_linea, total_lineas = 0, len(lineas[0].strip('\n')), len(lineas)
        es_grilla = True
        while indice_linea < total_lineas and es_grilla and lineas[indice_linea].strip('\n') != '':  # O(1)
            fila = []
            linea = lineas[indice_linea].strip('\n')
            indice_caracter, cantidad_de_caracteres = 0, len(linea.strip('\n'))  # O(1)
            while indice_caracter < cantidad_de_caracteres and es_grilla:  #O(1)
                caracter = linea[indice_caracter]
                if not caracter in ('123456789.#'):
                    es_grilla = False
                if caracter == '#': fila.append('.')
                else: fila.append(caracter)
                indice_caracter = indice_caracter + 1  # O(1)
            output.append(fila)
            indice_linea = indice_linea + 1
        archivo.close()
        return output

    def _siguiente(self, pos):
        if pos[0] < self.ancho() - 1:
            return (pos[0] + 1, pos[1])
        elif pos[1] < self.alto() - 1:
            return (0, pos[1] + 1)
        else:
            return None

    def _contar_simbolo(self, string):
        output = 0
        indice_fila, longitud_1er_fila, total_filas = 0, self.ancho(), self.alto()
        while indice_fila < total_filas:  # O(1)
            fila = self.grilla[indice_fila]
            indice_columna, cantidad_de_columnas = 0, longitud_1er_fila  # O(1)
            while indice_columna < cantidad_de_columnas:  # O(1)
                caracter = fila[indice_columna]
                if caracter in string:
                    output = output + 1
                indice_columna = indice_columna + 1  # O(1)
            indice_fila = indice_fila + 1
        return output

    def _devolver_posiciones(self, string):
        '''Devuelve las posiciones de los caracteres que esten en string. Las coordenadas de
        las posiciones se guardan en una lista.'''
        output = []
        indice_fila, longitud_1er_fila, total_filas = 0, self.ancho(), self.alto()
        while indice_fila < total_filas:  # O(1)
            fila = self.grilla[indice_fila]
            indice_columna, cantidad_de_columnas = 0, longitud_1er_fila  # O(1)
            while indice_columna < cantidad_de_columnas:  # O(1)
                caracter = fila[indice_columna]
                if caracter in string:
                    output.append((indice_columna, indice_fila))
                indice_columna = indice_columna + 1  # O(1)
            indice_fila = indice_fila + 1
        return output

    def _pared_conexa(self):
        '''Determina si en la grilla g, las paredes forman una única región conexa. Para eso se reutiliza la función
        es_conexa_via del trabajo práctico anterior con el caracter #.'''
        posiciones_validas = self._devolver_posiciones('#')
        cantidad_numerales = len(posiciones_validas)
        if posiciones_validas != []:
            posiciones_a_recorrer = [posiciones_validas[0]]
            posiciones_ya_recorridas = []
            while posiciones_a_recorrer != []:
                posicion_actual = posiciones_a_recorrer[0]
                adyacentes = [
                    (posicion_actual[0] + 1, posicion_actual[1]),
                    (posicion_actual[0] - 1, posicion_actual[1]),
                    (posicion_actual[0], posicion_actual[1] + 1),
                    (posicion_actual[0], posicion_actual[1] - 1)
                    ]
                j = 0
                while j < len(adyacentes):
                    adyacente = adyacentes[j]
                    if (adyacente in posiciones_validas) and (not adyacente in posiciones_ya_recorridas) and (not adyacente in posiciones_a_recorrer):
                        posiciones_a_recorrer.append(adyacente)
                    j = j + 1
                posiciones_ya_recorridas.append(posicion_actual)  # se saca la posibilidad de pasar sobre la posicion actual
                del posiciones_a_recorrer[0]  # se saca la posicion_actual de las posiciones_a_recorrer
            return len(posiciones_ya_recorridas) == cantidad_numerales
        else:
            return False

    def _suma_numeros_menos_1(self):
        '''Devuelve la cantidad de celdas blancas que debe contener la solución. Suma las celdas blancas que deben
        acompañar a cada número.'''
        output = 0
        indice = 0
        posiciones = self._devolver_posiciones('123456789')
        while indice < len(posiciones):
            pos = posiciones[indice]
            output = output + self.valor(pos) - 1
            indice = indice + 1
        return output

    def _islas_validas(self):
        '''Determina si en la grilla g dada todos los números forman islas del tamaño que indican. Se buscan las
        apariciones de los números. Para cada uno de ellos se forma una lista con las celdas blancas que se puedan unir mediante
        la adyacencia horizontal y vertical sin contarlas más de una vez. Luego se controla que el cardinal de la lista coincide
        con el número que contiene dentro.
        '''
        islas_recorridas_son_correctas = True
        posiciones_validas = self._devolver_posiciones('123456789')
        indice = 0
        while indice < len(posiciones_validas):  # O(m*n)
            posicion = posiciones_validas[indice]
            numero = self.valor(posicion)
            posiciones_a_recorrer = [posicion]
            posiciones_ya_recorridas = []
            while posiciones_a_recorrer != []:
                posicion_actual = posiciones_a_recorrer[0]
                adyacentes = [
                    (posicion_actual[0] + 1, posicion_actual[1]),
                    (posicion_actual[0] - 1, posicion_actual[1]),
                    (posicion_actual[0], posicion_actual[1] + 1),
                    (posicion_actual[0], posicion_actual[1] - 1)
                    ]
                i = 0
                ady2 = []
                while i < len(adyacentes):
                    adyacente = adyacentes[i]
                    if self.es_posicion_valida(adyacente):
                        ady2.append(adyacente)
                    i = i + 1
                adyacentes = ady2
                j = 0
                while j < len(adyacentes):
                    adyacente = adyacentes[j]
                    if (self.grilla[adyacente[1]][adyacente[0]] in '.123456789') and (not adyacente in posiciones_ya_recorridas) and (not adyacente in posiciones_a_recorrer):
                        posiciones_a_recorrer.append(adyacente)
                    j = j + 1
                posiciones_ya_recorridas.append(posicion_actual)  # se saca la posibilidad de pasar sobre la posicion actual
                del posiciones_a_recorrer[0]  # se saca la posicion_actual de las posiciones_a_recorrer
            islas_recorridas_son_correctas = islas_recorridas_son_correctas and (numero == len(posiciones_ya_recorridas))
            indice = indice + 1
        return islas_recorridas_son_correctas and self._contar_simbolo('.') == self.total_puntos

    def _hay_cuadrado_auxiliar(self):
        '''Función auxiliar que devuelve un booleano que será True si se encontró un cuadrado de 2x2 de paredes.
        Para esto se recorren todas posiciones y si es una pared se miran las posiciones correspondientes para verificar
        si hay un cuadrado negro.'''
        output = False
        indice_fila, longitud_1er_fila, total_filas = 0, self.ancho(), self.alto()
        while indice_fila < total_filas:  # O(1)
            fila = self.grilla[indice_fila]
            indice_columna, cantidad_de_columnas = 0, longitud_1er_fila  # O(1)
            while indice_columna < cantidad_de_columnas:  # O(1)
                caracter = fila[indice_columna]
                if indice_fila < total_filas - 1 and indice_columna < cantidad_de_columnas - 1 and not output:
                    output = True
                    cuadrado = [
                        (indice_columna, indice_fila),
                        (indice_columna + 1, indice_fila),
                        (indice_columna, indice_fila + 1),
                        (indice_columna + 1, indice_fila + 1)
                        ]
                    indice = 0
                    pos = cuadrado[indice]
                    while indice < 4:
                        pos = cuadrado[indice]
                        output = output and self.es_pared(pos)
                        indice = indice + 1
                indice_columna = indice_columna + 1  # O(1)
            indice_fila = indice_fila + 1
        return output

    def _resolver(self, pos):
        '''Se encarga de implementar el algoritmo de backtracking'''
        if pos == None:
            #Caso base: Si ya no quedan posicones por recorrer armamos el archivo con la grilla
            #si es que se cumplen las condiciones para ser solución del Nurikabe.
            if self._islas_validas() and self._pared_conexa():
                if not self.ya_esta_solucion:
                    archivo = open(self.nombre_archivo, "a")
                    archivo.write("\nSolucion:\n\n")
                    indice_linea = 0
                    while indice_linea < self.alto():
                        linea = self.grilla[indice_linea]
                        indice_caracter = 0
                        while indice_caracter < len(linea):
                            char = linea[indice_caracter]
                            archivo.write(char)
                            indice_caracter = indice_caracter + 1
                        archivo.write('\n')
                        indice_linea = indice_linea + 1
                    archivo.write('\n')
                    archivo.close()
                self.se_encontro_sol = True
            return self.grilla
        if self.grilla[pos[1]][pos[0]] == '.':
            self.grilla[pos[1]][pos[0]] = '#'

            if self.timer > 0:
                print(numpy.array(self.grilla), end = "\n"*15)
                time.sleep(self.timer)
                sys.stdout.flush()

            if self._islas_parcial_validas() and not self._hay_cuadrado_auxiliar():
                self._resolver(self._siguiente(pos))
            self.grilla[pos[1]][pos[0]] = '.'
        self._resolver(self._siguiente(pos))

    def _islas_parcial_validas(self):
        '''Se encarga de verificar que no haya una isla con menos puntos de los necesarios. Es parecida a la
        función _islas_validas pero solamente se verifica que el tamaño de las islas no sea menor que el número.'''
        booleano = True
        posiciones_validas = self._devolver_posiciones('987654321')
        indice = 0
        while indice < len(posiciones_validas):  # O(m*n)
            posicion = posiciones_validas[indice]
            numero = self.valor(posicion)
            posiciones_a_recorrer = [posicion]
            posiciones_ya_recorridas = []
            while posiciones_a_recorrer != []:
                posicion_actual = posiciones_a_recorrer[0]
                adyacentes = [
                    (posicion_actual[0] + 1, posicion_actual[1]),
                    (posicion_actual[0] - 1, posicion_actual[1]),
                    (posicion_actual[0], posicion_actual[1] + 1),
                    (posicion_actual[0], posicion_actual[1] - 1)
                    ]
                i = 0
                ady2 = []
                while i < len(adyacentes):
                    adyacente = adyacentes[i]
                    if self.es_posicion_valida(adyacente):
                        ady2.append(adyacente)
                    i = i + 1
                adyacentes = ady2
                j = 0
                while j < len(adyacentes):
                    adyacente = adyacentes[j]
                    if (self.grilla[adyacente[1]][adyacente[0]] == '.') and (not adyacente in posiciones_ya_recorridas) and (not adyacente in posiciones_a_recorrer):
                        posiciones_a_recorrer.append(adyacente)
                    j = j + 1
                posiciones_ya_recorridas.append(posicion_actual)
                del posiciones_a_recorrer[0]
            booleano = booleano and (numero <= len(posiciones_ya_recorridas))
            indice = indice + 1
        return booleano

    def _dev_adyacentes(self, pos):
        '''Devuelve las posiciones de los adyacentes a pos que están en la grilla'''
        adyacentes = [
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1)
        ]
        ady2 = []
        indice = 0
        while indice < len(adyacentes):
            adyacente = adyacentes[indice]
            if self.es_posicion_valida(adyacente):
                ady2.append(adyacente)
            indice = indice + 1
        return ady2

    def _encerrar_unos(self):
        ''' Se encarga de llenar con paredes las posiciones inmediatas (los adyacentes) a las instancias de unos que se encuentre'''
        posiciones = self._devolver_posiciones('1')
        indice = 0
        while indice < len(posiciones):
            num = posiciones[indice]
            adyacentes = self._dev_adyacentes(num)
            indice2 = 0
            while indice2 < len(adyacentes):
                adyacente = adyacentes[indice2]
                self.grilla[adyacente[1]][adyacente[0]] = '#'
                indice2 = indice2 + 1
            indice = indice + 1

    def _pintar_casi_adyacentes(self):
        '''Se encarga de pintar con paredes las posiciones tales que al menos dos de sus adyacentes sean numeros.'''
        posiciones_numeros = self._devolver_posiciones('123456789')
        i = 0
        while i < self.alto():
            j = 0
            while j < self.ancho():
                adyacentes_que_son_num = 0
                adyacentes = self._dev_adyacentes((j, i))
                indice = 0
                while indice < len(adyacentes) and adyacentes_que_son_num < 2:
                    pos = adyacentes[indice]
                    if pos in posiciones_numeros:
                        adyacentes_que_son_num = adyacentes_que_son_num + 1
                    if adyacentes_que_son_num == 2:
                        self.grilla[i][j] = '#'
                    indice = indice + 1
                j = j + 1
            i = i + 1

    def _pintar_islas_vacias(self):
        '''Se encarga de pintar las islas que hayan quedado vacías (un punto con paredes como adyacentes) luego de encerrar los unos y pintar los casi adyacentes'''
        i = 0
        while i < self.alto():
            j = 0
            while j < self.ancho():
                booleano = True
                adyacentes = self._dev_adyacentes((j, i))
                indice = 0
                while indice < len(adyacentes):
                    ady = adyacentes[indice]
                    booleano = booleano and self.es_pared(ady)
                    indice = indice + 1
                if booleano and self.grilla[i][j] == '.':
                    self.grilla[i][j] = '#'
                j = j + 1
            i = i + 1

g = Grilla(f"./puzzles/{sys.argv[1]}")
if len(sys.argv) == 3: g.timer = float(sys.argv[2])
# print(numpy.array(g.grilla))
# print(g.ya_esta_solucion)
g.resolver_nurikabe("./puzzles/test1sol")
