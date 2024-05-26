import os
import configparser
import platform
import subprocess
import shutil
import multiprocessing
import time

CONFIG_FILE = 'config.ini'

def input_mining_address():
    print("Please go to the following link to find your mining address:")
    print("https://www.nicehash.com/my/mining/rigs")
    mining_address = input(
        "Press 'mining address' on this page and paste it here: ")
    return mining_address


def input_worker_name():
    return input("Please provide your WorkerName: ")


def load_from_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        return (
            config['MINER'].get('MiningAddress'),
            config['MINER'].get('WorkerName'),
            config['MINER'].get('UseCpu'),
            config['MINER'].get('UseGpu'),
            config['MINER'].get('tls_flag'),
            config['MINER'].get('cpu_prio'),
            config['MINER'].get('change_fan_speed'),
            config['MINER'].get('fan_speed'),
            config['MINER'].get('mining_alg'),
            config['MINER'].get('protocol'),
            config['MINER'].get('mining_port'),
            config['MINER'].get('powerlimit'),
            config['MINER'].get('gpuoffset'),
            config['MINER'].get('memoffset'),
            config['MINER'].get('memoffsetcommand'),
            config['MINER'].get('gpuoffsetcommand'),
        )
    else:
        return None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None


def save_to_config(mining_address, worker_name, use_cpu, use_gpu, tls_flag, cpu_prio, change_fan_speed, fan_speed, mining_alg, protocol, mining_port, powerlimit, gpuoffset, memoffset, memoffsetcommand, gpuoffsetcommand):
    config = configparser.ConfigParser()
    config['MINER'] = {
        'MiningAddress': mining_address,
        'WorkerName': worker_name,
        'UseCpu': use_cpu,
        'UseGpu': use_gpu,
        'tls_flag': tls_flag,
        'cpu_prio': cpu_prio,
        'change_fan_speed': change_fan_speed,
        'fan_speed': fan_speed,
        'mining_alg': mining_alg,
        'protocol': protocol,
        'mining_port': mining_port,
        'powerlimit': powerlimit,
        'gpuoffset': gpuoffset,
        'memoffset': memoffset,
        'memoffsetcommand': memoffsetcommand,
        'gpuoffsetcommand': gpuoffsetcommand
    }
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def download_deps():
    if platform.system() == 'Linux':
        if shutil.which('7z') is None:
            subprocess.run(['sudo', 'pacman', '-Sy', 'p7zip'])
        if shutil.which('curl') is None:
            subprocess.run(['sudo', 'pacman', '-Sy', 'curl'])
        if shutil.which('wget') is None:
            subprocess.run(['sudo', 'pacman', '-Sy', 'wget'])
        if shutil.which('nvcc') is None:
            subprocess.run(['sudo', 'pacman', '-Sy', 'cuda'])

        if os.path.exists("xmrig"):
            print('xmrig found')
        else:
            subprocess.run(
                ['wget', 'https://github.com/xmrig/xmrig/releases/download/v6.21.3/xmrig-6.21.3-linux-static-x64.tar.gz'])
            subprocess.run(['7z', 'e', 'xmrig-6.21.3-linux-static-x64.tar.gz'])
            subprocess.run(['7z', 'e', 'xmrig-6.21.3-linux-static-x64.tar'])
            subprocess.run(['chmod', '+x', 'xmrig'])
        if os.path.exists("miniZ"):
            print('miniz found')
        else:
            subprocess.run(['curl', '-o', 'miniz.tar.gz',
                           'https://miniz.cc/?smd_process_download=1&download_id=5017'])
            subprocess.run(['7z', 'e', 'miniz.tar.gz'])
            subprocess.run(['7z', 'e', 'miniz.tar'])
            subprocess.run(['chmod', '+x', 'miniZ'])
        if os.path.exists("xmrig-6.21.3"):
            shutil.rmtree('xmrig-6.21.3')
        if os.path.exists("miniZ.sha256sum"):
            os.remove('miniZ.sha256sum')
        if os.path.exists("SHA256SUMS"):
            os.remove('SHA256SUMS')
        if os.path.exists("xmrig-6.21.3-linux-static-x64.tar.gz"):
            os.remove('xmrig-6.21.3-linux-static-x64.tar.gz')
        if os.path.exists("xmrig-6.21.3-linux-static-x64.tar"):
            os.remove('xmrig-6.21.3-linux-static-x64.tar')
        if os.path.exists("miniz.tar.gz"):
            os.remove('miniz.tar.gz')
        if os.path.exists("miniz.tar"):
            os.remove('miniz.tar')
    if platform.system() == 'Windows':
        if os.path.exists("miniZ.exe"):
            print("miniz found")
        else:
            print("Password is miniZ")
            print("Password is miniZ")
            print("Password is miniZ")
            time.sleep(2)
            subprocess.run(['powershell', '-Command', 'iwr',
                           'https://miniz.cc/?smd_process_download=1"&"download_id=5016', '-OutFile', '1.zip'])
            subprocess.run(['7z', 'e', '1.zip'])
        if os.path.exists("xmrig.exe"):
            print("xmrig found")
        else:
            subprocess.run(['powershell', '-Command', 'iwr',
                            'https://github.com/xmrig/xmrig/releases/download/v6.21.3/xmrig-6.21.3-msvc-win64.zip', '-OutFile', '2.zip'])
            subprocess.run(['7z', 'e', '2.zip'])
        if os.path.exists("xmrig-6.21.3"):
            shutil.rmtree('xmrig-6.21.3')
        if os.path.exists("miniZ.exe.sha256sum"):
            os.remove('miniZ.exe.sha256sum')
        if os.path.exists("SHA256SUMS"):
            os.remove('SHA256SUMS')
        if os.path.exists("miniZ_gui.exe"):
            os.remove('miniZ_gui.exe')
        if os.path.exists("miniZ_gui.exe.sha256sum"):
            os.remove('miniZ_gui.exe.sha256sum')
        if os.path.exists("1.zip"):
            os.remove('1.zip')
        if os.path.exists("2.zip"):
            os.remove('2.zip')
        if os.path.exists("pool_mine_example.cmd"):
            os.remove('pool_mine_example.cmd')
        if os.path.exists("rtm_ghostrider_example.cmd"):
            os.remove('rtm_ghostrider_example.cmd')
        if os.path.exists("solo_mine_example.cmd"):
            os.remove('solo_mine_example.cmd')
        if os.path.exists("start.cmd"):
            os.remove('start.cmd')
        if os.path.exists("benchmark_10M.cmd"):
            os.remove('benchmark_10M.cmd')
        if os.path.exists("benchmark_1M.cmd"):
            os.remove('benchmark_1M.cmd')


