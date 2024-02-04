# PROJET GNS3 #
During this project, we ought to implement a software which can generate the GNS3 configurations for each router in its output_file.cfg, by providing a json file as input. 
The json file is required to have the basic information about the topology of the network，of which the structure is shown in intent.json in the folder projet_GNS3_code
## First part:
The programme is able to configure IGP for every interface in each AS, distribute averagely subnets and ipv6 addresses for each links existed. 
After that, IBGP and EBGP will be established.
## Second part:
The program configurate automatically BGP Polices accroding to the AS tags entered in intput json file, containing: tag routes with different communities, set local preference for each community tag, filter routes based on communities.
In the folder Telnet, you will find the example of its basic usage.

  
