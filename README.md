# 🌐 Static Routing Network — Cisco Packet Tracer

<div align="center">

![Cisco](https://img.shields.io/badge/Cisco-Packet%20Tracer-1BA0D7?style=for-the-badge&logo=cisco&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)
![Networking](https://img.shields.io/badge/Topic-Static%20Routing-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A multi-router static routing implementation connecting three LAN segments via serial WAN links — built entirely in Cisco Packet Tracer.**

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Network Topology](#-network-topology)
- [Devices Used](#-devices-used)
- [IP Addressing Table](#-ip-addressing-table)
- [Router Configurations](#%EF%B8%8F-router-configurations)
- [Static Routes Explained](#-static-routes-explained)
- [Testing & Verification](#-testing--verification)
- [How to Run](#-how-to-run)
- [Key Learnings](#-key-learnings)
- [Author](#-author)

---

## 📌 Overview

This project demonstrates the fundamentals of **static routing** across a three-router network topology built in **Cisco Packet Tracer**. Each router manages a dedicated LAN segment, and all inter-network communication is achieved through **manually configured static routes** — without the use of any dynamic routing protocols such as OSPF or RIP.

The project simulates a real-world scenario where a network administrator must plan, configure, and verify connectivity between three geographically separated office networks connected over WAN serial links.

### ✨ Key Highlights

- 3 Cisco routers connected via **Serial WAN links** (/30 subnets)
- 3 separate **LAN segments** (/24 subnets) each with a dedicated switch and end hosts
- **6 PCs** (PC0–PC5) successfully communicating across all networks
- All routes manually configured — no dynamic routing protocols used
- Full **end-to-end connectivity** verified through ping tests

---

## 🗺️ Network Topology

> *Screenshot of the completed topology in Cisco Packet Tracer*

![Network Topology](screenshots/topology.png)

```
                    [10.0.0.0/30 WAN]           [11.0.0.0/30 WAN]
                    Se0/0 ←————————→ Se0/0   Se0/1 ←————————→ Se0/1
  [LAN 192.168.10.0/24]            [LAN 192.168.20.0/24]           [LAN 192.168.30.0/24]
         |                                  |                                |
      Router0 ————————————————————————— Router1 ————————————————————————— Router2
         |                                  |                                |
      Switch0                            Switch1                          Switch2
      /     \                            /     \                          /     \
    PC0     PC1                        PC2     PC3                      PC4     PC5
```

---

## 🖥️ Devices Used

| Device   | Model         | Quantity | Role                          |
|----------|---------------|----------|-------------------------------|
| Router0  | Cisco 2621XM  | 1        | Left Gateway (LAN 10.x)       |
| Router1  | Cisco 2621XM  | 1        | Central Hub Router            |
| Router2  | Cisco 2621XM  | 1        | Right Gateway (LAN 30.x)      |
| Switch0  | Cisco 2950-24 | 1        | LAN Switch — Left Segment     |
| Switch1  | Cisco 2950-24 | 1        | LAN Switch — Middle Segment   |
| Switch2  | Cisco 2950-24 | 1        | LAN Switch — Right Segment    |
| PC0–PC5  | PC-PT         | 6        | End Hosts (2 per LAN)         |

---

## 📊 IP Addressing Table

| Device   | Interface | IP Address    | Subnet Mask       | Network            | Role             |
|----------|-----------|---------------|-------------------|--------------------|------------------|
| Router0  | Fa0/0     | 192.168.10.1  | 255.255.255.0     | 192.168.10.0/24    | LAN Gateway      |
| Router0  | Se0/0     | 10.0.0.1      | 255.255.255.252   | 10.0.0.0/30        | WAN Link to R1   |
| Router1  | Se0/0     | 10.0.0.2      | 255.255.255.252   | 10.0.0.0/30        | WAN Link to R0   |
| Router1  | Se0/1     | 11.0.0.1      | 255.255.255.252   | 11.0.0.0/30        | WAN Link to R2   |
| Router1  | Fa0/0     | 192.168.20.1  | 255.255.255.0     | 192.168.20.0/24    | LAN Gateway      |
| Router2  | Se0/1     | 11.0.0.2      | 255.255.255.252   | 11.0.0.0/30        | WAN Link to R1   |
| Router2  | Fa0/0     | 192.168.30.1  | 255.255.255.0     | 192.168.30.0/24    | LAN Gateway      |
| Switch0  | VLAN 1    | 192.168.10.10 | 255.255.255.0     | 192.168.10.0/24    | Management IP    |
| Switch1  | VLAN 1    | 192.168.20.20 | 255.255.255.0     | 192.168.20.0/24    | Management IP    |
| Switch2  | VLAN 1    | 192.168.30.30 | 255.255.255.0     | 192.168.30.0/24    | Management IP    |
| PC0      | Fa0       | 192.168.10.2  | 255.255.255.0     | 192.168.10.0/24    | End Host         |
| PC1      | Fa0       | 192.168.10.3  | 255.255.255.0     | 192.168.10.0/24    | End Host         |
| PC2      | Fa0       | 192.168.20.2  | 255.255.255.0     | 192.168.20.0/24    | End Host         |
| PC3      | Fa0       | 192.168.20.3  | 255.255.255.0     | 192.168.20.0/24    | End Host         |
| PC4      | Fa0       | 192.168.30.2  | 255.255.255.0     | 192.168.30.0/24    | End Host         |
| PC5      | Fa0       | 192.168.30.3  | 255.255.255.0     | 192.168.30.0/24    | End Host         |

> **Note:** /30 subnets are used on WAN serial links to conserve IP address space — they only allow 2 usable host addresses, which is exactly what a point-to-point link requires.

---

## ⚙️ Router Configurations

### 🔷 Router0 — Left Gateway

```bash
Router> enable
Router# configure terminal
Router(config)# hostname Router0

! --- LAN Interface ---
Router0(config)# interface FastEthernet0/0
Router0(config-if)# ip address 192.168.10.1 255.255.255.0
Router0(config-if)# no shutdown

! --- WAN Interface ---
Router0(config)# interface Serial0/0
Router0(config-if)# ip address 10.0.0.1 255.255.255.252
Router0(config-if)# no shutdown

! --- Static Routes ---
Router0(config)# ip route 192.168.20.0 255.255.255.0 10.0.0.2
Router0(config)# ip route 192.168.30.0 255.255.255.0 10.0.0.2
Router0(config)# ip route 11.0.0.0 255.255.255.252 10.0.0.2

Router0(config)# end
Router0# write memory
```

---

### 🔷 Router1 — Central Hub

```bash
Router> enable
Router# configure terminal
Router(config)# hostname Router1

! --- LAN Interface ---
Router1(config)# interface FastEthernet0/0
Router1(config-if)# ip address 192.168.20.1 255.255.255.0
Router1(config-if)# no shutdown

! --- WAN Interface (to Router0) ---
Router1(config)# interface Serial0/0
Router1(config-if)# ip address 10.0.0.2 255.255.255.252
Router1(config-if)# no shutdown

! --- WAN Interface (to Router2) ---
Router1(config)# interface Serial0/1
Router1(config-if)# ip address 11.0.0.1 255.255.255.252
Router1(config-if)# no shutdown

! --- Static Routes ---
Router1(config)# ip route 192.168.10.0 255.255.255.0 10.0.0.1
Router1(config)# ip route 192.168.30.0 255.255.255.0 11.0.0.2

Router1(config)# end
Router1# write memory
```

---

### 🔷 Router2 — Right Gateway

```bash
Router> enable
Router# configure terminal
Router(config)# hostname Router2

! --- LAN Interface ---
Router2(config)# interface FastEthernet0/0
Router2(config-if)# ip address 192.168.30.1 255.255.255.0
Router2(config-if)# no shutdown

! --- WAN Interface ---
Router2(config)# interface Serial0/1
Router2(config-if)# ip address 11.0.0.2 255.255.255.252
Router2(config-if)# no shutdown

! --- Static Routes ---
Router2(config)# ip route 192.168.10.0 255.255.255.0 11.0.0.1
Router2(config)# ip route 192.168.20.0 255.255.255.0 11.0.0.1
Router2(config)# ip route 10.0.0.0 255.255.255.252 11.0.0.1

Router2(config)# end
Router2# write memory
```

---

## 🔀 Static Routes Explained

Static routing means each router is **manually told** where to forward packets for networks it does not directly know about. Unlike dynamic protocols, routes do not auto-update — the administrator defines every path.

### How Packets Travel (PC0 → PC5)

```
PC0 (192.168.10.2)
  │
  ▼ Default Gateway: 192.168.10.1
Router0 → checks routing table → forwards to 10.0.0.2 (Router1)
  │
  ▼ Serial Link: 10.0.0.0/30
Router1 → checks routing table → forwards to 11.0.0.2 (Router2)
  │
  ▼ Serial Link: 11.0.0.0/30
Router2 → directly connected → delivers to 192.168.30.3
  │
  ▼
PC5 (192.168.30.3) ✅ — Packet Delivered!
```

### Why /30 on WAN Links?

A **/30 subnet** provides only **2 usable IPs**, which is ideal for point-to-point serial links between two routers. Using a /24 on a WAN link would waste 252 IP addresses unnecessarily.

---

## ✅ Testing & Verification

### Ping Test Results

| Source | Destination   | Hops         | Result     |
|--------|---------------|--------------|------------|
| PC0    | 192.168.20.2  | R0 → R1      | ✅ Success |
| PC0    | 192.168.30.3  | R0 → R1 → R2 | ✅ Success |
| PC1    | 192.168.30.2  | R0 → R1 → R2 | ✅ Success |
| PC2    | 192.168.10.2  | R1 → R0      | ✅ Success |
| PC4    | 192.168.10.3  | R2 → R1 → R0 | ✅ Success |
| PC5    | 192.168.20.3  | R2 → R1      | ✅ Success |

### Verification Commands Used

```bash
# Verify full routing table on any router
show ip route

# Check all interface statuses (up/up = working)
show ip interface brief

# Test basic connectivity
ping 192.168.30.2

# Trace the full path a packet takes
tracert 192.168.30.2        # On PC (CMD)
traceroute 192.168.30.2     # On Router
```

> 📸 Screenshots of ping results are available in the `/screenshots` folder.

---

## ▶️ How to Run

### Prerequisites

- [Cisco Packet Tracer](https://www.netacad.com/courses/packet-tracer) — v7.x or v8.x recommended (free with Cisco NetAcad account)

### Steps

```bash
# 1. Clone this repository
git clone https://github.com/yourusername/static-routing-project.git

# 2. Navigate into the folder
cd static-routing-project

# 3. Open the Packet Tracer file
#    (Double-click or open from within Packet Tracer)
final-static-routing.pkt
```

4. Once open, switch to **Simulation Mode** (bottom right) to observe packet flow in real time
5. Open any PC → Desktop → Command Prompt
6. Run `ping <destination IP>` to test connectivity between all segments

---

## 💡 Key Learnings

Through this project, the following networking concepts were applied hands-on:

- **Static route syntax** — `ip route <network> <subnet-mask> <next-hop>`
- **WAN vs LAN subnetting** — using /30 for serial links vs /24 for LAN segments
- **Serial interface configuration** — including `clock rate` for DCE ends
- **Gateway of Last Resort** — understanding default gateways on end hosts
- **Routing table analysis** — reading `show ip route` output
- **Ping & traceroute** — verifying and debugging connectivity issues
- **IP address planning** — designing an efficient addressing scheme before configuration

---

## 📁 Repository Structure

```
static-routing-project/
│
├── README.md                        ← You are here
├── final-static-routing.pkt         ← Cisco Packet Tracer project file
│
├── /screenshots/
│   ├── topology.png                 ← Full network topology view
│   ├── router0-config.png           ← Router0 running config
│   ├── router1-config.png           ← Router1 running config
│   ├── router2-config.png           ← Router2 running config
│   └── ping-tests.png               ← Successful ping results
│
├── /configs/
│   ├── Router0-config.txt           ← Exported CLI config
│   ├── Router1-config.txt           ← Exported CLI config
│   └── Router2-config.txt           ← Exported CLI config
│
└── /docs/
    └── IP-Addressing-Table.md       ← Detailed IP plan
```

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE) — feel free to use it for learning purposes.

---

<div align="center">

⭐ **If you found this project helpful, please give it a star!** ⭐

*Built with ❤️ using Cisco Packet Tracer*

</div>
