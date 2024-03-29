

def write_in_config(dict_output_file,dict_config_dict):
   for router, dict in dict_config_dict.items():
       output_file = dict_output_file[router]
       with open(output_file, 'w') as file:
            file.write("!\n")
            file.write("!\n")
            file.write("upgrade fpd auto\n")
            file.write("version 12.4\n")
            file.write("service timestamps debug datetime msec\n")
            file.write("service timestamps log datetime msec\n")
            file.write("no service password-encryption\n")
            file.write("!\n")
            file.write(f"hostname R{router}\n")
            file.write("!\n")
            file.write("boost-start-marker\n")
            file.write("boot-end-marker\n")
            file.write("!\n")
            file.write("!\n")
            file.write("no aaa new-model\n")
            file.write("no ip icmp rate-limit unreachable\n")
            file.write("ip cef\n")
            file.write("!\n")
            file.write("no ip domain lookup\n")
            file.write("ipv6 unicast-routing\n")
            file.write("!\n")
            file.write("multilink bundle-name authenticated\n")
            file.write("!\n")
            file.write("archive\n")
            file.write(" log config\n")
            file.write("  hidekeys\n")
            file.write("!\n")
            file.write("ip tcp synwait-time 5\n")
            file.write("!\n")
            for interface in dict["interface"]:
                for command in dict["interface"][interface]:
                    file.write(command+"\n")
                file.write("!\n")
            for command in dict["BGP"]["bgp"]:
                file.write(command+"\n")
            for command in dict["BGP"]["bgp neighbor"]:
                file.write(command+"\n")
            file.write("!\n")
            for command in dict["BGP"]["neighbor active"]:
                file.write(command+"\n")
            for command in dict["BGP"]["network"]:
                file.write(command+"\n")
            file.write("!\n")
            file.write("ip forward-protocol nd\n")
            file.write("no ip http server\n")
            file.write("no ip http secure-server\n")
            file.write("!\n")
            file.write("!\n")
            file.write("logging alarm informational\n")
            file.write("no cdp log mismatch duplex\n")
            for command in dict["IGP"]:
                file.write(command+"\n")
            file.write("!\n")
            file.write("!\n")
            file.write("ipv6 prefix-list TAG_COMMUNITY seq 10 permit ::/0 le 128\n")
            file.write("!\n")
            file.write("!\n")
            for command in dict["access-list"]:
                for acl in command:
                    file.write(acl+"\n")
            for route_map in dict["route-map"]:
                for command in route_map:
                    file.write(command+"\n")
            file.write("!\n")
            file.write("control-plane\n")
            file.write("!\n")
            file.write("gatekeeper\n")
            file.write(" shutdown\n")
            file.write("!\n")
            file.write("line con 0\n")
            file.write(" exec-timeout 0 0\n")
            file.write(" privilege level 15\n")
            file.write(" logging synchronous\n")
            file.write(" stopbits 1\n")
            file.write("line vty 0 4\n")
            file.write(" login\n")
            file.write("!\n")
            file.write("!\n")
            file.write("end\n")