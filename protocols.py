import ipaddress

def ospf_config(output_file,interface, router_id, as_number):
    with open(output_file, 'a') as file:
        file.write(f"R{router_id}# configure terminal \n")
        file.write(f"R{router_id}# ipv6 unicast routing \n")
        file.write(f"R{router_id}# ipv6 router ospf {as_number}\n")
        file.write(f"R{router_id}# router-id {router_id}.{router_id}.{router_id}.{router_id} \n")
        file.write(f"R{router_id}# exit \n")
        file.write(f"R{router_id}# interface {interface} \n")
        file.write(f"R{router_id}# ipv6 enable\n")
        file.write(f"R{router_id}# ipv6 ospf {as_number} area {as_number} \n")
        file.write(f"R{router_id}# end \n")


def ospf_mode_passive(output_file,interface, router_id, as_number):
    with open(output_file, 'a') as file:
        file.write(f"R{router_id}# configure terminal \n")
        file.write(f"R{router_id}# interface {interface} \n")
        file.write(f"R{router_id}# ipv6 router ospf passive {as_number} \n")
        file.write(f"R{router_id}# passive-interface {interface}\n")
        file.write(f"R{router_id}# end \n")

def ospf_cost_commands(output_file,interface, router_id, as_number,metric_value):
     with open(output_file, 'a') as file:
        file.write(f"R{router_id}# configure terminal \n")
        file.write(f"R{router_id}# interface {interface} \n")
        file.write(f"R{router_id}# ipv6 ospf 1 area {as_number}\n")
        file.write(f"R{router_id}# cost {metric_value}\n")
        file.write(f"R{router_id}# end \n")
         
        
        
def rip_config(output_file,interface, router_id, as_number):
   with open(output_file, 'a') as file:
       file.write(f"R{router_id}# configure terminal \n")
       file.write(f"R{router_id}# ipv6 unicast routing \n")
       file.write(f"R{router_id}# ipv6 router rip {as_number}\n")
       file.write(f"R{router_id}# redistribute connected \n")
       file.write(f"R{router_id}# interface {interface} \n")
       file.write(f"R{router_id}# ipv6 rip {as_number} enable\n")
       file.write(f"R{router_id}# end \n")


def ibgp_config(output_file,as_number,router_id,interface, neighbor_router_ip):
    with open(output_file, 'a') as file:
        file.write(f"R{router_id}# configure terminal\n")
        file.write(f"R{router_id}# interface {interface}\n")
        file.write(f"R{router_id}# router bgp {as_number}\n")
        file.write(f"R{router_id}# neighbor {neighbor_router_ip} remote-as {as_number}\n")
        file.write(f"R{router_id}# end \n")
    

def ebgp_config(outputfile,as_number, router_id,neighbor_as_number,neighbor_router_ip):
    with open(outputfile, 'a') as file:
        file.write(f"R{router_id}# configure terminal \n")
        file.write(f"R{router_id}# router bgp {as_number} \n")
        file.write(f"R{router_id}# no bgp default ipv4-unicast \n")
        file.write(f"R{router_id}# bgp router-id {router_id}.{router_id}.{router_id}.{router_id} \n")   
        file.write(f"R{router_id}# neighbor {neighbor_router_ip} remote-as {neighbor_as_number} \n")
        file.write(f"R{router_id}# address-family ipv6 unicast \n")
        file.write(f"R{router_id}# neighbor {neighbor_router_ip} activate \n")
        file.write(f"R{router_id}# end \n")   
        
