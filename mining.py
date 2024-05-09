import os
import configparser
import platform
import subprocess
import shutil
import multiprocessing

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
        mining_address = config['MINER'].get('MiningAddress')
        worker_name = config['MINER'].get('WorkerName')
        return mining_address, worker_name
    else:
        return None, None


def save_to_config(mining_address, worker_name):
    config = configparser.ConfigParser()
    config['MINER'] = {'MiningAddress': mining_address,
                       'WorkerName': worker_name}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def download_deps():
    if platform.system() == 'Linux':
        if platform.release() == 'arch':
            if shutil.which('xmrig') is None:
                subprocess.run(['sudo', 'pacman', '-Sy', 'xmrig'])
            elif shutil.which('miner') is None:
                subprocess.run(['yay', '-Sy', 'gminer-bin'])


def run_xmrig(mining_address, worker_name, cpu_prio):
    xmrig_command = f'xmrig -o stratum+ssl://randomxmonero.auto.nicehash.com:443 \
    -u {mining_address}.{worker_name} -p x \
    --tls -k --nicehash --coin monero -a rx/0 \
    --cpu-priority={cpu_prio} --huge-pages-jit --asm=auto \
    --randomx-cache-qos --randomx-1gb-pages'
    os.system(xmrig_command)


def run_gminer(mining_address, worker_name):
    gminer_command = f'miner --algo kawpow --server stratum+ssl://kawpow.auto.nicehash.com:443 --user {
        mining_address}.{worker_name} -p x'
    os.system(gminer_command)


def run_miner(mining_address, worker_name, use_cpu, use_gpu, cpu_prio, change_fan_speed, fan_speed):
    if change_fan_speed.lower() == 'yes':
        unlock_fan_control_command = "nvidia-settings -a [gpu:0]/GPUFanControlState=1"
        subprocess.run(['sudo', f'{unlock_fan_control_command}'])
        fan0_speed_command = f"nvidia-settings -a [fan:0]/GPUTargetFanSpeed={
            fan_speed}"
        subprocess.run(['sudo', f'{fan0_speed_command}'])
        fan1_speed_command = f"nvidia-settings -a [fan:1]/GPUTargetFanSpeed={
            fan_speed}"
        subprocess.run(['sudo', f'{fan1_speed_command}'])
    if use_cpu.lower() == 'yes':
        xmrig_process = multiprocessing.Process(
            target=run_xmrig, args=(mining_address, worker_name, cpu_prio))
        xmrig_process.start()
    if use_gpu.lower() == 'yes':
        gminer_process = multiprocessing.Process(
            target=run_gminer, args=(mining_address, worker_name))
        gminer_process.start()

    if use_cpu.lower() == 'yes':
        xmrig_process.join()
    if use_gpu.lower() == 'yes':
        gminer_process.join()


if __name__ == "__main__":
    mining_address, worker_name = load_from_config()
    if mining_address is None or worker_name is None:
        mining_address = input_mining_address()
        worker_name = input_worker_name()
        save_to_config(mining_address, worker_name)

    use_cpu = input("Do you want to mine using CPU? (yes/no): ")
    cpu_prio = input("Enter cpu_priority for cpu mining: ")
    use_gpu = input("Do you want to mine using GPU? (yes/no): ")
    change_fan_speed = input(
        "Do you want to change target fan speed for GPU? (Nvidia-Only, single gpu) :")
    if change_fan_speed.lower() == 'yes':
        fan_speed = input("Set Target FAN Speed (GPU0): ")

    download_deps()
    run_miner(mining_address, worker_name, use_cpu, use_gpu,
              cpu_prio, change_fan_speed, fan_speed)
