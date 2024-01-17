import ipaddress

# Define the range of subnet addresses
start_subnet = ipaddress.IPv6Network('2001:100:100:1::')
end_subnet = ipaddress.IPv6Network('2001:100:100:30::')

# Define the links
links = [
	{
	'R1':{'f0/0':''},
	'R2':{'f0/0':''}
	}, 
	]
	

# Iterate through the links and assign the first available subnet address to one interface on one router
subnets = ipaddress.summarize_address_range(start_subnet.network_address, end_subnet.network_address)

i=0
while i < len(links):
	subnet1 = next(subnets)
	n = 1
	for router in links[i].values():
		interface_address = str(subnet1[i]) + str(n)
		n+=1
		for inter in router.values():
			inter = interface_address
			print(inter)
			print(f'{router}  has the address {interface_address}')
	i+=1


