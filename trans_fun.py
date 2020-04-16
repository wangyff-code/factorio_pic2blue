import copy
import json
import base64
import zlib
import os
from fac_dir import *
import numpy as np

item_id_dir={0:'stone-path',1:'stone-path',2:'stone-path',3:'stone-path',4:'stone-path',5:'stone-path',6:'stone-path',7:'stone-path',8:'stone-path',9:'stone-path',10:'stone-path',11:'stone-path',12:'stone-path',}



class gen_solar_station():
    def __init__(self,flam,k_balance,p1):
        self.p1 = p1
        self.k_balance = k_balance
        self.solar_number = 0
        self.battery_number = 0
        self.item_list = []
        self.ground_list = []
        self.id = 0
        self.flam = flam

    def gen_block(self,name,x,y):
        so_dir["entity_number"] = self.id 
        so_dir['position']['x'] = x
        so_dir['position']['y'] = y
        so_dir['name'] = name
        self.id += 1
        self.item_list.append(copy.deepcopy(so_dir))

    def gen_ground(self,name,x,y):
        block_dir['position']['x'] = x
        block_dir['position']['y'] = y
        block_dir['name'] = name
        self.ground_list.append(copy.deepcopy(block_dir))

    def gen_solarBlock(self,px, py):
        self.solar_number += 4
        for i in range(0, 2):
            for k in range(0, 2):
                self.gen_block("solar-panel",px+i*3+0.5, py+k*3+0.5)


    def gen_powerBlock0(self,px, py):
        temp = np.array([[0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 1, 0, 0],
                        [0, 0, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],]
                        )
        for i in range(0, 6):
            for k in range(0, 6):
                if temp[i][k] == 0:
                    self.gen_ground('stone-path',px+i, py+k)
        self.gen_block('substation',px+2.5, py+2.5)


    def gen_powerBlock1(self,px, py):
        self.battery_number +=8
        for i in range(0, 3):
            for k in range(0, 3):
                if i != 1 or k != 1:
                    self.gen_block('accumulator',px+i*2+0.5, py+k*2+0.5)
        self.gen_block('substation',px+2.5, py+2.5)


    def gen_batteryBlock(self,px, py):
        self.battery_number +=9
        for i in range(0, 3):
            for k in range(0, 3):
                self.gen_block('accumulator',px+i*2+0.5, py+k*2+0.5)

    def add_solar(self,i_start,k_limit,add_number,hx,hy):
        i = i_start
        while True:
            i+=1
            for k in range(0,k_limit):
                if i % 3 == 0 and k % 3 == 0:
                    self.gen_powerBlock0(i*6-hx, k*6-hy)
                    add_number -=0
                else:
                    self.gen_solarBlock(i*6-hx, k*6-hy)
                    add_number -=4
            if add_number <=0:
                break


    def add_battery(self,i_start,k_limit,add_number,hx,hy):
        i = i_start
        while True:
            i+=1
            for k in range(0,k_limit):
                if i % 3 == 0 and k % 3 == 0:
                    self.gen_powerBlock1(i*6-hx, k*6-hy)
                    add_number -=8
                else:
                    self.gen_batteryBlock(i*6-hx, k*6-hy)
                    add_number -=9
            if add_number <=0:
                break


    def gen_SolarStation(self,flam):
        x, y = flam.shape
        hx = x*3
        hy = y*3
        for i in range(0, x):
            self.p1["value"] = i/x*100
            for k in range(0, y):
                if i % 3 == 0 and k % 3 == 0:
                    if(flam[i][k] == 0):
                        self.gen_powerBlock0(i*6-hx, k*6-hy)
                    else:
                        self.gen_powerBlock1(i*6-hx, k*6-hy)
                else:
                    if(flam[i][k] == 0):
                        self.gen_solarBlock(i*6-hx, k*6-hy)
                    else:
                        self.gen_batteryBlock(i*6-hx, k*6-hy)

        now_k = self.battery_number/self.solar_number
        if now_k > self.k_balance:
            add_number = int(self.battery_number/self.k_balance) - self.solar_number
            self.add_solar(i,y,add_number,hx,hy)
        else:
            add_number = int(self.solar_number*self.k_balance) - self.battery_number
            self.add_battery(i,y,add_number,hx,hy)

    def strat_trans(self):
            self.gen_SolarStation(self.flam)
            so_bdy_dir['blueprint']['entities'] = self.item_list
            so_bdy_dir['blueprint']['tiles'] = self.ground_list
            self.pack_dir(so_bdy_dir)

    def pack_dir(self,dir_data):
            data = json.dumps(dir_data)
            data.replace(' ','')
            data.replace('\n','')
            st = data.encode('utf-8')
            st = zlib.compress(st)
            out = base64.b64encode(st).decode()
            out = '0' + out
            f = open('output.txt','w')
            f.write(out)
            f.close()
            os.startfile(r'output.txt')


class gen_mat():
    def __init__(self):
        pass

    def set_gen(self,gen_type,item_list,k,p1):
        self.p1 = p1
        self.gen_type = gen_type
        self.item_list = item_list
        self.k_balance = k
    
    def set_pix(self,pix_array):
        self.pix_array = pix_array

    def gen_block(self,id_,name,x,y):
        block_dir['position']['x'] = x
        block_dir['position']['y'] = y
        block_dir['name'] = name
        return block_dir

    def gen_block_sig(self):
        item_list = []
        count = 0
        name = self.item_list[0]
        x, y = self.pix_array.shape[0:2]
        for i in range(0,x):
            self.p1["value"] = i/x*100
            for k in range(0,y):
                if self.pix_array[i][k] == 0:
                    item_list.append(copy.deepcopy(self.gen_block(count,name,k - y//2,i - x//2)))
                    count +=1
        return item_list

    def gen_block_dou(self):
            item_list = []
            count = 0
            name1 = self.item_list[0]
            name2 = self.item_list[1]
            x, y = self.pix_array.shape[0:2]
            for i in range(0,x):
                self.p1["value"] = i/x*100
                for k in range(0,y):
                    if self.pix_array[i][k] == 0:
                        item_list.append(copy.deepcopy(self.gen_block(count,name1,k - y//2,i - x//2)))
                        count +=1
                    else:
                        item_list.append(copy.deepcopy(self.gen_block(count,name2,k - y//2,i - x//2)))
                        count +=1
            return item_list

    def gen_block_color(self):
        item_list = []
        count = 0
        x, y = self.pix_array.shape[0:2]
        for i in range(0,x):
            self.p1["value"] = i/x*100
            for k in range(0,y):
                name = item_id_dir[self.pix_array[i][k]]
                item_list.append(copy.deepcopy(self.gen_block(count,name,k - y//2,i - x//2)))
                count +=1
        return item_list

    def strat_trans(self):
        if self.gen_type == 0:
            item_list=self.gen_block_sig()
        if self.gen_type == 1:
            item_list=self.gen_block_dou()
        if self.gen_type == 2:
            gen_s = gen_solar_station(self.pix_array.T,self.k_balance,self.p1)
            gen_s.strat_trans()
            return
        if self.gen_type == 3:
            item_list=self.gen_block_color()
        body_dir['blueprint']['tiles'] = item_list
        self.pack_dir(body_dir)

    def pack_dir(self,dir_data):
        data = json.dumps(dir_data)
        data.replace(' ','')
        data.replace('\n','')
        st = data.encode('utf-8')
        st = zlib.compress(st)
        out = base64.b64encode(st).decode()
        out = '0' + out
        f = open('output.txt','w')
        f.write(out)
        f.close()
        os.startfile(r'output.txt')