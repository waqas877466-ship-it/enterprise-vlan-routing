
# Enterprise VLAN Segmentation & Inter-VLAN Routing

## Project Overview

Designed and implemented a **multi-department enterprise network** using Cisco VLAN segmentation and Router-on-a-Stick inter-VLAN routing. This project demonstrates core CCNA-level skills in Layer 2 switching, Layer 3 routing, 802.1Q trunking, IP subnetting, and extends into **enterprise security hardening** and **network automation** (NetDevOps).

**Technologies:** Cisco IOS, VLANs, 802.1Q Trunking, Router Sub-interfaces, IP Subnetting, Extended ACLs, SSH Hardening, Network Automation (Python/Netmiko, Ansible)

**Platform:** Cisco Packet Tracer (Manual Lab) + Real-World Automation Code

**Design Pattern:** Router-on-a-Stick with Security Hardening

---

## Network Architecture

### Topology

```
                    [ISR4321 Router]
                         |
                         | Gig0/0/0 (Trunk - 802.1Q)
                         |
              [2960-24TT Switch]
             /    |    |    \
           Fa0/1 Fa0/2 Fa0/3 Fa0/4
            |      |      |      |
          [HR]   [IT]  [Finance][Mgmt]
```

### Devices Used

| Device | Model | Role |
|--------|-------|------|
| Router | Cisco ISR4321 | Layer 3 routing + ACL enforcement |
| Switch | Cisco Catalyst 2960-24TT | Layer 2 VLAN segmentation |
| End Devices | 4x PC-PT | Department workstations |

### Cabling

| Connection | Cable Type | Ports |
|------------|-----------|-------|
| Router ↔ Switch | Copper Straight-Through | Gig0/0/0 ↔ Fa0/5 |
| HR PC ↔ Switch | Copper Straight-Through | Fa0 ↔ Fa0/1 |
| IT PC ↔ Switch | Copper Straight-Through | Fa0 ↔ Fa0/2 |
| Finance PC ↔ Switch | Copper Straight-Through | Fa0 ↔ Fa0/3 |
| Management PC ↔ Switch | Copper Straight-Through | Fa0 ↔ Fa0/4 |

---

## IP Addressing & VLAN Scheme

| VLAN ID | Department | Network | Gateway (Router) | PC IP | Subnet Mask |
|---------|-----------|---------|------------------|-------|-------------|
| 10 | HR | 192.168.10.0/24 | 192.168.10.1 | 192.168.10.10 | 255.255.255.0 |
| 20 | IT | 192.168.20.0/24 | 192.168.20.1 | 192.168.20.20 | 255.255.255.0 |
| 30 | Finance | 192.168.30.0/24 | 192.168.30.1 | 192.168.30.30 | 255.255.255.0 |
| 40 | Management | 192.168.40.0/24 | 192.168.40.1 | 192.168.40.40 | 255.255.255.0 |

---

## Configuration

### 1. Switch Configuration (Catalyst 2960-24TT)

```cisco
enable
configure terminal
hostname SW-ACCESS-01

! Create VLANs
vlan 10
 name HR
 exit
vlan 20
 name IT
 exit
vlan 30
 name Finance
 exit
vlan 40
 name Management
 exit

! HR Department - Access Port
interface fastEthernet 0/1
 description HR-PC
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 exit

! IT Department - Access Port
interface fastEthernet 0/2
 description IT-PC
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 exit

! Finance Department - Access Port
interface fastEthernet 0/3
 description FINANCE-PC
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
 exit

! Management Department - Access Port
interface fastEthernet 0/4
 description MANAGEMENT-PC
 switchport mode access
 switchport access vlan 40
 spanning-tree portfast
 exit

! Router Uplink - 802.1Q Trunk Port
interface fastEthernet 0/5
 description TRUNK-TO-ISR4321
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40
 exit

! Security: Shutdown unused ports
interface range fastEthernet 0/6 - 23
 description UNUSED-DISABLED
 shutdown
 exit

! Security: Local user + password encryption
username admin privilege 15 secret Netsec112211
service password-encryption

! Security: MOTD Banner
banner motd #
UNAUTHORIZED ACCESS IS STRICTLY PROHIBITED.
ALL ACTIVITY IS MONITORED AND LOGGED.
#

! Save configuration
end
write memory
```

### 2. Router Configuration (ISR4321)

