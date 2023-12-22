# Description: This file contains the function to configure OSPFv3 on a router
import ipaddress

def ospf_config(output_file,interface, router_id, as_number):
    output_file.write(f"R{router_id}# ipv6 router ospf {as_number} \n")
    output_file.write(f"R{router_id}# router-id {router_id}.{router_id}.{router_id}.{router_id} \n")
    output_file.write(f"R{router_id}# exit \n")
    output_file.write(f"R{router_id}# interface {interface}  \n")
    output_file.write(f"R{router_id}# ipv6 router ospf {as_number} \n")
    output_file.write(f"R{router_id}# end \n")