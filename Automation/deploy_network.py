#!/usr/bin/env python3
"""
Enterprise VLAN & Security Automation
Uses Netmiko to configure switch and router via SSH.
Compatible with Cisco IOS, IOS-XE devices.
"""

from netmiko import ConnectHandler

# ========== DEVICE INVENTORY ==========
switch = {
    "device_type": "cisco_ios",
    "host": "192.168.1.2",
    "username": "admin",
    "password": "Netsec112211",
    "secret": "Netsec112211",
}

router = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "admin",
    "password": "Netsec112211",
    "secret": "Netsec112211",
}

# ========== SWITCH CONFIGURATION ==========
switch_config = """
hostname SW-ACCESS-01

vlan 10
 name HR
vlan 20
 name IT
vlan 30
 name Finance
vlan 40
 name Management

interface fastEthernet 0/1
 description HR-PC
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast

interface fastEthernet 0/2
 description IT-PC
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast

interface fastEthernet 0/3
 description FINANCE-PC
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast

interface fastEthernet 0/4
 description MANAGEMENT-PC
 switchport mode access
 switchport access vlan 40
 spanning-tree portfast

interface fastEthernet 0/5
 description TRUNK-TO-ISR4321
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40

! Security: shutdown unused ports
interface range fastEthernet 0/6 - 23
 description UNUSED-DISABLED
 shutdown

! Security: local user + password encryption
username admin privilege 15 secret Netsec112211
service password-encryption

banner motd #
UNAUTHORIZED ACCESS IS STRICTLY PROHIBITED.
ALL ACTIVITY IS MONITORED AND LOGGED.
#

end
"""

# ========== ROUTER CONFIGURATION ==========
router_config = """
hostname RT-BRANCH-01

interface gigabitEthernet 0/0/0
 description TRUNK-TO-SWITCH
 no shutdown

interface gigabitEthernet 0/0/0.10
 description HR-GATEWAY
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 ip access-group ACL-HR-IN in

interface gigabitEthernet 0/0/0.20
 description IT-GATEWAY
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
 ip access-group ACL-IT-IN in

interface gigabitEthernet 0/0/0.30
 description FINANCE-GATEWAY
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
 ip access-group ACL-FINANCE-IN in

interface gigabitEthernet 0/0/0.40
 description MANAGEMENT-GATEWAY
 encapsulation dot1Q 40
 ip address 192.168.40.1 255.255.255.0
 ip access-group ACL-MGMT-IN in

! Security ACLs
ip access-list extended ACL-HR-IN
 permit ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255
 permit ip 192.168.10.0 0.0.0.255 192.168.40.0 0.0.0.255
 deny ip 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255
 permit ip any any

ip access-list extended ACL-FINANCE-IN
 permit ip 192.168.30.0 0.0.0.255 192.168.20.0 0.0.0.255
 permit ip 192.168.30.0 0.0.0.255 192.168.40.0 0.0.0.255
 deny ip 192.168.30.0 0.0.0.255 192.168.10.0 0.0.0.255
 permit ip any any

ip access-list extended ACL-IT-IN
 permit ip 192.168.20.0 0.0.0.255 any

ip access-list extended ACL-MGMT-IN
 permit ip 192.168.40.0 0.0.0.255 any

! SSH Security
ip domain-name enterprise.local
crypto key generate rsa 1024

username admin privilege 15 secret Netsec112211

line vty 0 15
 login local
 transport input ssh

enable secret Netsec112211
service password-encryption

banner motd #
UNAUTHORIZED ACCESS IS STRICTLY PROHIBITED.
ALL ACTIVITY IS MONITORED AND LOGGED.
#

end
"""

def deploy_config(device, config, device_name):
    print(f"\n{'='*50}")
    print(f"Connecting to {device_name} ({device['host']})...")
    print(f"{'='*50}")

    conn = ConnectHandler(**device)
    conn.enable()

    print(f"Sending configuration to {device_name}...")
    output = conn.send_config_set(config.split("\n"))

    print(f"Saving configuration on {device_name}...")
    conn.save_config()

    print(f"\n{device_name} configured successfully!")
    conn.disconnect()
    return output

if __name__ == "__main__":
    print("Enterprise VLAN & Security Deployment Script")
    print("This script automates the entire Router-on-a-Stick + ACL + SSH build")

    deploy_config(switch, switch_config, "SW-ACCESS-01")
    deploy_config(router, router_config, "RT-BRANCH-01")

    print("\n" + "="*50)
    print("DEPLOYMENT COMPLETE")
    print("="*50)
    print("Next steps: Verify with ping tests and 'show' commands.")
