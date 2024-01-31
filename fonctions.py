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
def ipv6_config(output_file,interface, router_id,interface_add):    
    with open(output_file, 'a') as output_file:
        output_file.write(f"R{router_id}# configure terminal \n")        
        output_file.write(f"R{router_id}# ipv6 unicast routing \n")
        output_file.write(f"R{router_id}# interface {interface} \n")
        output_file.write(f"R{router_id}# ipv6 address {interface_add} \n")
        output_file.write(f"R{router_id}# no shutdown \n")
        output_file.write(f"R{router_id}# end \n")
                
                    
def add_ipv6_config(as_number,router_id,inter_name,add_ipv6,dict_output_file,dict_data):
    for output_file_key in dict_output_file.keys():
        if router_id == output_file_key:
            ipv6_config(dict_output_file[output_file_key],inter_name, router_id,add_ipv6)  
            for router in dict_data[as_number].router:
                if router.router_id==router_id:
                    for interface in router.interfaces_physiques:
                        if interface.name==inter_name:
                            interface.ipv6_address=add_ipv6
                            break  
    
    
    
