import os
dossier="/home/tangkeke/GNS3/projects/gns3ConfigNew/project-files/dynamips"
liste_dossiers=os.listdir(dossier)

for nom_dossier in liste_dossiers:
	if os.path.isdir(os.path.join(dossier,nom_dossier)):
		listes=os.listdir(dossier+"/"+f"{nom_dossier}"+"/configs")
		for liste in listes:
		 print(liste)
