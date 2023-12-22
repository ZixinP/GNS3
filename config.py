import json
import ospf
import ebgp
import ibgp
import rip

def generate_cisco_config(intent_file, output_file):
    with open(intent_file, 'r') as file:
        network_intents = json.load(file)["networkIntents"]    # charger le fichier JSON et récupérer la liste des intents 
    with open(output_file, 'w') as file:      # ouvrir le fichier de sortie en mode écriture 
      links = []
      for intent in network_intents:
        as_number = intent["ASNumber"]
        igp_protocol = intent["IGP"]
        ip_range = intent["IPRange"]
        loopback_range = intent["LoopbackRange"]
        number_of_interface = 0  
        
        
        output_file.write(f"! Configuration for AS {as_number}\n")  # écrire le numéro d'AS dans le fichier de sortie
        output_file.write(f"router {igp_protocol.lower()} {as_number}\n")   # écrire le protocole IGP dans le fichier de sorti
       
         
        for router in intent["Routers"]:
            router_id = router["RouterID"]
            neighbors = router["Neighbors"]
            interfaces = router["Interfaces"]
            
            # configurer le protocole IGP
            if igp_protocol == "OSPF":
                for interface in interfaces:
                    ospf.ospf_config(output_file,interface, router_id, as_number)
            elif igp_protocol == "RIP":
                for interface in interfaces:
                    rip.rip_config(output_file,interface, router_id, as_number)
           
            # Ajouter les liens entre les routeurs
            for neighbor in neighbors:
                neighbor_router_id = neighbor["RouterID"]
                neighbor_interface = neighbor["Interface"]
                for link in links:
                    if len(link) != 4:   
                        if link[1] == router_id and link[0] == neighbor_router_id :
                            link[3]=neighbor_interface
                        else:   
                            links.append((router_id, neighbor_router_id, neighbor_interface))
                    
            
            
            
            
                    
            # l'addressage IPv6        
                
                
                output_file.write(f"R{router_id}# configure terminal \n")        
                output_file.write(f"R{router_id}# ipv6 unicast routing \n")
                output_file.write(f"R{router_id}# interface {n_interface} \n")
                output_file.write(f"R{router_id}# ipv6 address {interface_ip} \n")
                output_file.write(f"R{router_id}# no shutdown \n")
                output_file.write(f"R{router_id}# end \n")
                
            
                         
                      
          
                        


    
    
    




                