```cisco
enable
configure terminal
hostname RT-BRANCH-01

! Physical interface - enable only, no IP assigned
interface gigabitEthernet 0/0/0
 description TRUNK-TO-SWITCH
 no shutdown
 exit

! Sub-interface for VLAN 10 (HR Gateway)
interface gigabitEthernet 0/0/0.10
 description HR-GATEWAY
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 ip access-group ACL-HR-IN in
 exit

! Sub-interface for VLAN 20 (IT Gateway)
interface gigabitEthernet 0/0/0.20
 description IT-GATEWAY
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
 ip access-group ACL-IT-IN in
 exit

! Sub-interface for VLAN 30 (Finance Gateway)
interface gigabitEthernet 0/0/0.30
 description FINANCE-GATEWAY
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
 ip access-group ACL-FINANCE-IN in
 exit

! Sub-interface for VLAN 40 (Management Gateway)
interface gigabitEthernet 0/0/0.40
 description MANAGEMENT-GATEWAY
 encapsulation dot1Q 40
 ip address 192.168.40.1 255.255.255.0
 ip access-group ACL-MGMT-IN in
 exit

! Security: Extended ACLs
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

! Security: SSH Hardening
ip domain-name enterprise.local
crypto key generate rsa
! Type 1024 when prompted for modulus size

username admin privilege 15 secret Netsec112211

line vty 0 15
 login local
 transport input ssh
 exit

! Security: Enable secret + encryption
enable secret Netsec112211
service password-encryption

! Security: MOTD Banner
banner motd #
UNAUTHORIZED ACCESS IS STRICTLY PROHIBITED.
ALL ACTIVITY IS MONITORED AND LOGGED.
#

! Save configuration
end
write memory
```

### 3. PC Configuration (Static IP)

| PC | IP Address | Subnet Mask | Default Gateway |
|----|-----------|-------------|-----------------|
| **HR** | 192.168.10.10 | 255.255.255.0 | 192.168.10.1 |
| **IT** | 192.168.20.20 | 255.255.255.0 | 192.168.20.1 |
| **Finance** | 192.168.30.30 | 255.255.255.0 | 192.168.30.1 |
| **Management** | 192.168.40.40 | 255.255.255.0 | 192.168.40.1 |

---

## Security Hardening

### Inter-VLAN Access Control (ACLs)

Implemented **extended ACLs** on router sub-interfaces to enforce department-level security policies. This is how real enterprises protect sensitive data:

| Rule | Source | Destination | Action | Business Reason |
|------|--------|-------------|--------|-----------------|
| 1 | HR (VLAN 10) | IT (VLAN 20) | ✅ PERMIT | Collaboration & support |
| 2 | HR (VLAN 10) | Management (VLAN 40) | ✅ PERMIT | Reporting chain |
| 3 | HR (VLAN 10) | Finance (VLAN 30) | ❌ **DENY** | Protect financial data |
| 4 | Finance (VLAN 30) | IT (VLAN 20) | ✅ PERMIT | Collaboration & support |
| 5 | Finance (VLAN 30) | Management (VLAN 40) | ✅ PERMIT | Oversight & audit |
| 6 | Finance (VLAN 30) | HR (VLAN 10) | ❌ **DENY** | Protect payroll data |
| 7 | IT (VLAN 20) | ANY | ✅ PERMIT | Full admin access |
| 8 | Management (VLAN 40) | ANY | ✅ PERMIT | Oversight role |

> **Real-world analogy:** Think of ACLs as keycard access rules. HR employees can swipe into IT and Management, but their card gets **rejected** at the Finance vault door.

### Verification: ACL Enforcement in Action

**From HR PC:**
```cmd
C:\>ping 192.168.20.20     ! ✅ SUCCESS - IT is allowed
C:\>ping 192.168.40.40     ! ✅ SUCCESS - Management is allowed
C:\>ping 192.168.30.30     ! ❌ REQUEST TIMED OUT - Finance is BLOCKED
```

**From Finance PC:**
```cmd
C:\>ping 192.168.10.10     ! ❌ REQUEST TIMED OUT - HR is BLOCKED
```

The **failed pings prove the ACLs are actively enforced** by the router. This is not just theory — it's a live security policy.

### Remote Management Security (SSH)

| Feature | Implementation | Why It Matters |
|---------|---------------|--------------|
| **SSH vs Telnet** | `transport input ssh` on VTY lines | Telnet sends passwords in plain text; SSH encrypts everything |
| **RSA Key** | `crypto key generate rsa` | Generates encryption keys for SSH handshake |
| **Local User Auth** | `username admin privilege 15 secret` | Prevents anonymous logins; requires named credentials |
| **Enable Secret** | `enable secret Netsec112211` | Protects privileged EXEC mode with encrypted password |
| **Password Encryption** | `service password-encryption` | Encrypts all passwords in the running config file |
| **MOTD Banner** | Legal warning on login | Deters attackers; required for compliance (SOX, PCI-DSS) |

