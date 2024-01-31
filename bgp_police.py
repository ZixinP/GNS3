'''
community: xxx:yyy (xxx = AS number, yyy = community number) contenu dans le paquet BGP UPDATE


# consignes pour match les routes avec community 100:1 donc on peut les filtrer dans la route-map
    route-map MY_POLICY permit 10
    match community 100:1

# consignes pour ajouter community 200:2 dans le paquet BGP UPDATE
    route-map MY_POLICY permit 20
    match ip address PREFIX_LIST
    set community 200:2


'''

import fonctions as f

def Community_local_pref(dict_data,dict_config_dict):
    for AS in dict_data.values():
        as_number = AS.as_number
        for router in AS.router:
            if router.ASBR:
                for interface in router.interfaces_physiques:
                    if interface.neighbor_id != None:
                        print(router.router_id,interface.name)
                        nei_add = interface.neighbor_address
                        dict = dict_config_dict[router.router_id]
                        # router bgp dict_data[AS].as_number                                
                        if interface.neighbor_as in AS.customers.keys():
                                com = AS.customer_com
                                dict["route-map"].append([
                                f"route-map Community_customer permit 10",
                                " match ipv6 address prefix-list TAG-COMMUNITY",
                                f" set community {as_number}:{com}",
                                " set local-preference 100"
                                ])                       
                                
                                dict["BGP"]["neighbor active"].append(f" neighbor {nei_add} route-map Community_customer in")
                                       
                                # marquer les routes de customer avec community et changer leur local preference
                                '''
                                        route-map Community_customer permit 10
                                         match ip address PREFIX_LIST
                                         set community {dict_data[AS].customer[interface.neighbor_as]}
                                        neighbor interface.neighbor_address route-map Community_customer in
                                                                             
                                        route-map SET_LOCAL_PREF_customer permit 20
                                         match community {dict_data[AS].customer[interface.neighbor_as]}
                                         set local-preference 100
                                        neighbor interface.neighbor_address route-map SET_LOCAL_PREF_customer in
                                                                                                               
                                '''
                                    
                                    # on fait rien dans le sens out de voisin de customer,car on veut que le voisin reçoit toutes les routes
                                    # dans le but de maximiser le profit
                                    
                        elif interface.neighbor_as in AS.peers.keys():
                                com = AS.peer_com
                                dict["route-map"].append([
                                f"route-map Community_peer permit 10",
                                " match ipv6 address prefix-list TAG-COMMUNITY",
                                f" set community {as_number}:{com}",
                                " set local-preference 200"
                                ])
                                        
                                dict["BGP"]["neighbor active"].append(f" neighbor {nei_add} route-map Community_peer in")
                                
                                # marquer les routes de peer avec community et changer leur local preference
                                '''
                                        route-map Community_peer permit 10
                                         match ip address PREFIX_LIST
                                         set community {dict_data[AS].peer[interface.neighbor_as]}
                                        neighbor interface.neighbor_address route-map Community_peer in
                                                                            
                                        route-map SET_LOCAL_PREF_peer permit 20
                                         match community {dict_data[AS].peer[interface.neighbor_as]}
                                         set local-preference 200
                                        neighbor interface.neighbor_address route-map SET_LOCAL_PREF_peer in                                                           
                                '''
                                        
                                # filtrer les routes pour que le voisin reçoit seulement les routes de customer et les routes de ce AS
                                dict["route-map"].append([
                                    "route-map Advertize_customer permit 30",
                                    f" match community {as_number}:{AS.customer_com}", 
                                    ])
                                dict["BGP"]["neighbor active"].append(f" neighbor {nei_add} route-map Advertize_customer out")
                                          
                                '''
                                            route-map Advertize_customer permit 30
                                             match community {dict_data[AS].customer[customer]}
                                            neighbor interface.neighbor_address route-map Advertize_customer out
                                '''


                                dict["route-map"].append([
                                    "route-map Advertize_peer deny 40",
                                    f" match community {as_number}:{AS.peer_com}", 
                                    ])
                                dict["BGP"]["neighbor active"].append(f" neighbor {nei_add} route-map Advertize_peer out")
                                                   
                                '''
                                            route-map Advertize_peer deny 40
                                             match community {dict_data[AS].peer[peer]}
                                            neighbor interface.neighbor_address route-map Advertize_peer out
                                '''
                                
                                dict["route-map"].append([
                                    "route-map Advertize_provider deny 50",
                                    f" match community {as_number}:{AS.provider_com}", 
                                    ])
                                dict["BGP"]["neighbor active"].append(f" neighbor {nei_add} route-map Advertize_provider out")
                                                                                    
                                '''
                                            route-map Advertize_provider deny 50
                                             match community {dict_data[AS].provider[provider]}
                                            neighbor interface.neighbor_address route-map Advertize_provider out
                                '''
                                        
                                dict["route-map"].append([
                                    "route-map Advertize_all permit 60",
                                    ])
                                dict["BGP"]["neighbor active"].append(f" neighbor {nei_add} route-map Advertize_all out")
                                        
                                '''
                                        route-map Advertize_all permit 60
                                        neighbor interface.neighbor_address route-map Advertize_all out
                                '''
                                        
                                        
                        elif interface.neighbor_as in AS.provider.keys():                                     
                                        com = AS.provider_com
                                        dict["route-map"].append([
                                            f"route-map Community_provider permit 10",
                                            " match ipv6 address prefix-list TAG-COMMUNITY",
                                            f" set community {as_number}:{com}",
                                            " set local-preference 300"
                                            ])
                                        dict["BGP"]["neighbor active"].append(f" neighbor {nei_add} route-map Community_provider in")
                                        
                                        
                                        # marquer les routes de provider avec community et changer leur local preference
                                        '''
                                        route-map Community_provider permit 10
                                         match ip address PREFIX_LIST
                                         set community {dict_data[AS].provider[interface.neighbor_as]}
                                        neighbor interface.neighbor_address route-map Community_provider in
                                        
                                        route-map SET_LOCAL_PREF_provider permit 20
                                            match community {dict_data[AS].provider[interface.neighbor_as]}
                                            set local-preference 300
                                        neighbor interface.neighbor_address route-map SET_LOCAL_PREF_provider in
                                    
                                        '''
                                        
                                        # filtrer les routes pour que le voisin reçoit seulement les routes de customer et les routes de ce AS
                                        dict["route-map"].append([
                                            "route-map Advertize_customer permit 30",
                                            f" match community {as_number}:{AS.customer_com}", 
                                            ])
                                        dict["BGP"]["neighbor active"].append(f" neighbor {nei_add} route-map Advertize_customer out")
                                        '''
                                            route-map Advertize_customer permit 30
                                             match community {dict_data[AS].customer[customer]}
                                            neighbor interface.neighbor_address route-map Advertize_customer out
                                        '''
                                    
                                        dict["route-map"].append([
                                            "route-map Advertize_peer deny 40",
                                            f" match community {as_number}:{AS.peer_com}", 
                                            ])
                                        dict["BGP"]["neighbor active"].append(f" neighbor {nei_add} route-map Advertize_peer out")
                                        '''
                                            route-map Advertize_peer deny 40
                                             match community {dict_data[AS].peer[peer]}
                                            neighbor interface.neighbor_address route-map Advertize_peer out
                                        '''
                                        
                                        dict["route-map"].append([
                                            "route-map Advertize_provider deny 50",
                                            f" match community {as_number}:{AS.provider_com}", 
                                            ])
                                        dict["BGP"]["neighbor active"].append(f" neighbor {nei_add} route-map Advertize_provider out")
                                        '''
                                            route-map Advertize_provider deny 50
                                             match community {dict_data[AS].provider[provider]}
                                            neighbor interface.neighbor_address route-map Advertize_provider out
                                        '''
                                        
                                        dict["route-map"].append([
                                            "route-map Advertize_all permit 60",
                                            ])
                                        dict["BGP"]["neighbor active"].append(f" neighbor {nei_add} route-map Advertize_all out")
                                        '''
                                        route-map Advertize_all permit 60
                                        neighbor interface.neighbor_address route-map Advertize_all out
                                        '''







