
import protocols as p
import classes as c
import fonctions as f

dict_data = {}  # dictionnaire pour stocker tous les objets créés
dict_output_file = {}  # dictionnaire pour stocker les fichiers de consignes de configuration des routeurs différents


# Description: creation des consigne de configuration des adresses IPv6 sur les interfaces physiques
def generate_cisco_config_physique(network_intents, dict_data, dict_output_file):
        
        for intent in network_intents:
            as_number = intent["ASNumber"]
            igp_protocol = intent["IGP"]
            ip_range = intent["IPRange"]  
            provider = intent["Provider"]
            customers = intent["Customers"]
            peers = intent["Peers"]
            
            ip_range_reseau = ip_range.split("/")[0]
            print(ip_range_reseau)
            ip_range_mask = ip_range.split("/")[1]    
            print(ip_range_mask)
            
            
            as_name=f"AS{as_number}"
            as_name = c.AS(as_number, igp_protocol, ip_range,ip_range_mask)
            
            for provider_as in provider:
                as_name.provider[provider_as]=f"{as_number}:{provider_as}"
            for customer_as in customers:
                as_name.customers[customer_as]=f"{as_number}:{customer_as}"
            for peer_as in peers:
                as_name.peers[peer_as]=f"{as_number}:{peer_as}"
            
            for router in intent["Routers"]:
                router_id = router["RouterID"]
                neighbors = router["Neighbors"]
                interfaces = router["Interfaces"]
                
                router_name = f"R{router_id}"
                router_name = c.router(as_number, router_id)   # créer un objet router
                as_name.router.append(router_name)   # ajouter le router à l'AS
                
                output_file_name = f"R{router_id}.cfg"     # creer le fichier de sortie
                
                for interface in interfaces:
                    interface_obj = f"R{router_id}{interface}"
                    interface_obj = c.interface(router_id,interface,igp_protocol)   # créer un objet interface
                    
                    # ajouter l'interface aux listes des interfaces du router
                    if interface_obj.name not in router_name.interfaces_physiques and interface_obj.name not in router_name.interface_loopback:
                        if interface == "Loopback 0":
                            router_name.interface_loopback.append(interface_obj)   # ajouter l'interface loopback à la liste des interfaces loopback du router
                            interface_obj.loopback=True                    #identifiant pour l'interface loopback
                        else:
                            router_name.interfaces_physiques.append(interface_obj)   # ajouter l'interface physique à la liste des interfaces physiques du router)                  
                            
                            # configurer le protocole IGP sur l'interface physique
                            interface_obj.protocol=igp_protocol
                            if igp_protocol=="OSPF":
                                with open(output_file_name, 'w') as file:      # ouvrir le fichier de sortie en mode écriture 
                                    p.ospf_config(output_file_name,interface_obj.name, router_id, as_number)   # configurer OSPF sur le router
                            elif igp_protocol=="RIP":
                                with open(output_file_name, 'w') as file:      # ouvrir le fichier de sortie en mode écriture                                
                                    p.rip_config(output_file_name,interface_obj.name, router_id, as_number)   # configurer RIP sur le router
                            else:
                                print("Error: IGP protocol not supported")
                    
                        
                
                for neighbor in neighbors:
                    neighbor_router_id = neighbor["RouterID"]
                    neighbor_interface = neighbor["Interface"]
                    router_name.add_neighbor(neighbor_router_id, neighbor_interface)     # ajouter un voisin dans la liste
                
                dict_output_file[router_id]=output_file_name   # ajouter le fichier de sortie au dictionnaire dict_output_file
                #Creer un thread pour chaque fichier de sortie, et les executer en parallele       
               
            
            as_name.linkscollect()   # collecter les liens entre les routeurs de l'AS 
            print(as_name.links)
            dict_subnet=f.subnet_calculate(ip_range_reseau,ip_range_mask,len(as_name.links))   
            print(dict_subnet)
            as_name.subnets=dict_subnet   # ajouter les sous-réseaux au dictionnaire dict_subnet
            
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
                
                for interface in as_name.router[0].interfaces_physiques:
                    if interface.name==self_interface:
                        
                        interface.ipv6_address=link_ip.split("/")[0]+"1"+"/"+link_ip.split("/")[1]     # configurer l'adresse IP de l'interface de routeur
                        print(interface.ipv6_address)
                         
                         # si le voisin est un routeur d'un autre AS  
                        if neighbor_id == None:               
                            for output_file_key in dict_output_file.keys():
                                if router_id == output_file_key:
                                    f.ipv6_config(dict_output_file[output_file_key],self_interface, router_id, as_number,interface.ipv6_address)   
                                    if interface.protocol=="OSPF":
                                        p.ospf_mode_passive(dict_output_file[output_file_key],self_interface, router_id, as_number)   # configurer OSPF en mode passif sur l'interface physique
                        
                         # si le voisin est un routeur dans ce AS
                        else:
                            for output_file_key in dict_output_file.keys():
                                if router_id == output_file_key:
                                    f.ipv6_config(dict_output_file[output_file_key],self_interface, router_id, as_number,interface.ipv6_address)   
                
                            for interface in as_name.router[0].interfaces_physiques: 
                                if interface.name==neighbor_interface:
                                    interface.ipv6_address=link_ip.split("/")[0]+"2"+"/"+link_ip.split("/")[1]    # configurer l'adresse IP de l'interface de voisin
                                    print(interface.ipv6_address)
                                    for output_file_key in dict_output_file.keys():
                                        if neighbor_id == output_file_key:  
                                            f.ipv6_config(dict_output_file[output_file_key],neighbor_interface, neighbor_id, as_number,interface.ipv6_address)          
                               
                i+=1     
        
            dict_data[as_number]=as_name   # ajouter l'AS au dictionnaire dict_data 
        
          
                

# Description: creation des consigne de configuration des adresses IPv6 sur les interfaces loopback
def generate_cisco_config_loopback(network_intent, dict_data, dict_output_file):     
    
    for intent in network_intent:
        as_number = intent["ASNumber"]
        loopback_range = intent["loopbackRange"]
            
        lo_range_reseau = loopback_range.split("/")[0]
        print(lo_range_reseau)
        lo_range_mask = loopback_range.split("/")[1]
        print(lo_range_mask)
        
        i=1
        for router in dict_data[as_number].router:
            router_id = router.router_id
            for interface in router.interface_loopback:
                interface.loopback_address=lo_range_reseau+str(i)+"/"+lo_range_mask
                print(interface.loopback_address)
                i+=1
                for output_file_key in dict_output_file.keys():
                    if router_id == output_file_key:
                        f.ipv6_config(dict_output_file[output_file_key],interface.name, router_id, as_number,interface.loopback_address)   # configurer l'adresse loopback sur les interfaces loopback 
                
            
                           
    
    
    
    
    
    
    
               
                    
            


    
                       
                      
          
                        


    
    
    




                
