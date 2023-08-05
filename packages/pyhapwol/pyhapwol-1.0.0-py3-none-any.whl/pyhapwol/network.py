from scapy.all import Ether, ARP, IP, ICMP, srp1, sr1


def get_ip(mac, broadcast, iface=None):
    ether = Ether(dst=mac)
    arp = ARP(pdst=broadcast)
    result = srp1(ether/arp, iface=iface, timeout=2, verbose=0)
    if result and result[ARP].hwsrc == mac:
        return result[ARP].psrc
    return None


def ping(target_ip, iface=None):
    ip = IP(dst=target_ip)
    icmp = ICMP()
    result = sr1(ip/icmp, iface=iface, timeout=2, verbose=0)
    return result and result[IP].src == target_ip
