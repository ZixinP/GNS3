

def ebgp_config(outputfile, interface, router_id, as_number, neighbor_router_ip, neighbor_as_number):
    outputfile.write(f"R{router_id}# configure terminal \n")
    outputfile.write(f"R{router_id}# router bgp {as_number} \n")
    outputfile.write(f"R{router_id}# no bgp default ipv4-unicast \n")
    outputfile.write(f"R{router_id}# bgp router-id {router_id}.{router_id}.{router_id}.{router_id} \n")   
    outputfile.write(f"R{router_id}# neighbor {neighbor_router_ip} remote-as {neighbor_as_number} \n")
    outputfile.write(f"R{router_id}# address-family ipv6 unicast \n")
    outputfile.write(f"R{router_id}# neighbor {neighbor_router_ip} activate \n")
    outputfile.write(f"R{router_id}# end \n")
 