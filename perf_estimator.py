import os
import sys
import subprocess
import numpy as np
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cur_dir)
from charm import* 
from CDAC import *

log = {
    'accel_wise' : False,
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

MODEL_IN=np.array([  
    [3072,1024,1024,1],  
    [3072,1024,4096,1],
    [3072,4096,1024,1]
    ])


# MODEL_IN=np.array([  
#     [3072,1024,1024,1],  
#     [3072,1024,4096,1],
#     [3072,4096,1024,1],
#     [512,64,512,96],  
#     [512,512,64,96],  
#     ])

# MODEL_IN=np.array([
#     [2708,2433,64,1],   
#     [2708,64,7,1] 
#     ])

a = 8
b = 4 
c = 8
x = 4
y = 2 
z = 4

hw_config = np.zeros(12)
hw_config[0] = 0.5    # DDR_BANK
hw_config[1] = a*b*c  # AIE capacity
hw_config[2] = 52     # PLIO_IN
hw_config[3] = 64     # PLIO_OUT
hw_config[4] = 512    # BRAM
hw_config[5] = 320    # URAM
hw_config[6] = a 
hw_config[7] = b
hw_config[8] = c
hw_config[9] = x
hw_config[10] = y
hw_config[11] = z

try: 
    final_config, layer_cycle=direct_ac(MODEL_IN,DATA_TYPE,hw_config,log)
except:
    print("Current configuration failed")
