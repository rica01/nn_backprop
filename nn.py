from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from six.moves import zip
from numpy import hstack,exp,dot,ones,tanh,mean,abs,array
import numpy as np
import sys

def fact(f='sigmoide'):
    if f=='sigmoide':
        return [lambda x: 1./(1+exp(-x)), lambda y: y*(1-y)]
    elif f=='tanh':
        return [tanh, lambda y: 1 - y**2]
    elif f=='ident':
        return [lambda x: x, lambda y: 1]

def creapesos( arq ):
    en,hn,sn = arq
    syn_0 = 2*np.random.random( (en+1,hn+1) )-1
    syn_1 = 2*np.random.random( (hn+1,sn) )-1
    return [syn_0, syn_1]

def entrena(iters,alfa,pesos,iterr=1000,verbose=False):
    syn_0, syn_1 = pesos
    for j in range(iters):
        I = hstack( (X,ones((len(X),1))) )
        H = fh(dot(I,syn_0))
        S = fs(dot(H,syn_1))
        #error de la capa de salida
        S_err = S - Y
        #delta capa salida
        S_d = S_err*dfs(S)
        #error capa escondida
        H_err = S_d.dot(syn_1.T)
        #delta capa escondida
        H_d = H_err*dfh(H)
        #actualizamos pesos
        syn_1 -= alfa * (H.T.dot(S_d))
        syn_0 -= alfa * (I.T.dot(H_d))
        if(verbose):
            if((iterr>0) and (j%iterr==0)):
                print(mean(abs(S_err)))
    return [syn_0,syn_1]

def ff(estimulo,pesos):
    syn_0, syn_1 = pesos
    I = hstack( (estimulo,ones((len(estimulo),1))) )
    H = fh(dot(I,syn_0))
    S = fs(dot(H,syn_1))
    return S


xor = array( [[0,0,1,0],[0,1,1,1],[1,0,1,1],[1,1,1,0]] )
X = xor[:,:-1]
Y = xor[:,-1].reshape(-1,1)

tipocapa1="tanh"
tipocapa2="tanh"
f1, f2 = fact(tipocapa1), fact(tipocapa2)
fh, dfh = f1
fs, dfs = f2

if __name__ == '__main__':
    intermedias = 2
    cons_aprendizaje = 0.1
    iteraciones = 20000
    alfa, iters = (cons_aprendizaje, iteraciones)
    en, hn, sn = ( X.shape[1], intermedias, Y.shape[1] )
    syn_0, syn_1 = creapesos( (en,hn,sn) )
    print("alfa: {0}".format(alfa))
    print("iteraciones: {0}".format(iters))
    print("arquitectura: {0} {1} {2}".format(en,hn,sn))
    print("funciones de activacion: {0} {1}".format(tipocapa1,tipocapa2))
    print("pesos primera capa \n{0}".format(syn_0))
    print("pesos segunda capa \n{0}".format(syn_1))
    print("Datos \n{0}".format(X))
    print("Previo ")
    for x,y in zip(ff(X,[syn_0,syn_1]),Y):
        print("{0} : {1}".format(x,y))
    pesos_t = entrena(iters,alfa,[syn_0,syn_1])
    print("Entrenada")
    for x,y in zip(ff(X,pesos_t),Y):
        print("{0} : {1}".format(x,y))
    print("pesos primera capa \n{0}".format(syn_0))
    print("pesos segunda capa \n{0}".format(syn_1))

