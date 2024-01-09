# Description: This file contains the functions to configure RIP on a router
import ipaddress

def rip_config(output_file,interface, router_id, as_number):
   output_file.write(f"R{router_id}# configure terminal\n")
   output_file.write(f"R{router_id}# ipv6 router rip RIP{as_number}\n")
   output_file.write(f"R{router_id}# redistribute connected\n")
   output_file.write(f"R{router_id}# exit\n")
   output_file.write(f"R{router_id}# interface {interface}\n")
   output_file.write(f"R{router_id}# ipv6 rip RIP{as_number} enable\n")
   output_file.write(f"R{router_id}# end\n")
   