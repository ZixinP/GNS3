import ipaddress

def ospf_config(output_file,interface, router_id, as_number):
    output_file.write(f"R{router_id}# ipv6 router ospf {as_number} \n")
    output_file.write(f"R{router_id}# router-id {router_id}.{router_id}.{router_id}.{router_id} \n")
    output_file.write(f"R{router_id}# exit \n")
    output_file.write(f"R{router_id}# interface {interface}  \n")
    output_file.write(f"R{router_id}# ipv6 router ospf {as_number} \n")
    output_file.write(f"R{router_id}# end \n")
    

def rip_config(output_file,interface, router_id, as_number):
   output_file.write(f"R{router_id}# configure terminal\n")
   output_file.write(f"R{router_id}# ipv6 router rip RIP{as_number}\n")
   output_file.write(f"R{router_id}# redistribute connected\n")
   output_file.write(f"R{router_id}# exit\n")
   output_file.write(f"R{router_id}# interface {interface}\n")
   output_file.write(f"R{router_id}# ipv6 rip RIP{as_number} enable\n")
   output_file.write(f"R{router_id}# end\n")
   

def ibgp_config(output_file,as_number,router_id,interface, neighbor_router_ip):
    output_file.write(f"R{router_id}# configure terminal\n")
    output_file.write(f"R{router_id}# interface {interface}\n")
    output_file.write(f"R{router_id}# router bgp {as_number}\n")
    output_file.write(f"R{router_id}# neighbor {neighbor_router_ip} remote-as {as_number}\n")
    output_file.write(f"R{router_id}# end \n")
    

def ebgp_config(outputfile, interface, router_id, as_number, neighbor_router_ip, neighbor_as_number):
    outputfile.write(f"R{router_id}# configure terminal \n")
    outputfile.write(f"R{router_id}# router bgp {as_number} \n")
    outputfile.write(f"R{router_id}# no bgp default ipv4-unicast \n")
    outputfile.write(f"R{router_id}# bgp router-id {router_id}.{router_id}.{router_id}.{router_id} \n")   
    outputfile.write(f"R{router_id}# neighbor {neighbor_router_ip} remote-as {neighbor_as_number} \n")
    outputfile.write(f"R{router_id}# address-family ipv6 unicast \n")
    outputfile.write(f"R{router_id}# neighbor {neighbor_router_ip} activate \n")
    outputfile.write(f"R{router_id}# end \n")   