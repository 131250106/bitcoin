import sys
import threading

from django.shortcuts import render
from utils import get_data

sys.path.append('../')

from main import *


def inittree(request):
    setMode("pow")
    request.session['type'] = "pow"
    request.session['topo'] = "tree"
    startNet(node_num=8)
    updateJson(request)
    return render(request, 'init.html')

def initcircle(request):
    setMode("pow")
    request.session['type'] = "pow"
    request.session['topo'] = "circle"
    startNet()
    updateJson(request)
    return render(request, 'init.html')

def initnet(request):
    setMode("pow")
    request.session['type'] = "pow"
    request.session['topo'] = "net"
    startNet()
    updateJson(request)
    return render(request, 'init.html')


def initpow(request):
    setMode("pow")
    request.session['type'] = "pow"
    request.session['topo'] = "star"
    startNet()
    updateJson(request)
    return render(request, 'init.html')


def initpos(request):
    setMode("pos")
    request.session['type'] = "pos"
    request.session['topo'] = "star"
    startNet()
    updateJson(request)
    return render(request, 'init.html')

def initPBFT(request):
    setMode("PBFT")
    request.session['type'] = "PBFT"
    request.session['topo'] = "star"
    startNet()
    updateJson(request)
    return render(request, 'init.html')


def initBGP(request):
    setMode("pow")
    request.session['type'] = "BGP"
    request.session['topo'] = "star"
    startNet(attack="BGP", attack_num=1)
    updateJson(request)
    return render(request, 'init.html')

def initdouble(request):
    setMode("pow")
    request.session['type'] = "pow"
    request.session['topo'] = "star"
    startNet(attack="double", attack_num=1)
    updateJson(request)
    return render(request, 'init.html')


