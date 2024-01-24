'''
community: xxx:yyy (xxx = AS number, yyy = community number) contenu dans le paquet BGP UPDATE


# consignes pour match les routes avec community 100:1 donc on peut les filtrer dans la route-map
    route-map MY_POLICY permit 10
    match community 100:1

# consignes pour ajouter community 200:2 dans le paquet BGP UPDATE
    route-map MY_POLICY permit 20
    match ip address PREFIX_LIST
    set community 200:2

#对于每一个asbr,network as.subnets里面的所有网段

# 对于每个asbr,通过遍历links_externe查看它的邻居所在的as,遍别是peer,provider,customer哪一个,并加在neighbors的最后一项,然后根据这个信息到对应端口来配置community

#! 进入BGP配置模式
router bgp <Your-AS-Number>

! 创建一个Route Map,用于匹配Community并更改local preference,customer的local preference最高,peer的次之,provider的最低
route-map SET_LOCAL_PREF permit 10
 match community 100:1
 set local-preference 200

! 应用Route Map到BGP邻居
neighbor <Neighbor-IP> route-map SET_LOCAL_PREF in

# 给customer路由器的in是允许全部通过,out是只允许自身的路由通过,peer的不行
# 给peer路由器的in是允许全部通过,out是只允许自身的路由通过,customer的不行
# 给provider路由器的in是允许全部通过,out是只允许自身的路由通过,customer的不行  
？？？不确定是不是这样

# 所有的community都是在邻居路由器的in方向配置的？ 
'''



import fonctions as f
import classes as c




def Community_local_pref(dict_output_file, dict_data):
    for AS in dict_data.keys():
        set_peer_group(dict_data[AS])
        for router in dict_data[AS].routers:
            if router.ASBR:
                for interface in router.interfaces_physiques:
                    if interface.neighbor_id:
                        for output_file_key in dict_output_file.keys():
                            if router.router_id == output_file_key:
                                with open(dict_output_file[output_file_key], 'a') as file:
                                    
                                    # router bgp dict_data[AS].as_number                                
                                    if interface.neighbor_as in dict_data[AS].customers.keys():
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
                                    
                                    elif interface.neighbor_as in dict_data[AS].peers.keys():
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
                                        
                                        # filtrer les routes pour que le voisin reçoit seulement les routes de customer
                                        for customer in dict_data[AS].customers.keys():
                                            '''
                                            route-map Advertize_customer permit 30
                                             match community {dict_data[AS].customer[customer]}
                                            neighbor interface.neighbor_address route-map Advertize_customer out
                                            '''
                                    
                                    elif interface.neighbor_as in dict_data[AS].providers.keys():                                      
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
                                        # filtrer les routes pour que le voisin reçoit seulement les routes de customer
                                        for customer in dict_data[AS].customers.keys():
                                            '''
                                            route-map Advertize_customer permit 30
                                             match community {dict_data[AS].customer[customer]}
                                            neighbor interface.neighbor_address route-map Advertize_customer out
                                            '''
    return


# creer un peer groupe pour envoyer les community a tous les routeur de meme AS 
def set_peer_group(AS):
    '''
    router bgp {AS.as_number}
    
    neighbor ibgp_peer_group peer-group
    neighbor ibgp_peer_group send-community
    '''
    for router in AS.routers:
        '''
        neighbor {router.loopback_address} peer-group ibgp_peer_group
        '''




