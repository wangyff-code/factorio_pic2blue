import copy
import json
import base64
import zlib
import os
from fac_dir import *


class gen_mat():
    def __init__(self,point_list,p1,item_name):
        self.point_list = point_list
        self.p1 = p1
        self.gen_type,self.item_list = item_name 

    def gen_block(self,id_,name,x,y):
        block_dir['position']['x'] = x
        block_dir['position']['y'] = y
        block_dir['name'] = name
        return block_dir

    def gen_block_sig(self):
        item_list = []
        count = 0
        name = self.item_list[0]
        x, y = self.point_list.shape[0:2]
        for i in range(0,x):
            self.p1["value"] = i/x*100
            for k in range(0,y):
                if self.point_list[i][k] == 0:
                    item_list.append(copy.deepcopy(self.gen_block(count,name,k - y//2,i - x//2)))
                    count +=1
        return item_list

    def gen_block_dou(self):
            item_list = []
            count = 0
            name1 = item_list[0]
            name2 = item_list[1]
            x, y = point_list.shape[0:2]
            for i in range(0,x):
                self.p1["value"] = i/x*100
                for k in range(0,y):
                    if self.point_list[i][k] == 0:
                        item_list.append(copy.deepcopy(self.gen_block(count,name1,k - y//2,i - x//2)))
                        count +=1
                    else:
                        item_list.append(copy.deepcopy(self.gen_block(count,name2,k - y//2,i - x//2)))
                        count +=1
            return item_list

    def strat_trans(self):
        if gen_type == 0:
            item_list=self.gen_block_sig()
        if gen_type == 1:
            item_list=self.gen_block_dou(point_list,item_list[0],item_list[1])
        body_dir['blueprint']['tiles'] = item_list
        self.pack_dir(body_dir)

    def pack_dir(self.dir_data):
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