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