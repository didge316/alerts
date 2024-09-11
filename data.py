def process_data(addy, name):
    vaults_below = 0
    collateral = 0
    data_list = []
    with open('data_log.txt', 'r') as file:
        data = file.readlines()
    for line in data:
        if len(line) > 5:
            line = line.strip()
            data_list.append(line)
            
    for line in data_list: 
            vaults_below += 1       
            sline = line.split('|')
            add_collateral = sline[2].replace(',','')
            add_collateral = float(add_collateral)
            collateral += add_collateral
            
            if sline[0] == addy:
                 
                 break
    collateral = round(collateral)
    collateral = "{:,}".format(collateral)
    
    
    message = (f'{name} | {addy[:5]}\n')
    message += (f'{vaults_below} Vaults Below\n')             
    message += (f'${collateral} Buffer\n\n')
    
    return message

