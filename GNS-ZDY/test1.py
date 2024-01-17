#Importation des modules necessaires
import sys
import telnetlib

#Parametrage des variables
HOST1 = "localhost:5014"
HOST2 = "localhost:5015"

#Ouverture de la connexion
tn1 = telnetlib.Telnet("localhost",5014)
tn2 = telnetlib.Telnet("localhost",5015)

#Configuration de l'adresse IPv6
tn1.write(b"\r\n")
tn1.write(b"enable\r\n") 
tn1.write(b"conf t\r\n")
tn1.write(b"ipv6 unicast-routing\r\n")
tn1.write(b"interface fa0/0\r\n")
tn1.write(b"ipv6 enable\r\n")
tn1.write(b"ipv6 address 2001:1234:1234::1/64\r\n")
tn1.write(b"no shutdown\r\n")
tn1.write(b"end\r\n") 

tn2.write(b"\r\n") 
tn2.write(b"enable\r\n")
tn2.write(b"conf t\r\n")
tn2.write(b"ipv6 unicast-routing\r\n")
tn2.write(b"interface fa0/0\r\n")
tn2.write(b"ipv6 enable\r\n")
tn2.write(b"ipv6 address 2001:1234:1234::2/64\r\n")
tn2.write(b"no shutdown\r\n")
tn2.write(b"end\r\n") 

print(tn1.read_all())
print(tn2.read_all())
#Fermeture de la connexion
tn1.close()
tn2.close()
