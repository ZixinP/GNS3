import ipaddress

def ibgp_config(output_file,interface, as_number,neighbor_router_ip,router_id):
    output_file.write(f"R{router_id}# configure terminal\n")
    output_file.write(f"R{router_id}# interface {interface}\n")
    output_file.write(f"R{router_id}# router bgp {as_number}\n")
    output_file.write(f"R{router_id}# neighbor {neighbor_router_ip} remote-as {as_number}\n")
    output_file.write(f"R{router_id}# end \n")
