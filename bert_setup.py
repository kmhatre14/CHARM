import os
import sys
import subprocess
import numpy as np
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cur_dir)
from charm import* 
from CDAC import *

log = {
    'accel_wise' : True,
    'layer_wise' : False
}

num_acc=2
model='bert'
DATA_TYPE=4
part=1
acc='two_div'

#Set the design project path
prj_dir= cur_dir + '/bert_setup'
#subprocess.run(['mkdir','-p' ,f'{prj_dir}'])

# Raw model defination (Bert)
# batch Size : 8 
# seq_length : 384
# head : 16 
# head_dim : 64
# embed_dim : 1024

# MODEL_IN=np.array([
#     [seq*batch,embed_dim,embed_dim*3,1],
#     [seq*batch,head_dim,seq,heads],
#     [seq*batch,seq,head_dim,heads],
#     [seq*batch,embed_dim,embed_dim,1],
#     [seq*batch,embed_dim,mlp_dim,1],
#     [seq*batch,mlp_dim,embed_dim,1],
#     ])

# BERT model 
MODEL_IN=np.array([  
    [3072,1024,1024,1],  
    [3072,1024,4096,1],
    [3072,4096,1024,1],
    [512,64,512,96],  
    [512,512,64,96],  
    ])

# MODEL_IN=np.array([
#     [2708,2433,64,1],   
#     [2708,64,7,1] 
#     ])

part_final, final_config, layer_cycle=cdac_top(MODEL_IN,DATA_TYPE,num_acc,log)

Versal_config = final_config
# h1,   w1,   w2,   A,   B,   C,  A_BRO, C_BRO,  PACK_IN, PACK_OUT, X,   Y,   Z,  data_type  kernel_type
# 64.   64.    64.  8.   4.   4.  2.     2.      2.       2.        2.   4.   4.  1.         7.s  0.  9.  0.   4.  1.  1.  0.
# AIE_NAME= str(Versal_config[0,3]) + str(Versal_config[0,4]) + str(Versal_config[0,5])
# BUF_NAME= str(Versal_config[0,10]) + str(Versal_config[0,11]) + str(Versal_config[0,12])
#Set the design project path
# if DATA_TYPE==1:
#     prj_dir= prj_dir + '/int8_' +  acc +'/' + model + '/int8_' + AIE_NAME + '_' + BUF_NAME
# elif DATA_TYPE==2:
#     prj_dir= prj_dir + '/int16_' +  acc +'/' + model + '/int16_' + AIE_NAME + '_' + BUF_NAME
# elif DATA_TYPE==4:
#     prj_dir= prj_dir + '/fp32_' +  acc +'/' + model + '/fp32_' + AIE_NAME + '_' + BUF_NAME

#Create the object of the class charm
# subprocess.run(['mkdir','-p' ,f'{prj_dir}'])
# automm=charm(prj_dir)

#Launch charm automatic code generator to emit the code for AIE, PL and Host CPU
# device='vck190' # Supported devices are vck190 and vck5000
#automm.cacg(Versal_config,device)

# #Run Vitis Compilation Flow
# automm.build()