def run_xmrig(mining_address, worker_name, cpu_prio, protocol, mining_port, tls_flag):
    if platform.system() == 'Linux':
        xmrig_command = f'sudo ./xmrig -o stratum+{protocol}://randomxmonero.auto.nicehash.com:{mining_port} \
        -u {mining_address}.{worker_name} -p x \
        -k {tls_flag} --nicehash --coin monero -a rx/0 \
        --cpu-priority={cpu_prio} --huge-pages-jit --asm=auto \
        --randomx-cache-qos --randomx-1gb-pages --cpu-memory-pool=-1 \
        --argon2-impl=AVX2'
    else:
        xmrig_command = f'xmrig.exe -o stratum+{protocol}://randomxmonero.auto.nicehash.com:{mining_port} \
                -u {mining_address}.{worker_name} -p x \
                -k {tls_flag} --nicehash --coin monero -a rx/0 \
                --cpu-priority={cpu_prio} --asm=auto \
                --randomx-cache-qos --cpu-memory-pool=-1 \
                --argon2-impl=AVX2'
    os.system(xmrig_command)


def run_miniz(mining_alg, mining_address, worker_name, fan_speed, protocol, mining_port, powerlimit, gpuoffset, memoffset, memoffsetcommand, gpuoffsetcommand):
    if platform.system() == 'Linux':
         miniz_command = f'sudo ./miniZ --worker {worker_name} \
        --url {protocol}://{mining_address}.{worker_name}@{mining_alg}.auto.nicehash.com:{mining_port} \
        --oc1 --oc2 --ocX \
        --smart-pers --fanspeed={fan_speed} --mt-auto --ocXsamples=1000 \
        {gpuoffsetcommand}{gpuoffset} {memoffsetcommand}{memoffset} \
        --power={powerlimit} --dag-fix'
    else:
        miniz_command = f'miniZ.exe --worker {worker_name} \
             --url {protocol}://{mining_address}.{worker_name}@{mining_alg}.auto.nicehash.com:{mining_port} \
             --oc1 --oc2 --ocX \
             --smart-pers --fanspeed={fan_speed} --mt-auto --ocXsamples=1000 \
             {gpuoffsetcommand}{gpuoffset} {memoffsetcommand}{memoffset} \
             --power={powerlimit} --dag-fix'
    os.system(miniz_command)


