import math
import json



# charger le fichier JSON et récupérer la liste des intents               
def open_file(intent_file):
    with open(intent_file, 'r') as file:
        network_intents = json.load(file)["networkIntents"]    # charger le fichier JSON et récupérer la liste des intents
    return network_intents                       
               
               
               
# diviser le préfixe en sous-réseaux              
def subnet_calculate(ip_range_reseau,ip_range_prefix,subnet_amount):  
    dict_subnet={}
    log_base_2 = math.log2(subnet_amount)
    result = math.ceil(log_base_2)   
    prefix_nb=int(ip_range_prefix)+result      # calculer le préfixe selon le nombre de sous-réseaux             
    prefix_network=ip_range_reseau.split("::")[0]   # récupérer le préfixe du réseau
    for i in range(subnet_amount):
        if i != 0:
            new_prefix_network = prefix_network + ":" + str(i) + "::/" + str(prefix_nb)   
        else:
            new_prefix_network = prefix_network + "::/" + str(prefix_nb)   
        #le stocker dans un dictionnaire
        dict_subnet[i]=new_prefix_network
   
    return dict_subnet
                 
# configurer l'adresse IP de l'interface
def ipv6_config(as_number,interface, igp, add_ipv6, dict):  
    if igp == "OSPF":
        dict["interface"][f'{interface}']=[
            f"interface {interface}",
            " no ip address",
            " negotiation auto",
            f" ipv6 address {add_ipv6}",
            " ipv6 enable",
            f" ipv6 ospf 1 area {as_number}"
        ]
    elif igp == "RIP":
        dict["interface"][f'{interface}']=[
            f"interface {interface}",
            " no ip address",
            " negotiation auto",
            f" ipv6 address {add_ipv6}",
            " ipv6 enable",
            f" ipv6 rip {as_number} enable"
        ] 
                    
def add_ipv6_config(as_number,inter_name,igp,add_ipv6,dict,router_id,dict_data):
    ipv6_config(as_number,inter_name,igp,add_ipv6,dict)
    for router in dict_data[as_number].router:
        if router.router_id==router_id:
            for interface in router.interfaces_physiques:
                if interface.name==inter_name:
                    interface.ipv6_address=add_ipv6
                    break  
    
    
def loopback_config(as_number,interface,igp,add_ipv6,dict):
    if igp == "OSPF":
        dict["interface"][f'{interface}']=[
            f"interface {interface}",
            " no ip address",
            f" ipv6 address {add_ipv6}",
            " ipv6 enable",
            f" ipv6 ospf 1 area {as_number}"
        ]
    elif igp == "RIP":
        dict["interface"][f'{interface}']=[
            f"interface {interface}",
            " no ip address",
            f" ipv6 address {add_ipv6}",
            " ipv6 enable",
            f" ipv6 rip {as_number} enable"
        ]
       


def inter_init(dict,interface):
    dict["interface"][f'{interface}'] = [
        f"interface {interface}",
        "no ipv6 address",
        "shutdown",
        "negotiation auto" 
    ]
    
def igp_code(dict_data,dict_config_dict):
    for AS in dict_data.values():
        as_number = AS.as_number
        for router in AS.router:
            router_id = router.router_id
            dict = dict_config_dict[router_id]
            if AS.igp_protocol == "OSPF":
                dict["IGP"]=[
                    "ipv6 router ospf 1",
                    f"router-id {router_id}.{router_id}.{router_id}.{router_id}"
                ]
            elif AS.igp_protocol == "RIP":
                dict["IGP"]=[
                    f"ipv6 router rip {as_number}",
                    " redistribute connected",
                ]