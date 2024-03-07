import numpy as np
import math
import sys
from itertools import combinations
from .cdse import *


def cdac_top(MODEL_IN,DATA_TYPE,num_acc,log):
    total_ops = np.sum(np.multiply(np.multiply(np.multiply(MODEL_IN[:,0],MODEL_IN[:,1]),MODEL_IN[:,2]),MODEL_IN[:,3]))*2
    num_ops = np.multiply(np.multiply(MODEL_IN[:,0],MODEL_IN[:,1]),MODEL_IN[:,2])
    index=np.argsort(num_ops,0)[::-1]
    MODEL_SORT=MODEL_IN[index,:]

    num_layer=MODEL_IN.shape[0]

    DDR_BANK=1/num_acc
    AIE_NUM=400
    PLIO_IN=100
    PLIO_OUT=80
    BRAM=(967-199) #100 for AXI bound consumpssion
    URAM=(463-43)

    HW_Part=[DDR_BANK,AIE_NUM,PLIO_IN,PLIO_OUT,BRAM,URAM]

    # PL Frequency
    freq_rate=230/250

    combination = combinations(range(num_layer-1), num_acc-1)
    comb=list(combination)

    if num_acc==1:
        final_config,best_cycle,time_layer,HW_Used=cdse_top(MODEL_IN,HW_Part,DATA_TYPE)
        print('Estimated Latency is: ' + str(best_cycle*1e-6) + ' ms' )
        print('Estimated Throughput is: ' + str(total_ops/best_cycle) + ' GOPS' )
        part_final=0
        print(final_config)
        return part_final, final_config, time_layer
    else:
        round=len(comb)
        best_cycle=1e30
        for i in range(round):
            comb_sel=comb[i]
            comb_part_cur=0
            comb_part_nxt=0
            index_origin=[]
            HW_LEFT=HW_Part[1:6]
            HW_Used=np.zeros(5)
            HW_Cur=np.ones(6)*DDR_BANK
            total_ops_nxt=total_ops
            temp_config = np.zeros((num_acc,22))
            temp_cycle = np.zeros((num_acc,1))
            layer_cycle_temp = np.zeros((num_layer))
            ### Create the Partitions of the Model
            for acc in range(num_acc):
                if acc==num_acc-1:
                    comb_part_nxt=num_layer
                    compensation=[0,0,0,0,0]
                else:
                    comb_part_nxt=comb_sel[acc]+1
                    compensation=[20,20,20,50,40]
                index_temp=index[comb_part_cur:comb_part_nxt]
                index_origin.append(index_temp)
                MODEL_PART=MODEL_SORT[comb_part_cur:comb_part_nxt,:]
                comb_part_cur=comb_part_nxt

                total_ops_cur = np.sum(np.multiply(np.multiply(np.multiply(MODEL_PART[:,0],MODEL_PART[:,1]),MODEL_PART[:,2]),MODEL_PART[:,3]))*2
                comp_ratio=total_ops_cur/total_ops_nxt
                total_ops_nxt=total_ops_nxt-total_ops_cur
                HW_Cur[1:6]=np.add(np.multiply(HW_LEFT,comp_ratio),compensation)
                temp_config[acc,:],temp_cycle[acc,0],time_layer,HW_Used=cdse_top(MODEL_PART,HW_Cur,DATA_TYPE,log,i,acc)
                layer_cycle_temp[index_temp]=time_layer
                print(HW_Cur)
                print(MODEL_PART)
                print(temp_config[acc,:])
                print('\n')
                HW_LEFT = np.subtract(HW_LEFT,HW_Used)
                if temp_cycle[acc,0]==1e30:
                    print('No solution find for partition',end=" ") 
                    print(comb[i],end=" ")
                    print('because of Acc' + str(acc))
                    break
                
            max_cycle=np.max(temp_cycle)
            if max_cycle<=best_cycle:
                layer_cycle=layer_cycle_temp.copy()
                part_final=index_origin.copy()
                best_cycle=max_cycle
                final_config=temp_config.copy()
            print('Partition ' + str(i) + ' out of ' + str(round) + ' finish')
            print('Estimated Throughput is: ' + str(total_ops/max_cycle) + ' GOPS\n\n' )
            print('##################################')

        print("Final Solution for Partition is",end=" ")
        print(part_final)
        print(final_config)
        print(layer_cycle)
        print('Estimated Latency is: ' + str(best_cycle*1e-6) + ' ms' )
        print('Estimated Throughput is: ' + str(total_ops/best_cycle) + ' GOPS' )
        return part_final, final_config, layer_cycle
            





