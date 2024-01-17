import json
with open("books.json")as json_file:
    data=json.load(json_file)
    for book in data["books"]:
        fichier=open((book["title"]+".cfg"),"w")
        fichier.write(book["author"])
        fichier.write(str(book["published"]))