### Port Security (Physical Layer)

All unused switch ports are **administratively shutdown**:
```cisco
interface range fastEthernet 0/6 - 23
 shutdown
```

> **Why:** An attacker who walks into your office and plugs into an empty port gets **zero access**. The port is dead.

---

## Network Automation (DevOps/NetDevOps)

This project includes **production-ready automation scripts** that deploy the entire topology + security on real Cisco hardware via SSH.

> **Note:** Packet Tracer does not support external SSH automation tools. These scripts are designed for physical Cisco devices or GNS3/EVE-NG labs with real IOS images.

### Option A: Python + Netmiko

**File:** `automation/deploy_network.py`

A Python script using the **Netmiko** library to SSH into the switch and router, push the full configuration (VLANs, trunk, ACLs, security), and save to NVRAM.

**Usage:**
```bash
pip install -r requirements.txt
python deploy_network.py
```

**What it does:**
1. SSHs into `SW-ACCESS-01` and `RT-BRANCH-01`
2. Pushes the complete switch config (VLANs, access ports, trunk, port shutdown)
3. Pushes the complete router config (sub-interfaces, ACLs, SSH hardening)
4. Saves both configurations
5. Prints success confirmation

### Option B: Ansible Playbook

**Files:**
- `automation/deploy_network.yml` — Main playbook
- `automation/inventory.ini` — Device inventory

An **Ansible playbook** using the `ios_config` and `ios_banner` modules for idempotent configuration management.

**Usage:**
```bash
ansible-playbook -i inventory.ini deploy_network.yml
```

**What it does:**
- Uses conditionals (`when: inventory_hostname == "router"`) to apply router-only vs switch-only tasks
- Loops through VLAN/access-port definitions for clean, scalable code
- Enforces configuration state (if you run it twice, it won't duplicate — it's idempotent)

### Why Automation Matters

| Manual Configuration | Automated Deployment |
|---------------------|----------------------|
| 30+ minutes per device | 30 seconds per device |
| Typos and inconsistencies | Standardized, version-controlled configs |
| No rollback capability | Git history + config backups |
| Not scalable | Deploy to 100 switches with one command |
| Hard to audit | Every change is logged and reviewable |

> **DevOps Mindset:** "If you have to SSH into a device more than once, you should have automated it the first time."

---

## Troubleshooting Journey: Problems Faced & Fixes

This section documents every real-world issue encountered during the build and how each was resolved.

### Problem 1: Incorrect Router Cabling (Two Cables Instead of One)

**Symptom:** Router had two physical cables (Gig0/0/0 and Gig0/1) connected to the switch.  
**Root Cause:** Misunderstanding of the Router-on-a-Stick design. The entire point is to use **one physical interface** sliced into multiple logical sub-interfaces via 802.1Q tagging.  
**Fix:** Removed the second cable. Connected only **Gig0/0/0 ↔ Fa0/5** as the single trunk link.

> **Lesson:** Router-on-a-Stick uses one physical cable carrying all VLANs via 802.1Q tags. The router creates virtual sub-interfaces (Gig0/0/0.10, .20, .30, .40) — not additional physical cables.

---

### Problem 2: Router-to-Switch Link Stayed RED (Administratively Down)

**Symptom:** Cable between router and switch showed a red link light.  
**Root Cause:** Cisco router interfaces are **shutdown by default** when placed in Packet Tracer. The switch port was fine; the router interface was administratively disabled.  
**Fix:**
```cisco
interface gigabitEthernet 0/0/0
no shutdown
```
**Result:** Link light turned green within seconds.

> **Lesson:** Always remember `no shutdown` on router physical interfaces. Switches auto-enable ports; routers do not.

---

### Problem 3: PortFast Warning Message

**Symptom:** After typing `spanning-tree portfast`, the switch displayed a long warning about bridging loops.  
**Root Cause:** This is Cisco's standard safety disclaimer. It warns against using PortFast on trunk or multi-device ports.  
**Fix:** **No action needed.** Since Fa0/1–4 are connected to single PCs, PortFast is correct. The warning is informational.

> **Lesson:** PortFast is mandatory on access ports connected to end-hosts. It bypasses the 30-second STP listening/learning phase. The warning is normal.

