

def ospf_mode_passive(dict,interface):
    dict["IGP"].append(f" interface {interface} ospf passive")

def rip_mode_passive(dict,interface,as_number):
    dict["IGP"].append(f" interface {interface} no ipv6 rip {as_number} enable")

def ospf_cost_commands(dict,interface,cost):
    dict["interface"][f'{interface}'].append(f" ipv6 ospf cost {cost}")         

def bgp_init(dict_config_dict,dict_data):
    for AS in dict_data.values():
        as_number = AS.as_number
        for router in AS.router:
            router_id = router.router_id
            dict = dict_config_dict[router_id]
            dict["BGP"]["bgp"]=[
            f"router bgp {as_number}",
            f" bgp router-id {router_id}.{router_id}.{router_id}.{router_id}",
            " no bgp default ipv4-unicast",
            " bgp log-neighbor-changes"
            ]
            
            dict["BGP"]["neighbor active"]=[
            " address-family ipv6 unicast"
            ]


def ibgp_config(dict,as_number,nei_add):
    dict["BGP"]["bgp neighbor"].append(f" neighbor {nei_add} remote-as {as_number}")
    dict["BGP"]["bgp neighbor"].append(f" neighbor {nei_add} update-source loopback0")
    dict["BGP"]["neighbor active"].append(f"  neighbor {nei_add} activate")
    dict["BGP"]["neighbor active"].append(f"  neighbor {nei_add} send-community")



def ebgp_config(dict,nei_as,nei_add):
    dict["BGP"]["bgp neighbor"].append(f" neighbor {nei_add} remote-as {nei_as}")
    dict["BGP"]["neighbor active"].append(f"  neighbor {nei_add} activate")

  
    
def network(dict_config_dict,dict_data):
    for AS in dict_data.values():
        for router in AS.router: 
            if router.ASBR == True:
                dict = dict_config_dict[router.router_id]        
                for route in AS.subnets.values():
                    dict["BGP"]["network"].append(f"  network {route}")
                dict["BGP"]["network"].append(" exit-address-family")
