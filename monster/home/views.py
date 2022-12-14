from django.shortcuts import render
import paramiko
import json
# Create your views here.

def home(request):

    server_list = [
        {'name': 'SERVER18', 'host': '163.152.162.51', 'username': 'wonseok_roh', 'password': 'wonseok_roh'},
        {'name': 'SERVER16', 'host': '163.152.162.52', 'username': 'cvlab', 'password': '1234'},
    ]

    server_status = dict()

    for server in server_list:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh.connect(server['host'], username=server['username'], password=server['password'])
            print("======", server['name'] ,"CONNECTED ======")
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
                    split_line = list(filter(None, re.split(' ')))
                    gpu_temp = split_line[2]
                    gpu_curr = split_line[8]
                    gpu_full = split_line[10]
                    gpu_status[gpu_num]['temp'] = gpu_temp
                    gpu_status[gpu_num]['curr'] = gpu_curr
                    gpu_status[gpu_num]['full'] = gpu_full
            
            server_status[server['name']] = json.dumps(gpu_status)
        except Exception as err:
            print(err)
        print(server_status, '<=========== server status')

    return render(request, "monster.html", server_status)
