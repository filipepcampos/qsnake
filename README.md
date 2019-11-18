# Projeto QSnake
### FPRO/MIEIC, 2019/20
### Filipe Pinto Campos up201905609@fe.up.pt
### 1MIEIC07 

#### Objetivo

1. Criar um clone do clássico Snake em Pygame
2. Implementar Q-Learning

#### Descrição

Réplica do clássico jogo Snake.
O objetivo do jogo é obter a maior quantidade possível de comida possível sem colidir contra uma parede ou contra a cauda do jogador.
Este jogo poderá ser jogado por um humano ou por um agente de A.I baseado em Q-Learning

#### UI

![UI](ui.png)

### Pacotes

- Pygame
- Numpy

### Tarefas

1. **MATRIZ NxN**
   1. Desenhar
   1. Teclas jogador
   1. Desenhar comida / colisão
   1. Criar "cauda" do jogador (lista)
1. **OPÇÃO JOGADOR CONTROLADO POR AI (Q-Learning)**
   1. Traduzir jogo em estados básicos
      * Criar uma matriz estados -> acções
   1. Atualizar essa matriz com a *reward* que o jogador recebeu
      * Para já, a snake continua a ser controlada pelo ser humano
      * Não aconteceu nada -> soma 0
      * Apanhou comida -> soma 1
      * Morreu -> soma -10
   1. Agir, para cada estado, com a ação com maior *reward*
1. **MODO JOGADOR-AI AO MESMO TEMPO**

------
18/11/2019
