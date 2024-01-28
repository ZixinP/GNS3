import json
import protocols as p
import classes as c
import fonctions as f
import config_bgp as bgp
import config_ipv6 as ipv6

dict_data = {}  # dictionnaire pour stocker tous les objets créés
dict_output_file = {}  # dictionnaire pour stocker les fichiers de consignes de configuration des routeurs différents

def main(intent_file):
    
    network_intents = f.open_file(intent_file)    # charger le fichier JSON et récupérer la liste des intents
    ipv6.initialisation(network_intents, dict_data, dict_output_file)    # Initialiser les objets AS, router, interface et les ajouter aux dictionnaires dict_data
    ipv6.generate_cisco_config_physique(dict_data, dict_output_file)    # créer les objets et générer les consignes de configuration IPv6
    ipv6.generate_cisco_config_loopback(network_intents, dict_data, dict_output_file)    # créer les objets et générer les consignes de configuration IPv6   
    bgp.etablir_ibgp(dict_data, dict_output_file)    # créer les objets et générer les consignes de configuration iBGP
    bgp.etablir_ebgp(dict_data, dict_output_file)    # créer les objets et générer les consignes de configuration eBGP
    
    print(dict_output_file)
    return dict_output_file
    
main('intent.json')