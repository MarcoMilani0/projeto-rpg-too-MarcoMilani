from model.heroi import Heroi
from model.missao import Missao, Entrega, Cassino, Caçada
from model.inimigo import Inimigo
from model.enums import ClasseHeroi, TipoInimigo, StatusMissao

def main():
    heroi = Heroi("Aragorn", ClasseHeroi.GUERREIRO, 100, 100, 25, 10)
    print("Atributos antes da missão: ")
    print(heroi.exibir_dados())

    orc1 = Inimigo("Orc Guerreiro", TipoInimigo.ORC, 30, 30, 8, 2)
    goblin1 = Inimigo("Goblin Arqueiro", TipoInimigo.GOBLIN, 20, 20, 5, 1)

    missao_entrega = Entrega("Entrega Urgente", "Levar mantimentos para a vila vizinha", 80, 5)
    missao_cacada = Caçada("Caçada na Floresta", "Derrotar os monstros da região", 100, [orc1, goblin1])
    missao_cassino = Cassino("Aposta da Sorte", "Testar a sorte no cassino local", 50, 20)

    missoes = [missao_entrega, missao_cacada, missao_cassino]

    
    for missao in missoes:
        print(missao.exibir_dados())


    print("\nMissão de Entrega")
    print(missao_entrega.iniciar_missao())
    missao_entrega.concluir_missao(heroi)

    print("\nExecutando a Missão de Caçada")
    print(missao_cacada.iniciar_missao())
    missao_cacada.concluir_missao(heroi)

    print("\nExecutando a Missão do Cassino:")
    print(missao_cassino.iniciar_missao())
    missao_cassino.concluir_missao(heroi)

    print("Atributos depois da missão: ")
    print(heroi.exibir_dados()) 

    print("Teste operação inválida: ")
    missao_erro = Entrega("Missão Teste", "Testando transição proibida", 50, 3)
    try:
        missao_erro.status = StatusMissao.CONCLUIDA
    except (TypeError, ValueError) as erro:
        print(f"Erro capturado: {erro}")

main()