import os
import configparser
import platform
import subprocess
import shutil
import multiprocessing
import atexit

CONFIG_FILE = 'config.ini'


def exit_handler():
    revert_fan_speed = input('Do you want to restore fan speed?: (y/n)')
    if revert_fan_speed.lower() == 'y':
        lock_fan_control_command = "nvidia-settings -a [gpu:0]/GPUFanControlState=0"
        os.system(lock_fan_control_command)
    else:
        exit(1)


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
            config['MINER'].get('mining_port')
        )
    else:
        return None, None, None, None, None, None, None, None, None, None, None


def save_to_config(mining_address, worker_name, use_cpu, use_gpu, tls_flag, cpu_prio, change_fan_speed, fan_speed, mining_alg, protocol, mining_port):
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
        'mining_port': mining_port
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
    shutil.rmtree('xmrig-6.21.3')
    os.remove('miniZ.sha256sum')
    os.remove('SHA256SUMS')
    os.remove('xmrig-6.21.3-linux-static-x64.tar.gz')
    os.remove('xmrig-6.21.3-linux-static-x64.tar')
    os.remove('miniz.tar.gz')
    os.remove('miniz.tar')


def run_xmrig(mining_address, worker_name, cpu_prio, protocol, mining_port, tls_flag):
    xmrig_command = f'sudo ./xmrig -o stratum+{protocol}://randomxmonero.auto.nicehash.com:{mining_port} \
    -u {mining_address}.{worker_name} -p x \
    -k {tls_flag} --nicehash --coin monero -a rx/0 \
    --cpu-priority={cpu_prio} --huge-pages-jit --asm=auto \
    --randomx-cache-qos --randomx-1gb-pages'
    os.system(xmrig_command)


def run_miniz(mining_alg, mining_address, worker_name, fan_speed, protocol, mining_port):
    miniz_command = f'sudo ./miniZ --worker worker --url {protocol}://{
        mining_address}.{worker_name}@{mining_alg}.auto.nicehash.com:{mining_port} --oc1 --smart-pers --fanspeed={fan_speed} --mt-auto'
    os.system(miniz_command)


def run_miner(mining_address, worker_name, use_cpu, use_gpu, tls_flag, cpu_prio, change_fan_speed, fan_speed, mining_alg, protocol, mining_port):
    if change_fan_speed.lower() == 'y':
        unlock_fan_control_command = "nvidia-settings -a [gpu:0]/GPUFanControlState=1"
        os.system(unlock_fan_control_command)
        fan0_speed_command = f"nvidia-settings -a [fan:0]/GPUTargetFanSpeed={
            fan_speed}"
        os.system(fan0_speed_command)
        fan1_speed_command = f"nvidia-settings -a [fan:1]/GPUTargetFanSpeed={
            fan_speed}"
        os.system(fan1_speed_command)
    if use_cpu.lower() == 'y':
        xmrig_process = multiprocessing.Process(
            target=run_xmrig, args=(mining_address, worker_name, cpu_prio, protocol, mining_port, tls_flag))
        xmrig_process.start()
    if use_gpu.lower() == 'y':
        miniz_process = multiprocessing.Process(
            target=run_miniz, args=(mining_alg, mining_address, worker_name, fan_speed, protocol, mining_port))
        miniz_process.start()

    if use_cpu.lower() == 'y':
        xmrig_process.join()
    if use_gpu.lower() == 'y':
        miniz_process.join()


if __name__ == "__main__":
    download_deps()
    atexit.register(exit_handler)
    mining_address, worker_name, use_cpu, use_gpu, tls_flag, cpu_prio, change_fan_speed, fan_speed, mining_alg, protocol, mining_port = load_from_config()
    if mining_address is None or worker_name is None or use_cpu is None or use_gpu is None or tls_flag is None or cpu_prio is None or change_fan_speed is None or fan_speed is None or mining_alg is None or protocol is None or mining_port is None:
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
                           cpu_prio, change_fan_speed, fan_speed, mining_alg, protocol, mining_port)
    run_miner(mining_address, worker_name, use_cpu, use_gpu, tls_flag,
              cpu_prio, change_fan_speed, fan_speed, mining_alg, protocol, mining_port)
