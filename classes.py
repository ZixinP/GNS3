class router():
   def __init__(self,as_number, router_id):
         self.router_id = router_id
         self.interfaces = []
         self.as_number = as_number
         self.neighbors = []
   
   def add_neighbor(self, neighborrouter_id, neighbor_interface):     # ajouter un voisin dans la liste 
         self.neighbors.append([neighborrouter_id, neighbor_interface])


class interface():
   def __init__(self, protocol):
         self.loopback=False
         self.ipv6_address = None
         self.loopback_address = None
         self.neighbor_id = None
         self.neighbor_interface = None
         self.protocol = protocol
         
         
class AS():
      def __init__(self,as_number, igp_protocol, ip_range,ip_mask):
         self.as_number = as_number
         self.igp_protocol = igp_protocol
         self.router = []
         self.links = []
         self.iprange = ip_range
         self.ipmask = ip_mask
         
      def linkscollect(self):     # collecter les liens entre les routeurs de l'AS
            liste_links = []
            for router in self.router:
                  for neighbor in router.neighbors:
                        for link in liste_links:
                             FLAG=True
                             
                             # si le lien existe déjà dans la liste
                             if link[0]==router.router_id :                   
                                FLAG=False
                             
                             # si le lien existe déjà dans la liste mais il manque le nom de l'interface de voisin
                             elif link[2]==router.router_id:
                                FLAG=False
                                if link[3]==None:
                                    link[3]=neighbor[1]
                        # si le lien n'existe pas dans la liste, on l'ajoute 
                        if FLAG:
                              liste_links.append([router.router_id,neighbor[1],neighbor[0],None])
            
            self.links=liste_links
      
                 
                          
                              
                        
            
         
         