---

### Problem 4: Typo in Verification Command

**Symptom:**
```
SW-Access_01#shwo int trunk
% Invalid input detected at '^' marker.
```
**Root Cause:** Typo (`shwo` instead of `show`).  
**Fix:** Retyped the correct command: `show interfaces trunk`

> **Lesson:** Cisco CLI has no autocorrect. Common shorthand `sh int trunk` also works.

---

### Problem 5: Finance PC Port Left in Default VLAN (VLAN 1)

**Symptom:** `show vlan brief` showed Fa0/3 under **VLAN 1** instead of VLAN 30. VLAN 30 appeared with **no ports assigned**.

**Root Cause:** The configuration for Fa0/3 was skipped during initial setup.  
**Fix:** Re-entered the access port configuration for Fa0/3.

> **Lesson:** Always verify with `show vlan brief` after configuring access ports. One missed port breaks entire VLAN connectivity.

---

### Problem 6: `switchport nonegotiate` Not Supported

**Symptom:** The command `switchport nonegotiate` was not available on the Packet Tracer 2960-24TT model.  
**Root Cause:** Packet Tracer's simulated IOS does not include DTP disable options.  
**Fix:** Removed the command. The trunk works correctly without it in this simulation.

> **Lesson:** In production, `switchport nonegotiate` is a security best practice to prevent VLAN hopping attacks. On real hardware (Catalyst 9200/9300), always include it.

---

### Problem 7: Router Lockout After Setting Enable Secret

**Symptom:** After typing `enable secret Netsec112211`, the router rejected the password on subsequent login attempts (`% Bad secrets`).  
**Root Cause:** The `enable secret` command hashes the password with MD5. A typo during entry creates a hash mismatch — permanent lockout since you cannot see what was actually typed.  
**Fix:** Used Packet Tracer's **Config tab** → found "Enable Secret" field → cleared it → re-entered `Netsec112211` correctly. Alternative: power-cycled the router to reset.

> **Lesson:** When setting passwords in production, type them in a text editor first, then copy-paste. One wrong character = lockout. Always verify with `show running-config | include secret` immediately after.

---

## Verification & Proof of Work

### Switch Verification

```cisco
SW-Access_01#show vlan brief

VLAN Name              Status    Ports
---- ---------------- --------- -------------------------------
1    default            active    Fa0/6, Fa0/7, Fa0/8 ...
10   HR                 active    Fa0/1
20   IT                 active    Fa0/2
30   Finance            active    Fa0/3
40   Management         active    Fa0/4
```

```cisco
SW-Access_01#show interfaces trunk

Port        Mode         Encapsulation  Status        Native vlan
Fa0/5       on           802.1q         trunking      1

Port        Vlan allowed on trunk
Fa0/5       10,20,30,40
```

### Router Verification

```cisco
RT-BRANCH-01#show ip interface brief

Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0/0   unassigned      YES unset  up                    up
GigabitEthernet0/0/0.10 192.168.10.1  YES manual up                    up
GigabitEthernet0/0/0.20 192.168.20.1  YES manual up                    up
GigabitEthernet0/0/0.30 192.168.30.1  YES manual up                    up
GigabitEthernet0/0/0.40 192.168.40.1  YES manual up                    up
```

```cisco
RT-BRANCH-01#show ip route

C    192.168.10.0/24 is directly connected, GigabitEthernet0/0/0.10
C    192.168.20.0/24 is directly connected, GigabitEthernet0/0/0.20
C    192.168.30.0/24 is directly connected, GigabitEthernet0/0/0.30
C    192.168.40.0/24 is directly connected, GigabitEthernet0/0/0.40
```

### ACL Verification

```cisco
RT-BRANCH-01#show ip access-lists

Extended IP access list ACL-HR-IN
    10 permit ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255
    20 permit ip 192.168.10.0 0.0.0.255 192.168.40.0 0.0.0.255
    30 deny ip 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255
    40 permit ip any any

Extended IP access list ACL-FINANCE-IN
    10 permit ip 192.168.30.0 0.0.0.255 192.168.20.0 0.0.0.255
    20 permit ip 192.168.30.0 0.0.0.255 192.168.40.0 0.0.0.255
    30 deny ip 192.168.30.0 0.0.0.255 192.168.10.0 0.0.0.255
    40 permit ip any any
```

### SSH Verification

```cisco
RT-BRANCH-01#show ip ssh

SSH Enabled - version 1.99
Authentication timeout: 120 secs; Authentication retries: 3
```

