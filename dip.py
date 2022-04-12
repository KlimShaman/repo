import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import math
import os
import streamlit as st

def Mu(i, n):      
    mu = (1+i)**(-n)
    return mu

def Di(i, n):      
    di = 1 - ((1+i)**(-n))
    return di

def Di_pi(i, n, p):
    di = 1 - ((1+i)**(-n))
    di_pi = p*(1-(1-di)**(1/p))
    return di_pi
    
def I_pi(i, p):
    i_pi = p * ((1 + i)**(1/p) - 1)
    return i_pi

def Alpha(i, d, n, p):
    alpha = (i * Di(i, n))/(I_pi(i, p) * Di_pi(i, n, p))
    return alpha

def Beta(i, d, n, p):
    beta = (i - I_pi(i, p)) / (I_pi(i,p) * Di_pi(i, n, p))
    return beta
    
def TP_x(t, bord):
    if (t > bord):
        return 0
    else:
        return (0.7**t)
    
def A1(n, g, summa, x):
    a1 = 0.0
    a_1 = 0.0
    l = []
    l.clear()
    k = 0
    print('Введите', n, 'l')
    for i in range(x, x + n):
        a=float(input())
        l.append(a)
    for i in range(x, x + n):
        a1 += Mu(g, i) * l[k]
        k+=1
    a_1 = summa * (a1 / (l[0] * Mu(g, x)))
    return a_1

def A2(n, i, x, w, summa, p):
    a2 = (1/(1-Mu(i,n))) - (Mu(i, n)/((w - x)*(1-Mu(i, n))**2))*(1 - Mu(i, n)**(w-x))
    a_2 = Alpha(i, Di(i, n), n, p) * a2 - Beta(i, Di(i,n), n, p)
    a_22 = a_2*summa
    return a_22

def A3(t, n, bord, g):
    l = []
    l.clear()
    k=0
    b1=0
    for i in range(t, t + n):
        print('Введите сколько выплачивает перестраховочная компания в момент t =', i,':')
        a=float(input())
        l.append(a)
    for i in range(t, t + n):
        b1 += l[k]*TP_x(i, bord)*Mu(g, i)
        k+=1
    return b1
n = 0
g = 0
summa = 0
x = 0 
st.title('Рентный калькулятор')
st.write("Если хотите посчитать современную стоимость полной пожизненной ренты, выплачиваемой раз в год:")
st.text_input("Введите продолжительность временной пожизненной ренты (n):", key=n)
st.text_input("Введите эффективную процентную годовую ставку (i):", key=g)
st.text_input("Введите сумму, выплачиваемую раз в год в начале года:", key=summa)
st.text_input("Введите возраст человека на момент заключения договора:", key=x)

n = int(st.session_state.n)
g = float(st.session_state.g)
summa = int(st.session_state.summa)
x = int(st.session_state.x)

st.write('Актуарная современная стоимость временной пожизненной ренты =', A1(n, g, summa, x))       

# print('Введите <<1>>, если хотите посчитать актуарную современную стоимость временной пожизненной ренты (метод текущего платежа)\n')
# print('Введите <<2>>, если хотите посчитать современную стоимость полной пожизненной ренты, выплачиваемой раз в год\n')
# print('Введите <<3>>, если хотите посчитать актуарную современную стоимость обязательств перестраховочной компании\n')
# z = int(input())
# if (z==1):
#     print('Введите продолжительность временной пожизненной ренты (n): ')
#     n = int(input())
#     print('Введите эффективную процентную годовую ставку (i): ')
#     g = float(input())
#     print('Введите сумму, выплачиваемую раз в год в начале года: ')
#     summa = float(input())
#     print('Введите возраст человека на момент заключения договора: ')
#     x = int(input())
#     print('Актуарная современная стоимость временной пожизненной ренты =', A1(n, g, summa, x))
# if (z==2):
#     n = 1
#     print('Введите эффективную процентную годовую ставку (i): ')
#     g = float(input())
#     print('Введите сумму, выплачиваемую в год: ')
#     summa = float(input())
#     print('Введите возраст человека на момент заключения договора: ')
#     x = int(input())
#     print('Введите предельный возраст модели де Муавра(w): ')
#     w = int(input())
#     print('Введите частоту выплат(p): ')
#     p = int(input())
#     print('Современная стоимость полной пожизненной ренты, выплачиваемой раз в год =', A2(n, g, x, w, summa, p))
# if (z==3):
#     print('Введите момент t, начиная с которого перестраховщики начинают выплачивать деньги: ')
#     t = int(input())
#     print('Введите больше скольки лет не может прожить человек: ')
#     bord = float(input())
#     n = math.ceil(bord) - t
#     print('Введите эффективную процентную годовую ставку (i): ')
#     g = float(input())
#     print('Актуарная современная стоимость обязательств перестраховочной компании =', A3(t, n, bord, g))
# if (z != 1 and z != 2 and z!= 3):
#     print('Вы ввели несуществующую задачу')
