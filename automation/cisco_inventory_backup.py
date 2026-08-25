```python
"""
Automated Cisco IOS-XE Configuration Backup Engine
Uses Netmiko to pull running configurations across multi-vendor lab environments.
"""

import datetime
import os
from netmiko import ConnectHandler

# Sample Network Devices Inventory
DEVICES = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.1.1",
        "username": "admin",
        "password": "CiscoLabPassword123!",
        "secret": "EnablePassword123!",
    }
]

def backup_running_config(device: dict, output_dir: str = "backups") -> None:
    """Connects to Cisco device and exports show running-config."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    hostname = device["host"]

    print(f"[*] Connecting to Cisco Device: {hostname}...")
    try:
        connection = ConnectHandler(**device)
        connection.enable()
        
        print(f"[+] Fetching running-config from {hostname}...")
        config_data = connection.send_command("show running-config")
        
        filename = os.path.join(output_dir, f"{hostname}_config_{timestamp}.cfg")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(config_data)
            
        print(f"[+] Backup successfully saved to: {filename}")
        connection.disconnect()
    except Exception as error:
        print(f"[-] FAILED to backup {hostname}: {str(error)}")

if __name__ == "__main__":
    print("=== Cisco Network Automation - Backup Engine ===")
    for dev in DEVICES:
        backup_running_config(dev)
