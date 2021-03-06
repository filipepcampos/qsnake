<h1 align="center" style="font-size=60px;">
   &#128013 QSnake
   <br>
   <br>
</h1>


**FPRO/MIEIC, 2019/20**

**Filipe Pinto Campos up201905609@fe.up.pt**

**1MIEIC07**

---------

## :triangular_flag_on_post: Objetivo


1. Criar um clone do clássico Snake em Pygame
2. Implementar Q-Learning

## :page_facing_up: Descrição

Réplica do clássico jogo Snake.
O objetivo do jogo é obter a maior quantidade de comida possível sem colidir contra uma parede ou contra a cauda do jogador.
Este jogo poderá ser jogado por um humano ou por um agente de A.I baseado em Q-Learning

## :game_die: UI

<img src="/assets/ui.gif" width="300" height="300">

## :video_game: Controlos
* **Movimento** - Setas direcionais e WASD
* **Reiniciar Jogo** - Enter e Space
* **Alterar velocidade de jogo em modo A.I** - Teclas 1, 2, 3 e 4
* **Regressar ao menu** - Esc


## :package: Pacotes

- Pygame
- Numpy

## :clipboard: Uso
Iniciar menu principal:
``` sh
$ python3 qsnake.py
```

Iniciar diretamente modo específico:
``` sh
$ python3 singleplayer.py
$ python3 ai.py
$ python3 twoplayer.py
$ python3 playerai.py
```

## :heavy_check_mark: Tarefas
1. [x] **MATRIZ NxN**
   1. Desenhar
   1. Registar teclas do jogador
   1. Desenhar comida / colisão
   1. Criar "cauda" do jogador (lista)
1. [x] **OPÇÃO JOGADOR CONTROLADO POR AI (Q-Learning)**
   1. Traduzir jogo em estados básicos
      *  Criar uma matriz estados -> ações
   1. Atualizar essa matriz com a *reward* que o jogador recebeu
      * Para já, a snake continua a ser controlada pelo ser humano
      * Não aconteceu nada -> soma -0.01
      * Apanhou comida -> soma 10
      * Morreu -> soma -100
   1. Agir, para cada estado, com a ação com maior *reward*
1. [x] **MODO JOGADOR-AI AO MESMO TEMPO**

------
## :books: Método Q-Learning:
Em cada estado do jogo é mapeado um Q-value para cada ação (Up, Down, Left, Right), quanto maior este valor for melhor a ação é. Estes valores são obtidos através de tentativa e erro de diversas ações sendo a cada uma associada uma recompensa que irá influenciar o Q-value

**Q-Table**

|Estado | :arrow_up: | :arrow_down: | :arrow_left: | :arrow_right: |
|--- | -----------| ------------ | ------------ | ------------- |
| 0 | 0.322117 | 0.100763 | 0.040893 | 0.100597 |
| 1 |0.036582 |	0.000000 |	0.000000 |	0.136924|
| 2 | 0.121900 | 0.000000 | 0.000000 | 0.000000 | 
| 3 | 0.000000 | 0.000000 | 0.000000 | 0.179133 |
| 4 | 0.363259 | 0.369609 | 0.414382 | 0.773585 |
| ...| ... | ... | ... | ...
| 1022 | 0.000000 | 0.000000 | 0.000000 | 0.000000
------------------

### :watermelon: Recompensas:
* Movimento: -0.01
* Comida: 10
* Morte: -100

A cada movimento que o jogador realiza está associado uma recompensa negativa de modo a minimizar o número de movimentos até à comida.

### :floppy_disk: Parâmetros:
1. **Total**: número total de jogos a ser executados
1. **Epsilon** : fator decisor entre realizar uma ação aleatória (para explorar diferentes estados) e realizar a melhor ação conhecida
1. **Alpha** : taxa de aprendizagem, define o impacto de cada iteração sobre os Q-values
1. **Gamma** : importância de recompensa a longo prazo

### :camera: Estado:
Cada estado é inicialmente obtido como um número binário de 10 bits, e posteriormente convertido num número decimal
**0000_0000_00** a **1111_1111_11** (0 a 1023 decimal)
Os grupos de bits correspondem respetivamente ao Perigo, Comida e Direção

**Perigo**
<table><tr><td>
Corresponde a 4 valores booleanos associados ao perigo nas posições adjacentes ao jogador (cima, baixo, esquerda, direita)
</td></tr></table>

**Comida**
<table><tr><td>
Corresponde à posição relativa da comida em relação ao jogador. (cima, baixo, esquerda, direita).
</td></tr></table>


**Direção**
<table><tr><td>
Número de 2 bits correspondente à direção do movimento do jogador. <code>00: cima</code>, <code>01: baixo</code>, <code>10: esquerda</code>, <code>11: direita</code>
</td></tr></table>




### :computer: Funcionamento:
1. No início de cada iteração é associado um estado à situação atual do jogo. 
2. Em seguida é escolhida uma ação. Esta ação poderá ser uma ação aleatória se (um número aleatório entre 0 e 1 < epsilon) ou a melhor ação associada ao estado atual
3. O jogador movimenta-se e dependendo de o que acontecer será associado uma recompensa
4. É calculado o novo Q-Value para o estado anterior ao movimento, para a ação tomada através da seguinte fórmula:

![formula](./assets/formula.png)


5. Repetir até terminar o número total de jogos

------
18/11/2019
