from random import randint, choice, shuffle, sample
from sympy import *
from sympy.abc import x, y
from algebreb.listas.lista import Lista
from algebreb.expresiones.polinomios import Polinomio, polinomio_raices_aleatorias
from algebreb.ejercicios.ecuaciones_univariables import EcuacionLineal, EcuacionCuadratica

class ListaEcuacionesGrado1(Lista):
    def __init__(self, caracteristicas):
        super(ListaEcuacionesGrado1, self).__init__(caracteristicas)
        print(caracteristicas)
        self.instrucciones = 'Resolver las siguientes ecuaciones lineales:'

    def lista_ejercicios(self):
        cantidad = self.caracteristicas['cantidad']
        cmin = self.caracteristicas['cmin']
        cmax = self.caracteristicas['cmax']
        variables = self.caracteristicas['variables']
        dominio = self.caracteristicas['dominio']
        fraccion = self.caracteristicas['fraccion']
        lista = []

        for _ in range(cantidad):
            ld = polinomio_raices_aleatorias(1, variables, dominio, cmin, cmax, fraccion)
            li = Polinomio(0, variables)
            ec = EcuacionLineal(ld, li)

            r1 = 0
            r2 = 0
            r3 = 0
            while(r1 == r2 or r1 == r3 or r2 == r3):
                r1 = randint(cmin, cmax+5)
                r2 = randint(cmin, cmax+5)
                r3 = randint(cmin, cmax+5)
                while(r1 == int(ec.res[0])):
                    r1 = randint(cmin, cmax+5)
                while(r2 == int(ec.res[0])):
                    r2 = randint(cmin, cmax+5)
                while(r3 == int(ec.res[0])):
                    r3 = randint(cmin, cmax+5)

            ec.respuestas.append(r1)
            ec.respuestas.append(r2)
            ec.respuestas.append(r3)
            ec.respuestas.append(int(ec.res[0]))

            lista.append(ec)

        return lista

class ListaEcuacionesGrado2(Lista):
    def __init__(self, caracteristicas):
        super(ListaEcuacionesGrado2, self).__init__(caracteristicas)
        print(caracteristicas)
        self.instrucciones = 'Resolver las siguientes ecuaciones cuadráticas:'

    def lista_ejercicios(self):
        cantidad = self.caracteristicas['cantidad']
        cmin = self.caracteristicas['cmin']
        cmax = self.caracteristicas['cmax']
        variables = self.caracteristicas['variables']
        dominio = self.caracteristicas['dominio']
        fraccion = self.caracteristicas['fraccion']
        lista = []

        for _ in range(cantidad):
            ld = polinomio_raices_aleatorias(2, variables, dominio, cmin, cmax, fraccion)
            li = Polinomio(0, variables)
            ec = EcuacionCuadratica(ld, li)

            res = sample(range(cmax*(-1)-10,cmax+10), 6)

            ec.respuestas.append('{},{}'.format(res[0], res[3]))
            ec.respuestas.append('{},{}'.format(res[1], res[4]))
            ec.respuestas.append('{},{}'.format(res[2], res[5]))
            ec.respuestas.append(','.join(str(r) for r in  ec.res))

            lista.append(ec)

        return lista