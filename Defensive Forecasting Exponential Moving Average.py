# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 16:40:59 2018

@author: Sandman
"""


"""
"""

import pandas as pd
from scipy.optimize import minimize_scalar
import math
from scipy import optimize


df=pd.read_csv("Data1.txt",encoding='utf-8',delimiter=' ',header=None, names=["0","1","2","Stimulus","4","5","6","7","P_Bayesian_model","9","10","11","12"])



df.head()

data_set=df["Stimulus"].head(1000)
data_set_bayesian=df["P_Bayesian_model"].head(1000)
data_set_subject=df["4"].head(1000)


my_list_w=[]
my_list_z=[]
my_list_y=[]
w_old=0.5
z_old=0.5


#sigma_val = 0.06
#sigma_val = 6*(0.01)**2
sigma_val = 4*(0.01)**2
#sigma_val = 3*(0.01)**2

# Calculate W and Z values for Stimulas
for i, row in enumerate(data_set.values):
    my_list_w.append(w_old)
    my_list_z.append(z_old)
    my_list_y.append(data_set[i])
    w_current=((1/5)*(data_set[i])+(4/5)*w_old)
    z_current=((1/10)*(data_set[i])+(9/10)*z_old)
    w_old=w_current
    z_old=z_current

new_df = pd.DataFrame({'Y':my_list_y,'W':my_list_w,'Z':my_list_z})

func_list=[]
math_exprs_list=[]
equation_list=[]

# Create exponential moving average function for 1000 stimulas

for j in range(999,0,-1):     
    
    p_index = 'p_' + str(j-1)
    
    funct = 'def func' + "_" + str(j) + "(x):" 
    ret   = '    return'
    defn = funct + ret
    #w_val = ((new_df["W"][j] - new_df["W"][j-1])**2/sigma_val)
    z_val = ((new_df["Z"][j] - new_df["Z"][j-1])**2/sigma_val)
    y_p   = (new_df["Y"][j-1])
    minus = '-'
    star = '*'
    math_exprs_2 = ''
    open_brace = '('
    close_brace = ')'
    plus = '+'
    var_1 = '(math.exp((-(x - '
    var_2 = ')**2/0.06) - '
    first = var_1+p_index+var_2+str(z_val)+close_brace+star+open_brace+str(y_p)+minus+p_index+close_brace+close_brace
    equation = defn + open_brace+first 
    for i in range(j-1, 0,-1):
        p_index = 'p_' + str(i-1)
        w_val = ((new_df["W"][j] - new_df["W"][i-1])**2/sigma_val)
        z_val = ((new_df["Z"][j] - new_df["Z"][i-1])**2/sigma_val)
        y_p   = (new_df["Y"][i-1])
        second = plus+var_1+str(p_index)+var_2+str(z_val)+close_brace+star+open_brace+str(y_p)+minus+p_index+close_brace+close_brace
        math_exprs_2 = math_exprs_2 + second
        equation = equation + second    
    equation = equation + '+(0.5 - x))'
    func_list.append(equation)
    math_exprs = first+ math_exprs_2
    math_exprs_list.append(math_exprs)
    print("Created func_",j)

        #x=0
        
    
#exec(ema_func_list[1])

equation_list = list(reversed(math_exprs_list))
ema_func_list = list(reversed(func_list))

my_list_p=[]
my_list_p.append(0.5)

p_0 = 0.5

# Calculate P values by solving exponential moving average function equation using Bisect method
for i in range(0,999):
    p_val='p_' + str(i+1)
    exec(ema_func_list[i])
    opti = 'optimize.brenth('
    func = 'func_' + str(i+1)
    opti_close = ', 0, 1)'
    exprsn = p_val+opti+func+opti_close
    function = opti+func+opti_close
    x=0
    val_x0 = eval(equation_list[i])
    x=1
    val_x1 = eval(equation_list[i])
    if(val_x0 < 0 and val_x1 < 0):
        vars()[p_val] = 0
    elif(val_x0 > 0 and val_x1 >0):
        vars()[p_val] = 1
    else:
        vars()[p_val]=optimize.bisect(vars()[func], 0, 1)
    my_list_p.append(vars()[p_val])
    print("i--->",i)
#    i=i+1

len(my_list_w)


final_result_03.to_csv('final_result_950_no_W_3.csv')



#Brier score for error comparison between calculated P Values and Y "Stimulas"
sum((final_result_03['Y'] - final_result_03['P'])**2)


#Brier score for error comparison between calculated P Values and Subject Y values
sum((final_result_03['Y'] - final_result_03['P_subject'])**2)


#Brier score for error comparison between calculated P Values and Bayesian P values
sum((final_result_03['Y'] - final_result_03['P_bayesian'])**2)



