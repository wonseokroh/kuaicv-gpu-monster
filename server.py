import paramiko

server_list = [
    {'name': '18', 'host': '163.152.162.51', 'username': 'wonseok_roh', 'password': 'wonseok_roh'},
    {'name': '16', 'host': '163.152.162.52', 'username': 'cvlab', 'password': '1234'},
]

for server in server_list:
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(server['host'], username=server['username'], password=server['password'])
        print("====== SERVER", server['name'] ,"CONNECTED ======")
        stdin, stdout, stderr = ssh.exec_command("nvidia-smi")
        lines = stdout.readlines()

        gpu_status = list()
        for i in lines:
            re = str(i).replace('\n', '')
            if ' NVIDIA ' in re:
                split_line = re.split('  ')
                gpu_num = int(split_line[1].strip())
                gpu_model = split_line[2]
                gpu_status.append({'number': gpu_num, 'model': gpu_model})
            elif 'MiB' in re and 'Default' in re:
                split_line = re.split(' ')
                split_line = list(filter(None, split_line))
                # print(split_line_2, '<============= split line')
                gpu_temp = split_line[2]
                gpu_curr = split_line[8]
                gpu_full = split_line[10]
                gpu_status[gpu_num]['temp'] = gpu_temp
                gpu_status[gpu_num]['curr'] = gpu_curr
                gpu_status[gpu_num]['full'] = gpu_full
        print(gpu_status)
    except Exception as err:
        print(err)