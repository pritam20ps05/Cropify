def lmhClassifier(conc: float, norm_param: str, carr: list):
    minlimit, maxlimit = ((float)(vi) for vi in norm_param.split('-'))
    mindev = (minlimit - conc)/minlimit
    maxdev = (conc - maxlimit)/maxlimit

    if (conc>=minlimit) and (conc<=maxlimit):
        carr.append(2)
        return 'Medium'
    elif mindev>0 and mindev<=0.5:
        carr.append(1)
        return 'Low'
    elif mindev>0.5:
        carr.append(1)
        return 'Very Low'
    elif maxdev>0 and maxdev<=0.5:
        carr.append(1)
        return 'High'
    elif maxdev>0.5:
        carr.append(1)
        return 'Very High'

def phClassifier(ph: float, norm_param: str, carr: list):
    pd = ph - 7
    pda = abs(pd)

    pdcat = ""
    c = 1
    if pd<0:
        c = 1
        pdcat = 'Acidic'
    elif pd>0:
        c = 3
        pdcat = 'Alkaline'

    if pda==0:
        carr.append(2)
        return 'Neutral'
    elif pda>0 and pda<=2:
        carr.append(c)
        return f'Slightly {pdcat}'
    elif pda>2 and pda<=4:
        carr.append(c)
        return f'{pdcat}'
    elif pda>4:
        carr.append(c)
        return f'Highly {pdcat}'

def salineClassifier(ec: float, norm_param: str, carr: list):
    if ec>=0 and ec<=1:
        carr.append(2)
        return 'Normal'
    elif ec>1 and ec<=4:
        carr.append(2)
        return 'Very Slightly Saline'
    elif ec>4 and ec<=8:
        carr.append(1)
        return 'Slightly Saline'
    elif ec>8 and ec<=16:
        carr.append(1)
        return 'Moderately Saline'
    elif ec>16:
        carr.append(1)
        return 'Strongly Saline'
    
def microClassifier(conc: float, norm_param: str, carr: list):
    dp = norm_param[0]
    npm = (float)(norm_param[1:])

    if dp=='>':
        if conc>=npm:
            carr.append(2)
            return 'Sufficient'
        else:
            carr.append(1)
            return 'Defficient'
    elif dp=='<':
        if conc<=npm:
            carr.append(2)
            return 'Sufficient'
        else:
            carr.append(1)
            return 'Excess'
