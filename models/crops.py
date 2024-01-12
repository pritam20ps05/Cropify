cropsdata = {
    'rice': {
        'fullname': 'Rice',
        'params': [150, 35, 60, 6, 2]
    },
    'wheat': {
        'fullname': 'Wheat',
        'params': [100, 40, 60, 7, 2]
    },
    'maize': {
        'fullname': 'Maize',
        'params': [150, 35, 60, 6, 2]
    },
    'lentils': {
        'fullname': 'Lentils',
        'params': [20, 40, 20, 7, 2]
    },
    'sugarcane': {
        'fullname': 'Sugarcane',
        'params': [150, 35, 60, 6, 2]
    },
    'potato': {
        'fullname': 'Potato',
        'params': [150, 35, 120, 6, 2]
    },
    'pea': {
        'fullname': 'Pea',
        'params': [80, 30, 50, 6, 2]
    },
}

def suggestCrops(inp: list):
    crops = []
    for crop in cropsdata.keys():
        v = True
        for i, param in enumerate(cropsdata[crop]['params'][:-1]):
            dev = abs((inp[i] - param)/param)
            if dev>0.5:
                v = False
        if inp[4] > cropsdata[crop]['params'][4]:
            ecdev = abs((inp[4] - cropsdata[crop]['params'][4])/cropsdata[crop]['params'][4])
            if ecdev>0.5:
                v = False
        if v:
            crops.append(cropsdata[crop]['fullname'])
    return crops