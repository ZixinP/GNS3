class router():
   def __init__(self,as_number, router_id):
         self.as_number = as_number
         self.router_id = router_id
         self.interfaces_physiques = []
         self.interface_loopback = []
         self.neighbors = []
         self.ASBR=False
         
   def add_neighbor(self, neighborrouter_id, neighbor_interface):     # ajouter un voisin dans la liste 
         self.neighbors.append([neighborrouter_id, neighbor_interface])


class interface():
   def __init__(self, router_id,name,protocol):
         self.router_id = router_id
         self.name = name
         self.loopback=False
         self.ipv6_address = None
         self.loopback_address = None
         self.neighbor_as = None
         self.neighbor_id = None
         self.neighbor_address = None
         self.protocol = protocol
         
         
class AS():
      def __init__(self,as_number, igp_protocol, ip_range_reseau,ip_range_prefix):
         self.as_number = as_number
         self.igp_protocol = igp_protocol
         self.router = []
         self.links = []     # [router_id,router_interface,neighbor_id,neighbor_interface]
         self.iprange_reseau = ip_range_reseau
         self.iprange_prefix = ip_range_prefix
         self.subnets={}
         self.provider={}
         self.customers={}
         self.peers={}
      
      def linkscollect(self):     # collecter les liens entre les routeurs de l'AS
            liste_links = []
            for router in self.router:
                  for neighbor in router.neighbors:
                        FLAG=True
                        
                        for link in liste_links:
                          
                             # si le lien existe déjà dans la liste
                             if link[0]==router.router_id :                   
                                    if link[2]==neighbor[0]:
                                          FLAG=False
                                          
                             # si le lien existe déjà dans la liste mais dans l'autre sens
                             if link[0]==neighbor[0] :
                                    if link[2]==router.router_id:
                                          FLAG=False
                                          if link[3]==None:        # si l'interface de voisin n'est pas encore declarée
                                                link[3]=neighbor[1]
                        
                        # si le lien n'existe pas dans la liste, on l'ajoute 
                        if FLAG:
                              liste_links.append([router.router_id,neighbor[1],neighbor[0],None])
                              router.ASBR=True
                              
                              # ajouter l'interface de voisin dans l'objet interface
                              for interface in router.interfaces_physiques:
                                    if interface.name == neighbor[1]:
                                          interface.neighbor_id = neighbor[0]
                                    
                              
            self.links=liste_links
      
                 
                          
                              
                        
            
         
         