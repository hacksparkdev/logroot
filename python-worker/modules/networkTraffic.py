from scapy.all import sniff

def run(params):
    duration = params.get("duration", 60)  # Capture for 60 seconds
    interface = params.get("interface", None)  # Optional: specify network interface

    def packet_callback(packet):
        return packet.summary()

    packets = sniff(timeout=duration, iface=interface, prn=packet_callback)
    return [str(packet) for packet in packets]

