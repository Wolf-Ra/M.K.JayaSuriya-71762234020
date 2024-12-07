import json

f=open('Input\Input\Milestone0.json')
data = json.load(f)

steps = dict()
for i in range(len(data['steps'])):
    temp_val_dict = dict()
    temp_val_dict['max'] = data['steps'][i]['parameters']['P1'][1]
    temp_val_dict['min'] = data['steps'][i]['parameters']['P1'][0]
    temp_val_dict['dependency'] = data['steps'][i]['dependency']
    steps[data['steps'][i]['id']] = temp_val_dict
    temp_val_dict = dict()

#print(steps)

machines = dict()
for i in range(len(data['machines'])):
    temp_val_dict = dict()
    temp_val_dict['S_id'] = data['machines'][i]['step_id']
    temp_val_dict['cooling_time'] = data['machines'][i]['cooldown_time']
    
    param_dict = dict()
    for param in data['machines'][i]['initial_parameters'].keys():
        param_dict[param] = data['machines'][i]['initial_parameters'][param]
    
    fluc_dict = dict()
    for param in data['machines'][i]['fluctuation'].keys():
        fluc_dict[param] = data['machines'][i]['fluctuation'][param]


    temp_val_dict['init_param_valc'] = param_dict
    temp_val_dict['param_fluc'] = fluc_dict
    temp_val_dict['count'] = data['machines'][i]['n']
    machines[data['machines'][i]['machine_id']] = temp_val_dict
    temp_val_dict = dict()

#print(machines)

wafer = dict()
for w in range(len(data['wafers'])):
    temp_val_dict = dict()
    temp_val_dict['process_time'] = data['wafers'][w]['processing_times']
    temp_val_dict['quantity'] = data['wafers'][w]['quantity']
    wafer[data['wafers'][w]['type']] = temp_val_dict
    temp_val_dict = dict()

print(steps)
print("")
print(machines)
print("")
print(wafer)

#initially :
wafers_process = dict()
for sheet in wafer.keys():
    for num in range(wafer[sheet]['quantity']):
        wafers_process[sheet+"-"+str(num+1)] = []

machine_time = dict()
for m in machines.keys():
    machine_time[m] = 0

mach_status = dict()
for mac in machines.keys():
    mach_status[mac] = 'Free'

print("")
print(wafers_process)
print(machine_time)
print(mach_status)

schedule=dict()
allocation = []
list_wafer = []
for waf in wafers_process.keys():
    list_wafer.append(waf)



for quant in range(len(list_wafer)):
    if machine_time['M1']<machine_time['M2']:
        mach_status['M1'] = 'Free'
    else:
        machine_time['M2'] = machine_time['M1']
        mach_status['M1'] = 'Free'

    if machine_time['M1']>machine_time['M2']:
        mach_status['M2'] = 'Free'
    else:
        machine_time['M1'] = machine_time['M2']
        mach_status['M2'] = 'Free'


    if 'S1' not in wafers_process[list_wafer[quant]] and mach_status['M1'] != 'Busy':
        wafers_process[list_wafer[quant]].append('S1')
        init_time = machine_time['M1']
        machine_time['M1'] = init_time + wafer['W1']['process_time']['S1']
        mach_status['M1'] = 'Busy'
        schedule['wafer_id'] = list_wafer[quant]
        schedule['step'] = 'S1'
        schedule['machine'] = 'M1'
        schedule['start_time'] = init_time
        schedule['end_time'] = machine_time['M1']
        allocation.append(schedule)
        schedule = dict()
        init_time = machine_time['M1']
    else:
        continue
    if 'S2' not in wafers_process[list_wafer[len(list_wafer)-(quant+1)]] and mach_status['M2'] != 'Busy':
        wafers_process[list_wafer[len(list_wafer)-(quant+1)]].append('S2')
        init_time = machine_time['M2']
        machine_time['M2'] = init_time + wafer['W1']['process_time']['S2']
        mach_status['M2'] = 'Busy'
        schedule['wafer_id'] = list_wafer[len(list_wafer)-(quant+1)]
        schedule['step'] = 'S2'
        schedule['machine'] = 'M2'
        schedule['start_time'] = init_time
        schedule['end_time'] = machine_time['M2']
        allocation.append(schedule)
        schedule = dict()
        init_time = machine_time['M2']
    else:
        continue
    
for i in range(len(allocation)):
    print(allocation[i])

scheduledict = dict()
scheduledict['schedule'] = allocation

print(scheduledict)

# Convert and write JSON object to file
with open("Milestone0Solution.json", "w") as outfile: 
    json.dump(scheduledict, outfile, indent=4)