def updateJson(request):

    topo = request.session.get('topo')

    if topo == 'star':
        p2p_json = ['[\n', '{"source":"s1","target":"s1","region":"switch1"},\n']
        with open(os.path.join(cur_path, 'Logs/main'), 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                line_split = line.strip().split()

                if i == len(lines) - 1:
                    if line_split[-1] == "BGP":
                        p2p_line = '{"source":"%s","target":"%s","region":"(%s:9000)"}\n' % (
                            line_split[1], line_split[1], line_split[0])
                    else:
                        p2p_line = '{"source":"%s","target":"s1","region":"(%s:9000)"}\n' % (
                        line_split[1], line_split[0])
                else:
                    if line_split[-1] == "BGP":
                        p2p_line = '{"source":"%s","target":"%s","region":"(%s:9000)"},\n' % (
                            line_split[1], line_split[1], line_split[0])
                    else:
                        p2p_line = '{"source":"%s","target":"s1","region":"(%s:9000)"},\n' % (
                        line_split[1], line_split[0])
                p2p_json.append(p2p_line)

        p2p_json.append(']\n')

    elif topo == 'net':
        p2p_json = ['[\n']
        with open(os.path.join(cur_path, 'Logs/main'), 'r') as f:
            lines = f.readlines()
            for i, _ in enumerate(lines):
                line0 = lines[i].strip().split()

                for j in range(0,len(lines)):
                    line1 = lines[j].strip().split()
                    if i == len(lines) - 1 and j == len(lines) - 1:
                        p2p_line = '{"source":"%s","target":"%s","region":"(%s:9000)"}\n' % (
                        line0[1], line1[1], line1[0])
                    else:
                        p2p_line = '{"source":"%s","target":"%s","region":"(%s:9000)"},\n' % (
                            line0[1], line1[1], line1[0])
                    p2p_json.append(p2p_line)


        p2p_json.append(']\n')

    elif topo == 'circle':
        p2p_json = ['[\n']
        with open(os.path.join(cur_path, 'Logs/main'), 'r') as f:
            lines = f.readlines()
            for i, _ in enumerate(lines):
                line0 = lines[i].strip().split()
                p2p_line = '{"source":"%s","target":"%s","region":"(%s:9000)"},\n' % (
                    line0[1], line0[1], line0[0])
                p2p_json.append(p2p_line)

                if i == len(lines) - 1:
                    line1 = lines[0].strip().split()
                    p2p_line = '{"source":"%s","target":"%s","region":"(%s:9000)"}\n' % (
                        line0[1], line1[1], line1[0])
                else:
                    line1 = lines[i + 1].strip().split()
                    p2p_line = '{"source":"%s","target":"%s","region":"(%s:9000)"},\n' % (
                        line0[1], line1[1], line1[0])

                p2p_json.append(p2p_line)

        p2p_json.append(']\n')

    elif topo == 'tree' :
        p2p_json = ['[\n', '{"source":"s1","target":"s1","region":"switch1"},\n']
        with open(os.path.join(cur_path, 'Logs/main'), 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                line_split = line.strip().split()

                if i == len(lines) - 1:
                    if line_split[-1] == "BGP":
                        p2p_line = '{"source":"%s","target":"%s","region":"(%s:9000)"}\n' % (
                            line_split[1], line_split[1], line_split[0])
                    else:
                        p2p_line = '{"source":"%s","target":"s1","region":"(%s:9000)"}\n' % (
                            line_split[1], line_split[0])
                else:
                    if line_split[-1] == "BGP":
                        p2p_line = '{"source":"%s","target":"%s","region":"(%s:9000)"},\n' % (
                            line_split[1], line_split[1], line_split[0])
                    else:
                        p2p_line = '{"source":"%s","target":"s1","region":"(%s:9000)"},\n' % (
                            line_split[1], line_split[0])
                p2p_json.append(p2p_line)

        p2p_json.append(']\n')



    with open(os.path.join(cur_path, 'bitcoin/demo/static/data/p2p.json'), 'w') as f:
        f.writelines(p2p_json)


def startNet(attack="none",attack_num=1,node_num=6):
    try:
        delete_log()
        deleteCMD()
        setupP2PNet(node_num, 1, netType='star',attack=attack,attack_num=1)
        recordNodesInfo(attack=attack,attack_num=attack_num)

        threads = []
        t1 = threading.Thread(target=fileCommand)
        threads.append(t1)

        for t in threads:
            t.setDaemon(True)
            t.start()

        # myCommand().cmdloop();
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        traceback.print_stack()

        os.system("killall -SIGKILL xterm")
        os.system("mn --clean > /dev/null 2>&1")


def close(request):
    os.system("killall -SIGKILL xterm")
    os.system("mn --clean > /dev/null 2>&1")
    return render(request, 'close.html')


def add(request):
    with open(os.path.join(cur_path, 'CMD/main'), 'w') as f:
        f.write('addNode\n')

    sleep(3)
    print('in add')

    updateJson(request)

    sleep(1)

    host_name = request.session.get('hostname')
    host_ip = ""
    host_id = ""
    host_addr = ""
    block_info = []

    with open(os.path.join(cur_path, 'Logs/main'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line_split = line.strip().split()
            if line_split[1] == host_name:
                host_ip = line_split[0]
                break

    folder_path = os.path.join(cur_path, 'Logs/' + host_ip)
    base_info_path = os.path.join(folder_path, 'baseInfo')
    block_info_path = os.path.join(folder_path, 'BlockInfo')
    TX_info_path = os.path.join(folder_path, 'TXInfo')
    wallet_path = os.path.join(folder_path, 'wallet')

    with open(base_info_path, 'r') as f:
        lines = f.readlines()
        host_id = lines[0].strip()
        host_addr = lines[1].strip()

    block_info = get_data(block_info_path)
    tx_info = get_data(TX_info_path)
    wallet_info = get_data(wallet_path)

    return render(request, 'index.html', {'host_name': host_name,
                                          'base_info': [host_id, host_addr],
                                          'block_info': block_info,
                                          'tx_info': tx_info,
                                          'wallet_info': wallet_info,
                                          })


def delete(request):
    host_name = request.session.get('hostname')

    with open(os.path.join(cur_path, 'CMD/main'), 'w') as f:
        f.write('delNode '+host_name+'\n')

    sleep(3)

    updateJson(request)

    sleep(1)

    host_name = 'h1s1'
    request.session['hostname'] = host_name
    host_ip = ""
    host_id = ""
    host_addr = ""
    block_info = []

    with open(os.path.join(cur_path, 'Logs/main'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line_split = line.strip().split()
            if line_split[1] == host_name:
                host_ip = line_split[0]
                break

    folder_path = os.path.join(cur_path, 'Logs/' + host_ip)
    base_info_path = os.path.join(folder_path, 'baseInfo')
    block_info_path = os.path.join(folder_path, 'BlockInfo')
    TX_info_path = os.path.join(folder_path, 'TXInfo')
    wallet_path = os.path.join(folder_path, 'wallet')

    with open(base_info_path, 'r') as f:
        lines = f.readlines()
        host_id = lines[0].strip()
        host_addr = lines[1].strip()

    block_info = get_data(block_info_path)
    tx_info = get_data(TX_info_path)
    wallet_info = get_data(wallet_path)

    return render(request, 'index.html', {'host_name': host_name,
                                          'base_info': [host_id, host_addr],
                                          'block_info': block_info,
                                          'tx_info': tx_info,
                                          'wallet_info': wallet_info,
                                          })


def get_node_info(request):
    host_name = request.GET.get('hostname')
    request.session['hostname'] = host_name

    if host_name[0] == 's':
        host_name = 'h1s1'
        request.session['hostname'] = 'h1s1'

    host_ip = ""
    host_id = ""
    host_addr = ""
    block_info = []

    print(host_name)

    with open(os.path.join(cur_path, 'Logs/main'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line_split = line.strip().split()
            if line_split[1] == host_name:
                host_ip = line_split[0]
                break

    print(host_ip)

    folder_path = os.path.join(cur_path, 'Logs/' + host_ip)
    base_info_path = os.path.join(folder_path, 'baseInfo')
    block_info_path = os.path.join(folder_path, 'BlockInfo')
    TX_info_path = os.path.join(folder_path, 'TXInfo')
    wallet_path = os.path.join(folder_path, 'wallet')

    print(base_info_path)

    with open(base_info_path, 'r') as f:
        lines = f.readlines()
        host_id = lines[0].strip()
        host_addr = lines[1].strip()

    block_info = get_data(block_info_path)
    tx_info = get_data(TX_info_path)
    wallet_info = get_data(wallet_path)

    return render(request, 'index.html', {'host_name': host_name,
                                          'base_info': [host_id, host_addr],
                                          'block_info': block_info,
                                          'tx_info': tx_info,
                                          'wallet_info': wallet_info,
                                          })

def mine(request):
    host_name = request.session.get('hostname')
    host_ip = ""
    host_id = ""
    host_addr = ""
    block_info = []

    with open(os.path.join(cur_path, 'Logs/main'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line_split = line.strip().split()
            if line_split[1] == host_name:
                host_ip = line_split[0]
                break

    with open(os.path.join(cur_path, 'CMD/'+host_ip), 'w') as f:
        f.write('mine\n')

    folder_path = os.path.join(cur_path, 'Logs/' + host_ip)
    base_info_path = os.path.join(folder_path, 'baseInfo')
    block_info_path = os.path.join(folder_path, 'BlockInfo')
    TX_info_path = os.path.join(folder_path, 'TXInfo')
    wallet_path = os.path.join(folder_path, 'wallet')

    sleep(3)

    with open(base_info_path, 'r') as f:
        lines = f.readlines()
        host_id = lines[0].strip()
        host_addr = lines[1].strip()

    block_info = get_data(block_info_path)
    tx_info = get_data(TX_info_path)
    wallet_info = get_data(wallet_path)

    return render(request, 'index.html', {'host_name': host_name,
                                          'base_info': [host_id, host_addr],
                                          'block_info': block_info,
                                          'tx_info': tx_info,
                                          'wallet_info': wallet_info,
                                          })

def PBFT(request):
    host_name = request.session.get('hostname')
    host_ip = ""
    host_id = ""
    host_addr = ""
    block_info = []

    with open(os.path.join(cur_path, 'Logs/main'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line_split = line.strip().split()
            if line_split[1] == host_name:
                host_ip = line_split[0]
                break

    with open(os.path.join(cur_path, 'CMD/'+host_ip), 'w') as f:
        f.write('PBFT\n')

    folder_path = os.path.join(cur_path, 'Logs/' + host_ip)
    base_info_path = os.path.join(folder_path, 'baseInfo')
    block_info_path = os.path.join(folder_path, 'BlockInfo')
    TX_info_path = os.path.join(folder_path, 'TXInfo')
    wallet_path = os.path.join(folder_path, 'wallet')

    sleep(3)

    with open(base_info_path, 'r') as f:
        lines = f.readlines()
        host_id = lines[0].strip()
        host_addr = lines[1].strip()

    block_info = get_data(block_info_path)
    tx_info = get_data(TX_info_path)
    wallet_info = get_data(wallet_path)

    return render(request, 'index.html', {'host_name': host_name,
                                          'base_info': [host_id, host_addr],
                                          'block_info': block_info,
                                          'tx_info': tx_info,
                                          'wallet_info': wallet_info,
                                          })



def BGPattack(request):
    host_name = request.session.get('hostname')
    host_ip = ""
    host_id = ""
    host_addr = ""
    block_info = []

    with open(os.path.join(cur_path, 'Logs/main'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line_split = line.strip().split()
            if line_split[1] == host_name:
                host_ip = line_split[0]
                break

    with open(os.path.join(cur_path, 'CMD/'+host_ip), 'w') as f:
        f.write('join\n')

    with open(os.path.join(cur_path, 'CMD/main'), 'w') as f:
        f.write('recordNodesInfo\n')


    folder_path = os.path.join(cur_path, 'Logs/' + host_ip)
    base_info_path = os.path.join(folder_path, 'baseInfo')
    block_info_path = os.path.join(folder_path, 'BlockInfo')
    TX_info_path = os.path.join(folder_path, 'TXInfo')
    wallet_path = os.path.join(folder_path, 'wallet')

    sleep(4)

    updateJson(request)

    with open(base_info_path, 'r') as f:
        lines = f.readlines()
        host_id = lines[0].strip()
        host_addr = lines[1].strip()

    block_info = get_data(block_info_path)
    tx_info = get_data(TX_info_path)
    wallet_info = get_data(wallet_path)

    print(host_id, host_addr)
    print(block_info)
    print(tx_info)

    return render(request, 'index.html', {'host_name': host_name,
                                          'base_info': [host_id, host_addr],
                                          'block_info': block_info,
                                          'tx_info': tx_info,
                                          'wallet_info': wallet_info,
                                          })



def send_tx(request):
    host_name = request.session.get('hostname')
    receive_ip = request.GET.get('receive_ip')
    amount = request.GET.get('amount')
    host_ip = ""
    host_id = ""
    host_addr = ""
    block_info = []

    print(receive_ip)
    print(amount)

    with open(os.path.join(cur_path, 'Logs/main'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line_split = line.strip().split()
            if line_split[1] == host_name:
                host_ip = line_split[0]
                break

    with open(os.path.join(cur_path, 'CMD/' + host_ip), 'w') as f:
        strs = ['createTx',receive_ip,amount]

        f.write(' '.join(strs)+'\n')

    folder_path = os.path.join(cur_path, 'Logs/' + host_ip)
    base_info_path = os.path.join(folder_path, 'baseInfo')
    block_info_path = os.path.join(folder_path, 'BlockInfo')
    TX_info_path = os.path.join(folder_path, 'TXInfo')
    wallet_path = os.path.join(folder_path, 'wallet')

    sleep(3)

    with open(base_info_path, 'r') as f:
        lines = f.readlines()
        host_id = lines[0].strip()
        host_addr = lines[1].strip()

    block_info = get_data(block_info_path)
    tx_info = get_data(TX_info_path)
    wallet_info = get_data(wallet_path)

    return render(request, 'index.html', {'host_name': host_name,
                                          'base_info': [host_id, host_addr],
                                          'block_info': block_info,
                                          'tx_info': tx_info,
                                          'wallet_info': wallet_info,
                                          })

def index(request):
    host_name = 'h1s1'
    request.session['hostname'] = host_name
    host_ip = "10.0.0.1"
    host_id = ""
    host_addr = ""
    block_info = []

    with open(os.path.join(cur_path, 'Logs/main'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line_split = line.strip().split()
            if line_split[1] == host_name:
                host_ip = line_split[0]
                break

    folder_path = os.path.join(cur_path, 'Logs/' + host_ip)
    base_info_path = os.path.join(folder_path, 'baseInfo')
    block_info_path = os.path.join(folder_path, 'BlockInfo')
    TX_info_path = os.path.join(folder_path, 'TXInfo')
    wallet_path = os.path.join(folder_path, 'wallet')

    with open(base_info_path, 'r') as f:
        lines = f.readlines()
        host_id = lines[0].strip()
        host_addr = lines[1].strip()

    block_info = get_data(block_info_path)
    tx_info = get_data(TX_info_path)
    wallet_info = get_data(wallet_path)


    return render(request, 'index.html', {'host_name': host_name,
                                          'base_info': [host_id, host_addr],
                                          'block_info': block_info,
                                          'tx_info': tx_info,
                                          'wallet_info': wallet_info,
                                          })
