
import protocols as p


def etablir_ibgp(dict_data, dict_config_dict):
    for AS in dict_data.values():
        for self_router in AS.router:
               dict = dict_config_dict[self_router.router_id]
               # etablir la session ibgp entre les routeurs d'un AS
               for other_router in AS.router:
                   if other_router.router_id != self_router.router_id:
                       for other_interface in other_router.interface_loopback:
                           other_router_loopback=other_interface.loopback_address.split("/")[0]
                           p.ibgp_config(dict, AS.as_number, other_router_loopback)
                                       



def etablir_ebgp(dict_data, dict_config_dict):
    ebgp_links=[]    # [router_as,router_id,router_interface,router_inter_add,neighbor_as,neighbor_id,neighbor_interface,neighbor_inter_add]
    for AS in dict_data.keys():
        as_number=dict_data[AS].as_number
        for link in dict_data[AS].links:
            router_id=link[0]                  
            if link[3]==None:    # selectionner les liens ebgp               
                for router in dict_data[AS].router:
                    if router.router_id==router_id:
                        for interface in router.interfaces_physiques:
                            if interface.name==link[1]:
                                add_ipv6=interface.ipv6_address    # recuperer l'adresse ipv6 de l'interface
                                if add_ipv6:
                                    add_ipv6 = add_ipv6.split("/")[0]
                                else:
                                    continue
                
                FLAG=True                 
                for ebgp_link in ebgp_links:
                   
                    # si le lien existe déjà dans la liste
                    if ebgp_link[1]==link[0]:
                        if ebgp_link[5]==link[2]:
                            FLAG=False
                   
                    # si le lien existe déjà dans la liste mais dans l'autre sens，il faut completer l'adresse ipv6
                    elif ebgp_link[1]==link[2]:
                        if ebgp_link[5]==link[0]:
                            FLAG=False
                            if ebgp_link[4]==None:
                                ebgp_link[4]=as_number
                                ebgp_link[6]= link[1]
                                ebgp_link[7]=add_ipv6
                
                # si le lien n'existe pas dans la liste, on l'ajoute
                if FLAG:
                    ebgp_links.append([as_number,router_id,link[1],add_ipv6,None,link[2],None,None])
    
    # configurer les liens ebgp                
    for link_complet in ebgp_links:
        print(link_complet)
        as_number=link_complet[0]
        router_id=link_complet[1]
        router_interface=link_complet[2]
        router_inter_add=link_complet[3]
        neighbor_as=link_complet[4]
        neighbor_id=link_complet[5]
        neighbor_interface=link_complet[6]
        neighbor_inter_add=link_complet[7]
        
        self_dict = dict_config_dict[router_id]
        nei_dict = dict_config_dict[neighbor_id]
        p.ebgp_config(self_dict,neighbor_as,neighbor_inter_add)
        p.ebgp_config(nei_dict,as_number,router_inter_add)
        
        # ajouter les informations de voisin dans les attributs d'interface
        for router in dict_data[as_number].router:
            if router.router_id==router_id:
                for interface in router.interfaces_physiques:
                    if interface.name == router_interface:
                        interface.neighbor_as = neighbor_as
                        interface.neighbor_id = neighbor_id
                        interface.neighbor_address = neighbor_inter_add
                        break
        for router in dict_data[neighbor_as].router:
            if router.router_id==neighbor_id:
                for interface in router.interfaces_physiques:
                    if interface.name == neighbor_interface:
                        interface.neighbor_as = as_number
                        interface.neighbor_id = router_id
                        interface.neighbor_address = router_inter_add
                        break
    print(ebgp_links)
    