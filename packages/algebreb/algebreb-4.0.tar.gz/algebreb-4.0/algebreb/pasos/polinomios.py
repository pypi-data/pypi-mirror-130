from sympy import *
from sympy.abc import a, b, c, x, y, z
from sympy import UnevaluatedExpr
from algebreb.expresiones.polinomios import Polinomio

def textMath(text):
    inicio = '\\textrm{'
    fin = '}'
    return inicio + text + fin

def pasos_suma_polinomios(p1, p2):
    pasos = []

    p3 = p1 + p2

    pasos.append(textMath('Se encuentran los terminos semejantes del polinomio: ') 
        + latex(p1.as_expr()) + textMath(' con el polinomio ') + latex(p2.as_expr()) )
    # pasos.append(textMath('Los cuales son: '))
    pasos.append(textMath('Finalmente se tiene: ') + latex(p3.as_expr()))

    return pasos

def pasos_resta_polinomios(p1, p2):
    pasos = []

    p3 = p1 - p2

    pasos.append(textMath('Se encuentran los terminos semejantes del polinomio: ') 
        + latex(p1.as_expr()) + textMath(' con el polinomio ') + latex(p2.as_expr()) )
    # pasos.append(textMath('Los cuales son: '))
    pasos.append(textMath('Finalmente se tiene: ') + latex(p3.as_expr()))

    return pasos

def pasos_mult_polinomios(p1, p2):
    pasos = []
    sumandos = []

    monomios_p1 = list(Add.make_args(p1.as_expr()))
    paso = ''

    poli2_expr = p2.as_expr() 

    for monomio in monomios_p1:
        producto = monomio * poli2_expr
        # paso = 'Se multiplica el termino {} por {}, obteniendo {}'.format(latex(monomio), latex(poli2_expr), latex(producto))
        pasos.append( textMath('Se multiplica el termino ') 
            + latex(monomio) + textMath(' por ') + latex(poli2_expr) 
            + textMath(', obteniendo ') + latex(producto))
        sumandos.append(producto)
    
    str_sumandos = ' + '.join([latex(suma) for suma in sumandos])

    #pasos.append('Se suman los productos obtenidos: {}'.format(str_sumandos))
    pasos.append(textMath('Se suman los productos obtenidos: ') + str_sumandos)
    #pasos.append('Finalmente se obtiene: {}'.format(latex((p1*p2).as_expr())))
    pasos.append(textMath('Finalmente se obtiene: ') + latex((p1*p2).as_expr()))
    
    return pasos


poli1 = Polinomio(3*x**2+x+6, x)
poli2 = Polinomio(x**2+5*x+6, x)
multi = pasos_suma_polinomios(poli1, poli2)
print("PASOS: ", multi)
#print(poli1*poli2)