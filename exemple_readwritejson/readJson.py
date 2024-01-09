import json
with open("books.json")as json_file:
    data=json.load(json_file)
    for book in data["books"]:
        print(book["title"],"by",book["author"],"published in",book["published"])