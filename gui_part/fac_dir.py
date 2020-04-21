body_dir = {
    "blueprint": {
        "icons": [
            {
                "signal": {
                    "type": "item",
                    "name": "stone-brick"
                },
                "index": 1
            }
        ],
        "tiles": [
            {
                "position": {
                    "x": -1,
                    "y": -1
                },
                "name": "stone-path"
            }, {
                "position": {
                    "x": -1,
                    "y": 0
                },
                "name": "stone-path"
            }, {
                "position": {
                    "x": 0,
                    "y": -1
                },
                "name": "stone-path"
            }, {
                "position": {
                    "x": 0,
                    "y": 0
                },
                "name": "stone-path"
            }
        ],
        "item": "blueprint",
        "version": 73019621376
    }
}

so_bdy_dir={
    "blueprint": {
        "icons": [
            {
                "signal": {
                    "type": "item",
                    "name": "solar-panel"
                },
                "index": 1
            }, {
                "signal": {
                    "type": "item",
                    "name": "accumulator"
                },
                "index": 2
            }
        ],
        "entities": [
            {
                "entity_number": 1,
                "name": "solar-panel",
                "position": {
                    "x": -5,
                    "y": -2
                }
            }
        ],
        "item": "blueprint",
        "version": 73019621376
    }
}

so_dir = {
                "entity_number": 2,
                "name": "solar-panel",
                "position": {
                    "x": -2,
                    "y": -2
                }
}

block_dir = {
                "position": {
                    "x": -1,
                    "y": -1
                },
                "name": "stone-path"
            }

color_list = [[66, 158, 206], [148, 93, 0], [0, 89, 107], [164, 129, 66],
              [148, 101, 25], [173, 129, 58], [206, 214, 206], [123, 125, 123],
              [74, 81, 82], [58, 61, 58], [33, 142, 181], [41, 49, 49],
              [25, 93, 115]]


item_color_dir ={   0:{'name':'基础传送带', 'color':[66,158,206],'isEntity':True},
                    1:{'name':'铁箱',       'color':[148,93,0],'isEntity':True},
                    2:{'name':'地下传送带', 'color':[0,89,107],'isEntity':True},
                    3:{'name':'管道',       'color':[164,129,66],'isEntity':True},
                    4:{'name':'地下管道',    'color':[148,101,25],'isEntity':True},
                    5:{'name':'热管',    'color':[173,129,58],'isEntity':True},
                    6:{'name':'石墙',    'color':[206,214,206],'isEntity':True},
                    7:{'name':'闸门',    'color':[123,125,123],'isEntity':True},
                    8:{'name':'石砖',    'color':[74,81,82],'isEntity':False},
                    9:{'name':'混凝土',   'color':[58,61,58],'isEntity':False},
                    10:{'name':'钢筋混凝土',   'color':[33,142,181],'isEntity':False},
                    11:{'name':'标记混凝土',   'color':[41,49,49],'isEntity':False},
                    12:{'name':'钢筋标记混凝土',   'color':[25,93,115],'isEntity':False}
}

scale_dir1  ={"缩放比例":0,"阈值下限":1,"边缘上限":2,"边缘下限":3}

scale_dir2  ={"缩放比例":0,"亮度增益":1,"亮度基准":2} 



color_dir ={0:
                {
                        "entity_number": 1,
                        "name": "transport-belt",
                        "position": {
                            "x": 0,
                            "y": 0
                        },
                        "direction": 2
                },
            1:{
                "entity_number": 1,
                "name": "iron-chest",
                "position": {
                    "x": 0,
                    "y": 0
                }
              },
            2:{
                "entity_number": 1,
                "name": "underground-belt",
                "position": {
                    "x": 0,
                    "y": 0
                },
                "direction": 2,
                "type": "input"
            },
            3:{
                "entity_number": 1,
                "name": "pipe",
                "position": {
                    "x": 0,
                    "y": 0
                }
            },
            4:{
                "entity_number": 1,
                "name": "pipe-to-ground",
                "position": {
                    "x": 0,
                    "y": 0
                }
            },
            5:{
                "entity_number": 1,
                "name": "heat-pipe",
                "position": {
                    "x": 0,
                    "y": 0
                }
            },
            6:{
                "entity_number": 1,
                "name": "stone-wall",
                "position": {
                    "x": 0,
                    "y": 0
                }
            },
            7:{
                "entity_number": 1,
                "name": "gate",
                "position": {
                    "x": 0,
                    "y": 0
                },
                "direction": 2
            },
            8:{
                "position": {
                    "x": 0,
                    "y": 0
                },
                "name": "stone-path"
            },
            9:{
                "position": {
                    "x": 0,
                    "y": 0
                },
                "name": "concrete"
            },
            10:{
                "position": {
                    "x": 0,
                    "y": 0
                },
                "name": "hazard-concrete-left"
            },
            11:{
                "position": {
                    "x": 0,
                    "y": 0
                },
                "name": "refined-concrete"
            },
            12:
            {
                "position": {
                    "x": 0,
                    "y": 0
                },
                "name": "refined-hazard-concrete-left"
            }
}