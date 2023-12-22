class router():
   def __init__(self, interface, neighbor_router_id, neighbor_interface, neighbor_ip, neighbor_as_number):
         self.interface = interface
         self.neighbor_router_id = neighbor_router_id
         self.neighbor_interface = neighbor_interface
         self.neighbor_ip = neighbor_ip
         self.neighbor_as_number = neighbor_as_number


class interface():
   def __init__(self,igp_ip,loopback_ip,state,ebgp_state,ibgp_state):
         self.igp_ip = igp_ip
         self.loopback_ip = loopback_ip
         self.state = state
         self.ebgp_state = ebgp_state
         self.ibgp_state = ibgp_state
         
class AS():
      def __init__(self,as_number, igp_protocol, router, links):
         self.as_number = as_number
         self.igp_protocol = igp_protocol
         self.router = router
         self.links = links

      