### End-to-End Connectivity Test (HR PC)

```cmd
C:\>ping 192.168.20.20
Reply from 192.168.20.20: bytes=32 time<1ms TTL=127
Reply from 192.168.20.20: bytes=32 time<1ms TTL=127
Reply from 192.168.20.20: bytes=32 time<1ms TTL=127
Reply from 192.168.20.20: bytes=32 time<1ms TTL=127

C:\>ping 192.168.30.30
Request timed out.
Request timed out.
Request timed out.
Request timed out.
```

**Analysis:** The `ping 192.168.30.30` fails because the router's ACL **actively drops** HR-to-Finance traffic. This proves the security policy is enforced.

### Path Trace (HR → Management)

```cmd
C:\>tracert 192.168.40.40

Tracing route to 192.168.40.40 over a maximum of 30 hops:

  1   <1 ms   <1 ms   <1 ms   192.168.10.1
  2   <1 ms   <1 ms   <1 ms   192.168.40.1
  3   <1 ms   <1 ms   <1 ms   192.168.40.40

Trace complete.
```

---

## Real-World Context

### Where This Design Is Used

The **Router-on-a-Stick** pattern is deployed in:
- Small branch offices (under 50 users)
- Remote sites with a single L2 access switch
- Lab environments and CCNA training
- Budget-conscious networks before upgrading to Layer-3 switches

### Production Evolution

In enterprise campus networks, this role is handled by **Layer-3 switches** (e.g., Cisco Catalyst 9300, Aruba CX 6300, Juniper EX4400) to achieve wire-speed routing without a router bottleneck. However, the concepts learned here — VLANs, 802.1Q trunking, gateway IPs, ACLs, SSH hardening, and inter-VLAN routing — are **universal** across every vendor and platform.

### Security in Enterprise Networks

Real enterprises layer multiple security controls:

| Layer | Control | This Project |
|-------|---------|------------|
| **Physical** | Locked server rooms, badge access | Port shutdown on unused interfaces |
| **Network** | VLANs, ACLs, private VLANs | ✅ VLANs + Extended ACLs |
| **Endpoint** | 802.1X port authentication, NAC | (Next step: dot1x) |
| **Remote Access** | SSH, VPN, jump servers | ✅ SSH-only, encrypted passwords |
| **Monitoring** | Syslog, SNMP traps, SIEM | (Next step: logging host) |

---

## Key Takeaways

1. **VLANs isolate broadcast domains** — HR traffic does not flood into IT unless explicitly routed.
2. **802.1Q trunking** allows a single physical link to carry multiple VLANs using 4-byte tags.
3. **Router sub-interfaces** (`interface g0/0/0.10`) create logical gateways for each VLAN without requiring separate physical cables.
4. **Extended ACLs** enforce security policies at the network edge — controlling which departments can communicate.
5. **SSH replaces Telnet** for encrypted remote management; RSA keys, local users, and banners are mandatory.
6. **Unused ports should always be shutdown** — physical security is network security.
7. **Automation eliminates human error** — Python/Netmiko and Ansible turn 30 minutes of CLI typing into 30 seconds of code execution.
8. **Verification is non-negotiable** — `show vlan brief`, `show ip route`, `show ip access-lists`, and `ping` are your best friends.
9. **Documentation matters** — Every troubleshooting step teaches something. Writing it down turns a lab into a portfolio piece.

---

## File Structure

```
enterprise-vlan-routing/
├── README.md                          # This file
├── topology.png                       # Packet Tracer screenshot
├── configs/
│   ├── switch-config.txt              # 2960 running-config
│   └── router-config.txt              # ISR4321 running-config
├── verification/
│   ├── show-vlan-brief.png
│   ├── show-ip-route.png
│   ├── acl-ping-test.png              # HR blocked from Finance
│   ├── show-ip-ssh.png                # SSH enabled
│   └── tracert-output.png
└── automation/                        # NetDevOps / Infrastructure as Code
    ├── deploy_network.py              # Python + Netmiko script
    ├── deploy_network.yml             # Ansible playbook
    ├── inventory.ini                  # Ansible device inventory
    └── requirements.txt               # Python dependencies
```

---

## Author

Built from scratch in **Cisco Packet Tracer** as a foundational networking project, then extended with **security hardening** and **automation code** for real-world deployment scenarios.

*"Manual builds prove you understand the technology. Automation proves you understand scale."*

---

## License

This project is open for educational and portfolio use.
