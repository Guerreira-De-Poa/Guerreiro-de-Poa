import pygame

class Item():
    def __init__(self, tipo, nome, atributos, equipado, personagem):
        self.tipo = tipo.lower()
        self.nome = nome
        self.atributos = atributos
        self.equipado = equipado
        self.personagem = personagem

        if self.equipado and self.tipo == 'armadura':
            personagem.armadura_equipada = self
        elif self.equipado and self.tipo == 'arma':
            personagem.arma_equipada = self

    def equipar(self):
        self.equipado = not self.equipado

        if self.equipado:
            for k,v in self.atributos.itens():
                self.personagem.k += v
        else:
            for k,v in self.atributos.itens():
                self.personagem.k -= v

    def utilizar(self):
        if self.tipo != 'consumivel':
            return
        valor = 0
        for atributo in self.atributos.values():
            valor = atributo
        self.personagem.HP += valor
        print(f"VOCE RECUPEROU {valor} HP!")

    def equipar(self):
        if self.tipo == 'arma' and self.personagem.arma_equipada:
            self.personagem.arma_equipada.equipado = False
            self.personagem.arma_equipada = self
            return
        elif self.tipo == 'armadura' and self.personagem.armadura_equipada:
            self.personagem.armadura_equipada.equipado = False
            self.personagem.armadura_equipada = self
            return

        if self.equipado == False:
            if self.tipo == 'arma' and self.personagem.arma_equipada:
                self.personagem.arma_equipada = self
                self.equipado = True
            elif self.tipo == 'armadura' and self.personagem.armadura_equipada:
                self.personagem.armadura_equipada = self
                self.equipado = True
        

    '''

    TIPOS:
    Armadura
    Arma
    Consumivel

    'ATRIBUTOS' DEVE SER UM DICIONÁRIO


    '''