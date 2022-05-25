import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import math
import os
import streamlit as st
import time


def Mu(i, n):      
    mu = (1+i)**(-n)
    return mu

def Di(i, n):      
    di = 1 - ((1+i)**(-n))
    return di

def Surv(x):
    ver = math.sqrt(1 - x/110)
    return ver

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
    fr = ls[0]
    for z in range(0, n):
        a1 += Mu(g, z) * ls[z]
    a_1 = summa * (a1 / (fr * Mu(g, 0)))
    return a_1

def A2(n, i, x, w, summa, p):
    summa = summa * p
    a2 = (1/(1-Mu(i,n))) - (Mu(i, n)/((w - x)*(1-Mu(i, n))**2))*(1 - Mu(i, n)**(w-x))
    a_2 = Alpha(i, Di(i, n), n, p) * a2 - Beta(i, Di(i,n), n, p)
    a_22 = a_2*summa
    return a_22

def A3(t, n, bord, g):
    k = 0
    b1 = 0
    for i in range(t, t + n):
        b1 += ls2[k]*TP_x(i, bord)*Mu(g, i)
        k += 1
    return b1

def A4(age, age2, per, pl):
    summa3 = pl
    percent = 0.067
    delta = (age2 - age) * 12
    for i in range(delta):
        summa3 += summa3 * (1 + percent/12)
        summa3 += 5000
    otvet = summa3 / (12 * (age2 - age))
    return otvet
    
    



try:
    st.title('Рентный калькулятор')

    option = st.selectbox(
        'Какую задачу вы хотите решить?',
        ('Посчитать актуарную современную стоимость временной пожизненной ренты', 
         'Посчитать актуарную современную стоимость полной пожизненной ренты', 
         'Посчитать актуарную современную стоимость обязательств перестраховочной компании',
         'Посчитать вероятность смерти/выживания',
         'Посчитать будущую пенсию')
    )
    if (option == 'Посчитать актуарную современную стоимость временной пожизненной ренты'):
        x = int(st.number_input("Введите возраст человека на момент заключения договора:"))
        n = int(st.number_input("Введите продолжительность временной пожизненной ренты (n):"))
        ip = st.number_input("Введите эффективную процентную годовую ставку (i):")
        summa = st.number_input("Введите сумму, выплачиваемую раз в год в начале года:")
        global ls
        ls = [0] * n
        for i in range(0, n):
            ls[i] = st.number_input(f'Введите l {x + i}')


        st.write('Актуарная современная стоимость временной пожизненной ренты =', A1(n, ip, summa, x))
    elif (option == 'Посчитать актуарную современную стоимость полной пожизненной ренты'):
        n = 1
        g = float(st.number_input("Введите эффективную процентную годовую ставку (i):"))
        x = int(st.number_input("Введите возраст человека на момент заключения договора:"))
        w = int(st.number_input("Введите предельный возраст модели де Муавра(w):"))
        p = int(st.number_input("Введите частоту выплат(p):"))
        summa = int(st.number_input("Введите сумму, выплачиваемую в период:"))

        st.write('Современная стоимость полной пожизненной ренты, выплачиваемой раз в заданный период =', A2(n, g, x, w, summa, p))

    elif (option == 'Посчитать актуарную современную стоимость обязательств перестраховочной компании'):
        t = int(st.number_input("Введите момент t, начиная с которого перестраховщики начинают выплачивать деньги:"))
        bord = st.number_input("Введите больше скольки лет не может прожить человек:")
        n = math.ceil(bord) - t
        g = float(st.number_input("Введите эффективную процентную годовую ставку (i):"))
        global ls2
        ls2 = [0] * n
        for i in range(0, n):
            ls2[i] = int(st.number_input(f'Введите сколько выплачивает перестраховочная компания в момент t = {i + t}:'))
        st.write('Актуарная современная стоимость обязательств перестраховочной компании =', A3(t, n, bord, g))
    elif (option == 'Посчитать вероятность смерти/выживания'):
        option2 = st.selectbox('Какую величину вы хотите посчитать?',
                               ('Вероятность смерти человека возраста x в ближайшие t лет',
                               'Вероятность того, что человек в возрасте x проживет еще минимум t лет',
                               'Вероятность того, что человек в возрасте x умрет в течение ближайшего года',
                               'Вероятность того, что человек в возрасте x проживет минимум еще год',
                               'Вероятность того, что человек в возрасте x проживет еще t лет, но умрет на протяжении следующих n лет'
                               )
                              )
        if (option2 == 'Вероятность смерти человека возраста x в ближайшие t лет'):
            x = int(st.number_input("Введите возраст человека:"))
            t = st.number_input("Введите t:")
            st.write('Вероятность =', (Surv(x) - Surv(x + t)) / Surv(x))
        if (option2 == 'Вероятность того, что человек в возрасте x проживет еще минимум t лет'):
            x = int(st.number_input("Введите возраст человека:"))
            t = st.number_input("Введите t:")
            st.write('Вероятность =', Surv(x + t) / Surv(x))
        if (option2 == 'Вероятность того, что человек в возрасте x умрет в течение ближайшего года'):
            x = int(st.number_input("Введите возраст человека:"))
            st.write('Вероятность =', (Surv(x) - Surv(x+1)) / Surv(x))
        if (option2 == 'Вероятность того, что человек в возрасте x проживет минимум еще год'):
            x = int(st.number_input("Введите возраст человека:"))
            st.write('Вероятность =', Surv(x+1) / Surv(x))
        if (option2 == 'Вероятность того, что человек в возрасте x проживет еще t лет, но умрет на протяжении следующих n лет'):
            x = int(st.number_input("Введите возраст человека:"))
            t = st.number_input("Введите t:")
            n = st.number_input("Введите n:")
            st.write('Вероятность =', (Surv(x+t) - Surv(x+t+n)) / Surv(x))
    elif (option == 'Посчитать будущую пенсию'):
         age = int(st.number_input("Введите ваш возраст:"))
         age2 = int(st.number_input("Введите возраст выхода на негосударственную пенсию:"))
         pl = int(st.number_input("Введите ежемесячный платеж:"))
         per = int(st.number_input("Введите период выплаты пенсии(в годах):"))
         st.write('Пенсия (руб/мес) =', A4(age, age2, per, pl))
         
        


        
        
except IndexError:
    pass
except ZeroDivisionError:
    pass
