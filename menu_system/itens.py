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

    def utilizar(self):
        if self.tipo != 'consumivel':
            return
        valor = 0
        for atributo in self.atributos.values():
            valor = atributo
        self.personagem.HP += valor
        print(f"VOCE RECUPEROU {valor} HP!")

    def equipar(self):
        print(self.equipado)
        if self.equipado == False:
            if self.tipo == 'arma':
                if self.personagem.arma_equipada:
                    self.personagem.dano -= self.personagem.arma_equipada.atributos['dano']
                    self.personagem.arma_equipada.equipado = False
                self.personagem.arma_equipada = self
                self.equipado = True
                
            elif self.tipo == 'armadura':
                if self.personagem.armadura_equipada:
                    self.personagem.defesa -= self.personagem.armadura_equipada.atributos['defesa']
                    self.personagem.armadura_equipada.equipado = False
                self.personagem.armadura_equipada = self
                self.equipado = True
            for atributo,atributo_val in self.atributos.items():
                if atributo == 'dano':
                    print(self.personagem.dano)
                    self.personagem.dano += atributo_val
                    print(self.personagem.dano)

                elif atributo == 'HP':
                    self.personagem.MAX_HP += atributo_val

                elif atributo == 'defesa':
                    print(self.personagem.defesa)
                    self.personagem.defesa += atributo_val
                    print(self.personagem.defesa)

                elif atributo == 'velocidade':
                    self.personagem.max_stamina += atributo_val

                elif atributo == 'stamina':
                    self.personagem.velocidade_corrida += atributo_val
        else:
            if self.tipo == 'arma':
                self.personagem.arma_equipada = False
                self.equipado = False
            elif self.tipo == 'armadura':
                self.personagem.armadura_equipada = False
                self.equipado = False

            for atributo,atributo_val in self.atributos.items():
                if atributo == 'dano':
                    self.personagem.dano -= atributo_val

                elif atributo == 'HP':
                    self.personagem.MAX_HP -= atributo_val

                elif atributo == 'defesa':
                    print(self.personagem.defesa)
                    self.personagem.defesa -= atributo_val
                    print(self.personagem.defesa)

                elif atributo == 'velocidade':
                    self.personagem.max_stamina -= atributo_val

                elif atributo == 'stamina':
                    self.personagem.velocidade_corrida -= atributo_val
        print(self.equipado)

    '''

    TIPOS:
    Armadura
    Arma
    Consumivel

    'ATRIBUTOS' DEVE SER UM DICIONÁRIO


    '''