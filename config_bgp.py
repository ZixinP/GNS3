
import protocols as p
import json


def etablir_ibgp(dict_data, dict_output_file):
    for AS in dict_data.keys():
        for self_router in dict_data[AS].router:
           
               # etablir la session ibgp entre les routeurs d'un AS
               for other_router in dict_data[AS].router:
                   if other_router.router_id != self_router.router_id:
                       for other_interface in other_router.interface_loopback:
                           other_router_loopback=other_interface.loopback_address.split("/")[0]
                           for output_file_key in dict_output_file.keys():
                               if self_router.router_id == output_file_key:
                                   
                                   # ajouter les consignes sur la connexion ibgp dans le fichier
                                   with open(dict_output_file[output_file_key], 'a') as file:
                                       p.ibgp_config(dict_output_file[output_file_key],dict_data[AS].as_number,self_router.router.id,self_router.interface_loopback[0],other_router_loopback)
    
    '''
    Essai d'utiliser le dict pour stocker les liens ibgp
    au lieu de iterer sur les routeurs et les interfaces
    celui-ci peut ameliorer la performance
    '''



def etablir_ebgp(dict_data, dict_output_file):
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
                                add_ipv6=interface.ipv6_address.split("/")[0]    # recuperer l'adresse ipv6 de l'interface
                              
                for ebgp_link in ebgp_links:
                    FLAG=True        # pour verifier si le lien existe deja dans la liste
                   
                    # si le lien existe déjà dans la liste
                    if ebgp_link[1]==link[1]:
                        if ebgp_link[5]==link[5]:
                            FLAG=False
                   
                    # si le lien existe déjà dans la liste mais dans l'autre sens，il faut completer l'adresse ipv6
                    elif ebgp_link[1]==link[5]:
                        if ebgp_link[5]==link[1]:
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
        as_number=link_complet[0]
        router_id=link_complet[1]
        router_interface=link_complet[2]
        neighbor_as=link_complet[4]
        neighbor_id=link_complet[5]
        neighbor_interface=link_complet[6]
        neighbor_inter_add=link_complet[7]
        for output_file_key in dict_output_file.keys():
            if router_id == output_file_key:
                with open(dict_output_file[output_file_key], 'a') as file:
                    p.ebgp_config(dict_output_file[output_file_key],as_number, router_id,router_interface,neighbor_as,neighbor_id,neighbor_interface,neighbor_inter_add)