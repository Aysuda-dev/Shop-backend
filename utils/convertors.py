def group_list(custom_ist , size=4):
    group_list = []
    for item in range(0,len(custom_ist),size):
        group_list.append(custom_ist[item:item+size])
    return group_list