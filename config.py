import math
import json

import ospf
import ebgp
import ibgp
import rip
import classes as c

def generate_cisco_config(intent_file, output_file):
    
    with open(intent_file, 'r') as file:
        network_intents = json.load(file)["networkIntents"]    # charger le fichier JSON et récupérer la liste des intents 
    with open(output_file, 'w') as file:      # ouvrir le fichier de sortie en mode écriture 
        
        # dict_as = {}  peut être utilisé pour stocker les AS
      
         for intent in network_intents:
            as_number = intent["ASNumber"]
            igp_protocol = intent["IGP"]
            ip_range = intent["IPRange"]  
            
            ip_range_reseau = ip_range.split("/")[0]
            print(ip_range_reseau)
            ip_range_mask = ip_range.split("/")[1]    
            print(ip_range_mask)
            
            
            as_name=f"AS{as_number}"
            as_name = c.AS(as_number, igp_protocol, ip_range)    # créer un objet AS
                
            for router in intent["Routers"]:
                router_id = router["RouterID"]
                neighbors = router["Neighbors"]
                interfaces = router["Interfaces"]
                
                router_name = f"R{router_id}"
                router_name = c.router(as_number, router_id)   # créer un objet router
                as_name.router.append(router_name)   # ajouter le router à l'AS
                
                for interface in interfaces:
                    interface_name = f"R{interface}"
                    interface_name = c.interface(igp_protocol)   # créer un objet interface
                    router_name.interfaces.append(interface_name)   # ajouter l'interface au router
                    
                    if interface_name=="Loopback 0":    
                        interface_name.loopback=True    # configurer l'interface comme une interface loopback
                    else:
                        interface_name.protocol=igp_protocol
                        if igp_protocol=="OSPF":
                            ospf.ospf_config(output_file,interface_name, router_id, as_number)   # configurer OSPF sur le router
                        elif igp_protocol=="RIP":
                            rip.rip_config(output_file,interface_name, router_id, as_number)   # configurer RIP sur le router
                        else:
                            print("Error: IGP protocol not supported")
                
                for neighbor in neighbors:
                    neighbor_router_id = neighbor["RouterID"]
                    neighbor_interface = neighbor["Interface"]
                    router_name.add_neighbor(neighbor_router_id, neighbor_interface)     # ajouter un voisin dans la liste
                
            as_name.linkscollect()   # collecter les liens entre les routeurs de l'AS 
            print(as_name.links)
            dict_subnet=subnet_calculate(ip_range_reseau,ip_range_mask,len(as_name.links))   
            print(dict_subnet)
            
            i=0   # key du dictionnaire dict_subnet
            for link in as_name.links:
                router_id=link[0]
                self_interface=link[1]
                neighbor_id=link[2]
                neighbor_interface=link[3]
                link_ip=dict_subnet[i]   # récupérer le préfixe du sous-réseau    
                print(link_ip)
                
                '''
                comme link[0] est toujours le routeur dans ce AS, 
                on peut directement configurer l'adresse IP de l'interface de routeur
                '''
                self_interface.ipv6_address=link_ip.split("/")[0]+"1"+"/"+link_ip.split("/")[1]   
                print(self_interface.ipv6_address)
                ipv6_config(output_file,self_interface, router_id, as_number,self_interface.ipv6_address)   
                
                # si le voisin est un routeur de l'AS
                if neighbor_interface!=None:
                    neighbor_interface.ipv6_address=link_ip.split("/")[0]+"2"+"/"+link_ip.split("/")[1]   # configurer l'adresse IP de l'interface de voisin  
                    print(neighbor_interface.ipv6_address)
                    ipv6_config(output_file,neighbor_interface, neighbor_id, as_number,neighbor_interface.ipv6_address)   # configurer l'adresse IP de l'interface de voisin       
                
                i+=1        
                
                
                
                
                        
               
               
               
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
                    
            
    
    
                       
                      
          
                        


    
    
    




                
