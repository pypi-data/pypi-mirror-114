#coding:utf-8

class Ml:
    def __init__(self, name):
        self.name = name
        print("objet créé")
    
    def __str__(self):
        return f"Nom de l'objet: {self.name}"

    def rename(self):
        self.name = "rename"
        print(self.name)
    