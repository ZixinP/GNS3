import json
import ipaddress
import os
import time

json_file=open("gnsConf.json")#nom de fichier ".json"
data=json.load(json_file)
start_subnet=ipaddress.IPv6Network(data['IPv6_range']['Physical']['start'])
#print(data['IPv6_range']['Physical']['start'])
#start_subnet=ipaddress.IPv6Network('2001:100:100:1::/64')
#end_subnet=ipaddress.IPv6Network('2001:200:100:255::/64')
end_subnet=ipaddress.IPv6Network(data['IPv6_range']['Physical']['end'])
#stockIP=[{'r1':[{'inter1':'ip@'},{'inter2':'ip@'}]},]
stockIPs=[]

	
subnets = ipaddress.summarize_address_range(start_subnet.network_address, end_subnet.network_address)
i=0
#subnet=next(subnets)

#distribuer les @ aux routeurs

for router in data['routers']:
	stockIPs+=[{router['name']:[] }]
for link in data['links']:
	#for router in data['routers']:
	for stockIP in stockIPs:
		#print(link['source']['router'])
		for key in stockIP:
			#print(key)
			if key==link['source']['router'] :
				subnet1=next(subnets)
				address1=subnet1[1]
				address2=subnet1[2]
				#print(subnet1)
				#print(address1)
				#print(address2)
				#print(stockIP.keys())
				#print(stockIP[key])
				
				stockIP[key]+=[{link['source']['interface']:str(address1)}]
				for stock1 in stockIPs:
					for key1 in stock1:
						if key1==link['destination']['router']:
							stock1[key1]+=[{link['destination']['interface']:str(address2)}]
				
				
				#stockIP[key]+=[{link['destination']['interface']:str(address2)}]
			
	
#print (stockIPs)

NumOSPF=1
NumLoopback=1
stockLoopbackIP=[]
NumBgp=1
#distribution les @ loopback
for router in data['routers']:
	stockLoopbackIP+=[{router['name']:str(NumLoopback)+"::"+str(NumLoopback)}]
	NumLoopback+=1


	

