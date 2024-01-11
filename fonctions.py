import math
import json



# charger le fichier JSON et récupérer la liste des intents               
def open_file(intent_file):
    with open(intent_file, 'r') as file:
        network_intents = json.load(file)["networkIntents"]    # charger le fichier JSON et récupérer la liste des intents
    return network_intents                       
               
               
               
# diviser le préfixe en sous-réseaux              
def subnet_calculate(ip_range,ip_mask,subnet_amount):    
    dict_subnet={}
    log_base_2 = math.log2(subnet_amount)
    result = math.ceil(log_base_2)   
    prefix_nb=int(ip_mask)+result      # calculer le préfixe selon le nombre de sous-réseaux             
    prefix_network=ip_range.split("::")[0]  
    prefix_network_lastbyte=int(prefix_network.split(":")[-1])   # récupérer le dernier byte du préfixe
    for i in range(subnet_amount):
        prefix_network_lastbyte+=1
       
        # choisir le préfixe du sous-réseau sauf le dernier byte
        prefix_network=prefix_network.split(":")[:-1]  
        
        # ajouter le dernier byte
        prefix_network.append(str(prefix_network_lastbyte))
       
        # construire le nouveau préfixe
        prefix_network=":".join(prefix_network)
        prefix_network=prefix_network+"/" + str(prefix_nb)
        
        #le stocker dans un dictionnaire
        dict_subnet[i]=prefix_network
   
    return dict_subnet
                 
# configurer l'adresse IP de l'interface
def ipv6_config(output_file,interface, router_id, as_number,interface_ip):    
    output_file.write(f"R{router_id}# configure terminal \n")        
    output_file.write(f"R{router_id}# ipv6 unicast routing \n")
    output_file.write(f"R{router_id}# interface {interface} \n")
    output_file.write(f"R{router_id}# ipv6 address {interface_ip} \n")
    output_file.write(f"R{router_id}# no shutdown \n")
    output_file.write(f"R{router_id}# end \n")                    
                    
            