def run_miner(mining_address, worker_name, use_cpu, use_gpu, tls_flag, memoffsetcommand, gpuoffsetcommand, cpu_prio, change_fan_speed, fan_speed, mining_alg, protocol, mining_port, powerlimit, gpuoffset, memoffset):
    if use_cpu.lower() == 'y':
        xmrig_process = multiprocessing.Process(
            target=run_xmrig, args=(mining_address, worker_name, cpu_prio, protocol, mining_port, tls_flag))
        xmrig_process.start()
    if use_gpu.lower() == 'y':
        miniz_process = multiprocessing.Process(
            target=run_miniz, args=(mining_alg, mining_address, worker_name, fan_speed, protocol, mining_port, powerlimit, gpuoffset, memoffset, memoffsetcommand, gpuoffsetcommand))
        miniz_process.start()
    if use_cpu.lower() == 'y':
        xmrig_process.join()
    if use_gpu.lower() == 'y':
        miniz_process.join()


if __name__ == "__main__":
    download_deps()
    mining_address, worker_name, use_cpu, use_gpu, tls_flag, cpu_prio, change_fan_speed, fan_speed, mining_alg, protocol, mining_port, powerlimit, gpuoffset, memoffset, memoffsetcommand, gpuoffsetcommand = load_from_config()
    if mining_address is None or worker_name is None or use_cpu is None or use_gpu is None or tls_flag is None or cpu_prio is None or change_fan_speed is None or fan_speed is None or mining_alg is None or protocol is None or mining_port is None or powerlimit is None or gpuoffset is None or memoffset is None:
        mining_address = input_mining_address()
        worker_name = input_worker_name()
        protocol = input("Select protocol: (tcp or ssl)").lower()
        if protocol == 'ssl':
            mining_port = 443
            tls_flag = '--tls'
        else:
            mining_port = 9200
        mining_alg = input(
            "Select GPU Mining Algo: (zelhash or kawpow or octopus) ").lower()
        use_cpu = input("Do you want to mine using CPU? (y/n): ")
        if use_cpu.lower() == 'y':
            cpu_prio = input("Enter cpu_priority for cpu mining: ")
        elif use_cpu.lower() == 'n':
            cpu_prio = 0
        use_gpu = input("Do you want to mine using GPU? (y/n): ")
        gpuoffset = input("Enter Gpu Clock Offset (Like +100): ")
        if gpuoffset != "0":
            gpuoffsetcommand = "--gpuoffset="
        else:
            gpuoffsetcommand = ""
        memoffset = input("Enter Gpu Memory Clock Offset (Like +200)")
        if memoffset != "0":
            memoffsetcommand = "--memoffset="
        else:
            memoffsetcommand = ""
        powerlimit = input("Enter Power Limit in Watts: ")
        change_fan_speed = input(
            "Do you want to change target fan speed for GPU? (Nvidia-Only, single gpu): (y/n)")
        if change_fan_speed.lower() == 'y':
            fan_speed = input("Set Target FAN Speed (GPU0): (%)")
        elif change_fan_speed.lower() == 'n':
            fan_speed = 35
        save_to_cfg = input(
            "Do you want to save current settings to config? (y/n): ").lower()
        if save_to_cfg == 'y':
            save_to_config(mining_address, worker_name, use_cpu, use_gpu, tls_flag,
                           cpu_prio, change_fan_speed, fan_speed, mining_alg, protocol, mining_port, powerlimit, gpuoffset, memoffset, memoffsetcommand, gpuoffsetcommand)
    run_miner(mining_address, worker_name, use_cpu, use_gpu, tls_flag, memoffsetcommand, gpuoffsetcommand,
              cpu_prio, change_fan_speed, fan_speed, mining_alg, protocol, mining_port, powerlimit, gpuoffset, memoffset)
