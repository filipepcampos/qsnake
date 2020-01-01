<h1 align="center">&#128013 QSnake</h1>

-------
**FPRO/MIEIC, 2019/20**
**Filipe Pinto Campos up201905609@fe.up.pt**
**1MIEIC07**

---------

## :triangular_flag_on_post: Objetivo


1. Criar um clone do clássico Snake em Pygame
2. Implementar Q-Learning

## :page_facing_up: Descrição

Réplica do clássico jogo Snake.
O objetivo do jogo é obter a maior quantidade possível de comida possível sem colidir contra uma parede ou contra a cauda do jogador.
Este jogo poderá ser jogado por um humano ou por um agente de A.I baseado em Q-Learning

## :game_die: UI

<img src="/assets/ui.gif" width="300" height="300">

## :video_game: Controlos
**Movimento** - Setas direcionais e WASD
**Reiniciar Jogo** - Enter e Space
**Alterar velocidade de jogo em modo A.I** - Teclas 1, 2, 3 e 4


## :package: Pacotes

- Pygame
- Numpy

## :clipboard: Uso
Iniciar menu principal:
``` sh
python3 menu.py
```

Iniciar diretamente modo específico:
``` sh
python3 singleplayer.py
python3 ai.py
python3 twoplayer.py
python3 playerai.py
```

## :heavy_check_mark: Tarefas

1. ~~**MATRIZ NxN**~~
   1. ~~Desenhar~~
   1. ~~Teclas jogador~~
   1. ~~Desenhar comida / colisão~~
   1. ~~Criar "cauda" do jogador (lista)~~
1. ~~**OPÇÃO JOGADOR CONTROLADO POR AI (Q-Learning)**~~
   1. ~~Traduzir jogo em estados básicos~~
      *  ~~Criar uma matriz estados -> acções~~
   1. ~~Atualizar essa matriz com a *reward* que o jogador recebeu~~
      * ~~Para já, a snake continua a ser controlada pelo ser humano~~
      * ~~Não aconteceu nada -> soma 0~~
      * ~~Apanhou comida -> soma 1~~
      * ~~Morreu -> soma -10~~
   1. ~~Agir, para cada estado, com a ação com maior *reward*~~
1. ~~**MODO JOGADOR-AI AO MESMO TEMPO**~~

------
## Método Q-Learning:
Em cada estado do jogo é mapeado um Q-value para cada ação (Up, Down, Left, Right), quanto maior este valor for melhor a ação é. Estes valores são obtivos através de tentativa e erro de diversas ações sendo a cada uma associada uma recompensa que irá influenciar o Q-value

### Recompensas:
* Movimento: -0.1
* Comida: 200
* Morte: -100

A cada movimento que o jogador realiza está associado uma recompensa negativa de modo a minimizar o número de movimentos até à comida.

### Parâmetros:
1. **Total**: Número total de jogos a ser executados
1. **Epsilon**: Fator decisor entre realizar uma ação aleatória (para explorar diferentes estados) e realizar a melhor ação conhecida
1. **Alpha**: Taxa de aprendizagem, define o impacto de cada iteração sobre os Q-values
1. **Gamma**: Importância de recompensa a longo prazo

### Estado:
Cada estado é inicialmente obtido como um número binário de 10 bits, e posteriormente convertido num número decimal
**0000_0000_00** a **1111_1111_11** (0 a 1023 decimal)
Os grupos de bits correspondem respetivamente ao Perigo, Comida e Direção

**Perigo**
<table><tr><td>
Corresponde a 4 valores booleanos associados ao perigo nas posições adjacentes ao jogador (cima, baixo, esquerda, direita)
</td></tr></table>

**Comida**
<table><tr><td>
Corresponde à posição relativa da comida em relação ao jogador. (a cima, a baixo, à esquerda, à direita). A informação parece redundante pois a comida não poderá se encontrar simultâneamente a cima e a baixo do jogador mas, no entanto, permite centrar o jogador em relação à comida, se não estiver a cima nem a baixo, o jogador está centrado
</td></tr></table>


**Direção**
<table><tr><td>
Número de 2 bits correspondente à direção do movimento do jogador. <code>00: cima</code>, <code>01: baixo</code>, <code>10: esquerda</code>, <code>11: direita</code>
</td></tr></table>




### Funcionalidade:
1. No início de cada iteração é associado associado um estado à situação atual do jogo. 
2. Em seguida é escolhida uma ação. Esta ação poderá ser uma ação aleatória se (um número aleatório entre 0 e 1 < epsilon) ou a melhor ação associada ao estado atual
3. O jogador movimenta-se e dependendo de o que acontecer será associado uma recompensa
4. É calculado o novo Q-Value para o estado atual, para a ação tomada através da seguinte fórmula:
![Q-Learning formula](/assets/formula.png)
5. Repetir até terminar o número total de jogos

------
18/11/2019
