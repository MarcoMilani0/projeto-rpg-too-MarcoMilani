# Com o avançar do jogo as recompensas das missoes são aumentadas para balancear o jogo 
# O status vai mudar com o avançar do jogo
# Nome e descrição são fixos
import random
from model.enums import StatusMissao

class Missao:
    def __init__(self, nome, descricao, recompensa):
        self.__nome = nome
        self.__descricao = descricao
        self.__recompensa = recompensa
        self.__status = StatusMissao.PENDENTE

    @property
    def nome(self):
        return self.__nome

    @property
    def descricao(self):
        return self.__descricao

    @property
    def recompensa(self):
        return self.__recompensa

    @recompensa.setter 
    def recompensa(self, valor):
        if valor < 0:
            print("Recompensa de missão não pode ser negativa")
        else:
            self.__recompensa = valor

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        if not isinstance(valor, StatusMissao):
            raise TypeError('Tipo precisa ser um StatusMissao')

        if self.__status == StatusMissao.PENDENTE and valor != StatusMissao.EM_ANDAMENTO:
            raise ValueError("Para sair de pendente precisa ser em andamento")

        if self.__status == StatusMissao.EM_ANDAMENTO and valor != StatusMissao.CONCLUIDA:
            raise ValueError("Para sair de em andamento precisa ser em concluida")

        if self.__status == StatusMissao.CONCLUIDA:
            raise ValueError("Missão já concluída, não é possível alterar o status")

        self.__status = valor

    def iniciar_missao(self):
        if self.status == StatusMissao.PENDENTE:
            self.status = StatusMissao.EM_ANDAMENTO
            return f"A missão {self.nome} começou! O objetivo é {self.descricao}."
        else:
            return f'A missão {self.nome} já foi iniciada!!!'

    def exibir_dados(self):
        msg = f'''
[{self.__class__.__name__}]
Nome: {self.nome}
Descrição: {self.descricao}
Recompensa: {self.recompensa}
Status: {self.status.value}
'''
        return msg

    def calcular_recompensa(self):
        if self.status is not StatusMissao.CONCLUIDA:
            return 0
        return self.recompensa

    def __str__(self):
        return f'missão [{self.__class__.__name__}]: {self.nome} | status: {self.status.value}'

    def concluir_missao(self, heroi):
        if self.status == StatusMissao.PENDENTE:
            self.status = StatusMissao.EM_ANDAMENTO
        if self.status == StatusMissao.EM_ANDAMENTO:
            self.status = StatusMissao.CONCLUIDA

        xp_recompensa = self.calcular_recompensa()
        heroi.ganhar_experiencia(xp_recompensa)


class Entrega(Missao):
    # O tempo da missão varia a recompensa: entregas mais longas (maior
    # duração) aumentam a recompensa em XP. Duração é o atributo próprio
    # que pode mudar após a criação (ajuste de prazo), dentro de um limite.

    def __init__(self, nome, descricao, recompensa, tempo):
        super().__init__(nome, descricao, recompensa)
        self.__duracao = tempo

    @property
    def duracao(self):
        return self.__duracao

    @duracao.setter
    def duracao(self, valor):
        if valor <= 0:
            raise ValueError("A duração da missão não pode ser menor ou igual a 0")
        elif valor > 10:
            print("A duração não pode ultrapassar 10 horas, valor ajustado para 10 horas")
            self.__duracao = 10
        else:
            self.__duracao = valor

    def calcular_recompensa(self):
        base = super().calcular_recompensa()
        if base == 0:
            return 0
        return base + 10 * self.duracao


class Cassino(Missao):
    # Aposta de XP pode mudar antes de apostar; sorte começa em 50 e cai a
    # cada vitória. Resultado da última aposta (ganho ou perda) é o que
    # soma na recompensa final, premiando quem sai no lucro do cassino.

    def __init__(self, nome, descricao, recompensa, xpApostado):
        super().__init__(nome, descricao, recompensa)
        self.__aposta = xpApostado
        self.__sorte = 50
        self.__resultado_aposta = 0

    @property
    def aposta(self):
        return self.__aposta

    @property
    def sorte(self):
        return self.__sorte

    @property
    def resultado_aposta(self):
        return self.__resultado_aposta

    @aposta.setter
    def aposta(self, valor):
        if valor <= 0:
            raise ValueError("O xp apostado precisa ser maior que 0")
        else:
            self.__aposta = valor

    @sorte.setter
    def sorte(self, valor):
        if valor <= 0:
            self.__sorte = 0
        else:
            self.__sorte = valor

    def apostar(self, personagem):
        numero = random.randint(0, 100)

        if numero > self.sorte:
            ganho = self.aposta * 1.5
            self.sorte -= 2
            self.__resultado_aposta = ganho
            print(f'Ganhou: {ganho}, e sua sorte foi diminuída')
        else:
            self.sorte = 50
            self.__resultado_aposta = -self.aposta
            print('Perdeu, mas sua sorte foi recuperada')

        return self.__resultado_aposta

    def concluir_missao(self, heroi):
        if self.status == StatusMissao.PENDENTE:
            self.status = StatusMissao.EM_ANDAMENTO

        if self.status == StatusMissao.EM_ANDAMENTO:
            self.apostar(heroi)              # só calcula o resultado, não mexe no XP ainda
            super().concluir_missao(heroi) 


class Caçada(Missao):
    # Quantidade de inimigos na caçada determina o bônus de recompensa:
    # cada inimigo enfrentado paga 10 de XP extra ao concluir a missão.

    def __init__(self, nome, descricao, recompensa, inimigos):
        super().__init__(nome, descricao, recompensa)
        self.__inimigos = inimigos
        self.__xp_acumulado = 0
        self.__xp_base = 10
        self.__incremento_xp = 5

    @property
    def inimigos(self):
        return self.__inimigos

    @property
    def quantidade_inimigos(self):
        return len(self.__inimigos)

    @property
    def xp_acumulado(self):
        return self.__xp_acumulado

    def cacar(self, personagem):
        xp_desta_vitoria = self.__xp_base

        for inimigo in self.__inimigos:
            print(f'--- {personagem.nome} encontrou {inimigo.nome}! ---')

            while personagem.esta_vivo() and inimigo.esta_vivo():
                personagem.atacar(inimigo)
                if inimigo.esta_vivo():
                    inimigo.atacar(personagem)

            if not personagem.esta_vivo():
                print(f'{personagem.nome} foi derrotado durante a caçada!')
                break

            print(f'{inimigo.nome} foi derrotado! {personagem.nome} ganhou {xp_desta_vitoria} de XP.')
            personagem.ganhar_experiencia(xp_desta_vitoria)
            self.__xp_acumulado += xp_desta_vitoria
            xp_desta_vitoria += self.__incremento_xp

        if personagem.esta_vivo():
            print(f'{personagem.nome} sobreviveu à caçada inteira!')

    def calcular_recompensa(self):
        base = super().calcular_recompensa()
        if base == 0:
            return 0
        return base + 10 * self.quantidade_inimigos

    def concluir_missao(self, heroi):
        if self.status == StatusMissao.PENDENTE:
            self.status = StatusMissao.EM_ANDAMENTO

        if self.status == StatusMissao.EM_ANDAMENTO:
            self.cacar(heroi)
            super().concluir_missao(heroi)