import ipaddress
import platform
import subprocess
import os
import datetime

warp_cidr = [
    '162.159.192.0/24',
    '162.159.193.0/24',
    '162.159.195.0/24',
    '162.159.204.0/24',
    '188.114.96.0/24',
    '188.114.97.0/24',
    '188.114.98.0/24',
    '188.114.99.0/24'
]

script_directory = os.path.dirname(__file__)
ip_txt_path = os.path.join(script_directory, 'ip.txt')
result_path = os.path.join(script_directory, 'result.csv')


def create_ips():
    c = 0
    total_ips = sum(len(list(ipaddress.IPv4Network(cidr))) for cidr in warp_cidr)

    with open(ip_txt_path, 'w') as file:
        for cidr in warp_cidr:
            ip_addresses = list(ipaddress.IPv4Network(cidr))
            for addr in ip_addresses:
                c += 1
                file.write(str(addr))
                if c != total_ips:
                    file.write('\n')


if os.path.isfile(ip_txt_path):
    print("ip.txt exists.")
else:
    print('Creating ip.txt File.')
    create_ips()
    print('ip.txt File Created Successfully!')


def arch_suffix():
    machine = platform.machine().lower()
    if machine.startswith('i386') or machine.startswith('i686'):
        return '386'
    elif machine.startswith(('x86_64', 'amd64')):
        return 'amd64'
    elif machine.startswith(('armv8', 'arm64', 'aarch64')):
        return 'arm64'
    elif machine.startswith('s390x'):
        return 's390x'
    else:
        raise ValueError("Unsupported CPU architecture")


arch = arch_suffix()

print("Fetch warp program...")
url = f"https://gitlab.com/Misaka-blog/warp-script/-/raw/main/files/warp-yxip/warp-linux-{arch}"

subprocess.run(["wget", url, "-O", "warp"])
os.chmod("warp", 0o755)
command = ["./warp", ">/dev/null", "2>&1"]
print("Scanning ips...")
process = subprocess.run(command, shell=False)
# Wait for the process to finish
if process.returncode != 0:
    print("Error: Warp execution failed.")
else:
    print("Warp executed successfully.")


def warp_ip():
    creation_time = os.path.getctime(result_path)
    formatted_time = datetime.datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M:%S")
    config_prefixes = ''
    with open(result_path, 'r') as csv_file:
        next(csv_file)
        ip1 = next(csv_file).split(',')[0]
        ip2 = next(csv_file).split(',')[0]
        ip3 = next(csv_file).split(',')[0]
        ip4 = next(csv_file).split(',')[0]
        config_prefix1 = f'{ip1}'
        config_prefix2 = f'{ip2}'
        config_prefix3 = f'{ip3}'
        config_prefix4 = f'{ip4}'
        config_prefixes += config_prefix1 + '\n' + config_prefix2 + '\n' + config_prefix3 + '\n' + config_prefix4
    return config_prefixes, formatted_time


configs = warp_ip()[0]
export_directory = os.path.join(script_directory, 'export')
os.makedirs(export_directory, exist_ok=True)
export_file_path = os.path.join(export_directory, 'warp-ip')
with open(export/warp-ip, 'w') as op:
    op.write(f"{configs}")

os.remove(ip_txt_path)
os.remove(result_path)
os.remove("warp")
