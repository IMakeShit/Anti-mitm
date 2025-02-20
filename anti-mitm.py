from scapy.all import Ether, ARP, srp, sniff, conf, os, subprocess

def get_mac(ip):
    p = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip)
    result = srp(p, timeout=3, verbose=False)[0]
    return result[0][1].hwsrc
def process(packet):
    if packet.haslayer(ARP):
        if packet[ARP].op == 2:
            try:                
                real_mac = get_mac(packet[ARP].psrc)
                response_mac = packet[ARP].hwsrc
                if real_mac != response_mac:
                       os.system("iptables -A INPUT -m mac --mac-source " + response_mac + " -j DROP")
                       os.system('notify-send "Обнаружена возможная mitm атака!"')
            except IndexError:
                pass
sniff(store=False, prn=process)