for router in data ["routers"]:
	with open(f"{ router['name']}_startup-config.cfg","w") as f:
		f.write("!\n")
		#the head unchangeable part
		f.write("!\n")
		f.write("!\n")
		f.write("version 15.2\n")
		f.write("service timestamps debug datetime msec\n")
		f.write("service timestamps log datetime msec\n")
		f.write("!\n")
		f.write(f"hostname {router['name']}\n")
		f.write("!\n")
		f.write("boot-start-marker\n")
		f.write("boot-end-marker\n")
		f.write("!\n")
		f.write("!\n")
		f.write("no aaa new-model\n")
		f.write("no ip icmp rate-limit unreachable\n")
		f.write("ip cef\n")
		f.write("!\n")
		f.write("!\n")
		f.write("no ip domain lookup\n")
		f.write("ipv6 unicast-routing\n")
		f.write("ipv6 cef\n")
		f.write("!\n")
		f.write("!\n")
		f.write("multilink bundle-name authenticated\n")
		f.write("!\n")
		f.write("ip tcp synwait-time 5\n")
		f.write("! \n")
		f.write("!\n")
		
		f.write("interface Loopback0\n")
		f.write("no ip address\n")
		
		for loopbackAdd in stockLoopbackIP:
			for key in loopbackAdd:
				if key==router['name']:
					f.write("ipv6 address "+loopbackAdd[key]+"/64\n")
					f.write("ipv6 enable\n")
					if router['protocole']=="OSPF":
						f.write("ipv6 ospf 1 area 0\n")
					if router['protocole']=="RIP":
						f.write("ipv6 rip 1 enable\n")
					f.write("!\n")
					
		
		
		
		
		

		#accéder dans un interface physique
		for link in data['links']:
			if link['source']['router']==router['name'] or link['destination']['router']==router['name']:
				if link['source']['router']==router['name'] :
					f.write(f"interface {link['source']['interface']}\n")
					f.write(f"no ip address\n")
					f.write(f"negotiation auto\n")
					f.write(f"duplex full\n")
					#configurer l'@ pour chaque interface
					for stockIP in stockIPs:
						for key in stockIP:
							if key==router['name']:
								for interface in stockIP[key]:
									for key1 in interface:
									#print(key1)
									#print (link['source']['router'])
										if key1==link['source']['interface']:
										#print('hello')
											f.write(f"ipv6 address {interface[key1]}/64\n")
											
					
				else:
					f.write(f"interface {link['destination']['interface']}\n")
					f.write(f"no ip address\n")
					f.write(f"negotiation auto\n")
					f.write(f"duplex full\n")
				#f.write(f"ipv6 address ...\n")
					for stockIP in stockIPs:
						for key in stockIP:
							if key==router['name']:
								for interface in stockIP[key]:
									for key1 in interface:
									#print(key1)
									#print (link['source']['router'])
										if key1==link['destination']['interface']:
										#print('hello')
											f.write(f"ipv6 address {interface[key1]}/64\n")
											
				#calculIP(link,f)
				f.write(f"ipv6 enable \n")
				if (router['protocole']=="RIP"):
					f.write("ipv6 rip 1 enable\n")
				if (router['protocole']=="OSPF"):
					f.write("ipv6 ospf 1 area 0\n")
					f.write("!\n")
					f.write("router ospf 1 \n")
					f.write("!\n")
					
				f.write("!\n")
		#protocole BGP
		f.write(f"router bgp {router['AS']}\n")
		
		
		
		#####################################################################################
		f.write("bgp router-id "+str(NumBgp)+"."+str(NumBgp)+"."+str(NumBgp)+"."+str(NumBgp)+"\n")
		#####################################################################################
		NumBgp+=1
		
		f.write("bgp log-neighbor-changes\n")
		f.write("no bgp default ipv4-unicast\n")		
		for router1 in data['routers']:
			if router1['AS']==router['AS'] and router1['name']!=router['name']:
				#f.write("neighbor "+str(NumLoopback)+"::"+str(NumLoopback)+"\n")
				for loopbackIP in stockLoopbackIP:
					for key in loopbackIP:
						if router1['name']==key:
							f.write("neighbor "+loopbackIP[key]+" remote-as "+router['AS']+"\n")
							f.write("neighbor "+loopbackIP[key]+" update-source loopback0\n")
		#configuration d'EBGP
		if router['BorderRouter']==True:
			for link in data['links']:
				if link['source']['router']==router['name']:
					routerNeighbor=link['destination']['router']
					interfaceNeighbor=link['destination']['interface']
					for IP in stockIPs:
						for key in IP:
							if key==routerNeighbor:
								for inter in IP[key]:
									for key1 in inter:
										if key1==interfaceNeighbor:
											#inter[key1]
											for router1 in data['routers']:
												#print(key1)
												if router1['name']==routerNeighbor:
													#router1['AS']
													
													f.write("neighbor "+inter[key1]+" remote-as "+router1['AS']+"\n")
				elif link['destination']['router']==router['name']:
					routerNeighbor=link['source']['router']
					interfaceNeighbor=link['source']['interface']
					for IP in stockIPs:
						for key in IP:
							if key==routerNeighbor:
								for inter in IP[key]:
									for key1 in inter:
										if key1==interfaceNeighbor:
											#inter[key1]
											for router1 in data['routers']:
												#print(key1)
												if router1['name']==routerNeighbor:
													#router1['AS']
													
													f.write("neighbor "+inter[key1]+" remote-as "+router1['AS']+"\n")
				
				
				
				
				
		
		f.write("!\n")
		f.write("address-family ipv4\n")
		f.write("exit-address-family\n")
		f.write("!\n")
		f.write("address-family ipv6\n")
		f.write("address-family ipv6\n")
		for IP in stockIPs:
			for key in IP:
				if key==router['name']:
					for inter in IP[key]:
						for key1 in inter:
							f.write(" network "+inter[key1][:-1]+"/64\n")	
		f.write("!\n")
		for router1 in data['routers']:
			if router1['AS']==router['AS'] and router1['name']!=router['name']:
				#f.write("neighbor "+str(NumLoopback)+"::"+str(NumLoopback)+"\n")
				for loopbackIP in stockLoopbackIP:
					for key in loopbackIP:
						if router1['name']==key:
							f.write("neighbor "+loopbackIP[key]+" activate "+"\n")
		if router['BorderRouter']==True:
			for link in data['links']:
				if link['source']['router']==router['name']:
					routerNeighbor=link['destination']['router']
					interfaceNeighbor=link['destination']['interface']
					for IP in stockIPs:
						for key in IP:
							if key==routerNeighbor:
								for inter in IP[key]:
									for key1 in inter:
										if key1==interfaceNeighbor:
											#print(inter[key1])					
											f.write("neighbor "+inter[key1]+" activate"+"\n")
				elif link['destination']['router']==router['name']:
					routerNeighbor=link['source']['router']
					interfaceNeighbor=link['source']['interface']
					for IP in stockIPs:
						for key in IP:
							if key==routerNeighbor:
								for inter in IP[key]:
									for key1 in inter:
										if key1==interfaceNeighbor:
											#print(inter[key1])					
											f.write("neighbor "+inter[key1]+" activate"+"\n")			
							
							
							
							
							
		f.write("exit-address-family\n")
		f.write("!\n")
		f.write("ip forward-protocole nd\n")
		f.write("!\n")
		f.write("!\n")
		f.write("no ip http server\n")
		f.write("no ip http secure-server\n")
		
		
		f.write("!\n")
		#protocole IGP
		if (router['protocole']=="RIP"):
			f.write("ipv6 router rip 1\n")
			f.write("redistribute connected\n")
		if (router['protocole']=="OSPF"):
			f.write(f"!\n")
			f.write("ipv6 router ospf 1 \n")					
			f.write("router-id "+ str(NumOSPF)+"."+str(NumOSPF)+"."+str(NumOSPF)+"."+str(NumOSPF)+"\n")	
			NumOSPF+=1
		f.write(f"!\n")
		
		#à ajouter des infos de BGP
		
		
	
				
				#the end unchangeable part
		f.write("!\n")
		f.write("control-plane\n")
		f.write("!\n")
		f.write("!\n")
		f.write("line con 0\n")
		f.write(" exec-timeout 0 0\n")
		f.write(" privilege level 15\n")
		f.write(" logging synchronous\n")
		f.write(" stopbits 1\n")
		f.write("line aux 0\n")
		f.write(" exec-timeout 0 0\n")
		f.write(" privilege level 15\n")
		f.write(" logging synchronous\n")
		f.write(" stopbits 1\n")
		f.write("line vty 0 4\n")
		f.write(" login\n")
		f.write("!\n")
		f.write("!\n")
		f.write("end\n")
		
		#déplacer le fichier
		dossier="/home/tangkeke/GNS3/projects/gns3ConfigTest/project-files/dynamips"#répertoire de projet GNS3 
		liste_dossiers=os.listdir(dossier)
		#time.sleep(5)
		for nom_dossier in liste_dossiers:
			
			if os.path.isdir(os.path.join(dossier,nom_dossier)):
				listes=os.listdir(dossier+"/"+f"{nom_dossier}"+"/configs")#répertoire de dossier "configs"
				for liste in listes:
		 			#print(f"{router['name']}_startup-config.cfg")
		 			if liste==f"{router['name']}_startup-config.cfg":
		 				path=os.replace("/home/tangkeke/Documents/GNS/"+f"{ router['name']}_startup-config.cfg",dossier+"/"+f"{nom_dossier}"+"/configs/"+f"{router['name']}_startup-config.cfg")#le premier élément est la répertoire de script Python, le deuxième est la répertoire de ".cfg"
