import protocols as p
import fonctions as f
import config_bgp as bgp
import config_ipv6 as ipv6
import bgp_police as police
import write as w

dict_data = {}  # dictionnaire pour stocker tous les objets créés
dict_output_file = {}  # dictionnaire pour stocker les fichier de sortie 
dict_config_dict = {}  #  dictionnaire pour stocker les dictionnaires de configuration de chaque routeur

def main(intent_file):
    network_intents = f.open_file(intent_file)    
    ipv6.initialisation(network_intents, dict_data, dict_output_file,dict_config_dict)    
    ipv6.generate_cisco_config_physique(dict_data,dict_config_dict)  
    ipv6.generate_cisco_config_loopback(network_intents, dict_data, dict_config_dict)    
    p.bgp_init(dict_config_dict,dict_data)
    bgp.etablir_ibgp(dict_data, dict_config_dict)    
    bgp.etablir_ebgp(dict_data, dict_config_dict)
    p.network(dict_config_dict,dict_data)   
    police.Community_local_pref(dict_data, dict_config_dict) 
    f.igp_code(dict_data, dict_config_dict)
    w.write_in_config(dict_output_file,dict_config_dict)    
    
    print(dict_output_file)
    return dict_output_file
    
main('intent.json')