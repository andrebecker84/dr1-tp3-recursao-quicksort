<sub>[⬅ README](../../README.md) · [Notebook](../../andre_becker_DR1_TP3.ipynb) · [Relatório](../RELATORIO_TP3.md) · [Rubrica](rubrica-DR1-TP3.md)</sub>

# 📄 Enunciado · DR1-TP3 (Teste de Performance)

| | |
|---|---|
| **Disciplina** | Velocidade e Qualidade com Estruturas de Dados e Algoritmos |
| **Trimestre** | 26E4 |
| **Professor** | Ian Monteiro Nunes |
| **Bloco** | Ciência da Computação |
| **Turma** | GRLENGR2C2-N2-L1 |
| **Instituição** | Instituto Infnet |

> Texto do enunciado, na íntegra, como foi entregue pela disciplina. Onde cada exercício é atendido:
> [notebook](../../andre_becker_DR1_TP3.ipynb) e [relatório](../RELATORIO_TP3.md).

---

Chegamos à etapa final deste ciclo da disciplina. Neste Teste de Performance 3 (TP3), você será desafiado a trabalhar com recursão, programação dinâmica e algoritmos avançados de ordenação e seleção, consolidando competências fundamentais para resolver problemas computacionais complexos de forma eficiente, estruturada e justificável.

---

## Exercício 1 - Multiplicação Recursiva por Soma

**Introdução**

Em ambientes computacionais restritos, nem sempre todas as operações básicas estão disponíveis. Nessas situações, operações mais complexas precisam ser decompostas em operações simples. A recursão permite expressar esse tipo de decomposição de forma clara, controlada e sistemática. Neste exercício, você irá implementar uma multiplicação utilizando apenas somas, evidenciando o fluxo de chamadas recursivas e o momento em que as operações efetivamente ocorrem.

**Tarefa**

1. Implemente uma função recursiva mult(x, y) que calcule o produto de dois inteiros apenas por meio de somas.
2. Defina explicitamente o caso base da recursão.
3. Garanta funcionamento correto para valores positivos.
4. Instrumente a função para evidenciar chamadas e retornos.
5. Analise em que momento a soma ocorre: na chamada ou no retorno.

## Exercício 2 - Fatoração Recursiva de Inteiros

**Introdução**

A fatoração de números inteiros é um problema clássico que se beneficia de abordagens recursivas quando o espaço de busca é progressivamente reduzido. Neste exercício, você irá construir uma função recursiva que decompõe um número em seus fatores, controlando limites de busca, casos base e condições especiais.

**Tarefa**

1. Implemente uma função recursiva factor(x, lowest=2) que retorne a lista de fatores de x.
2. Limite os divisores ao intervalo entre lowest e a raiz quadrada de x.
3. Trate corretamente números primos.
4. Trate casos especiais como 0, 1 e números negativos.
5. Teste com diferentes valores de entrada.

## Exercício 3 - Potenciação Recursiva com Expoentes Negativos

**Introdução**

A potenciação é naturalmente definida de forma recursiva. A inclusão de expoentes negativos exige cuidado adicional na definição dos casos base e na transformação matemática do problema. Neste exercício, você irá implementar uma solução completa e consistente.

**Tarefa**

1. Implemente uma função recursiva power(x, y) para calcular x^y.
2. Defina casos base para expoentes 0 e 1.
3. Trate expoentes negativos utilizando transformação matemática adequada.
4. Teste a função com valores positivos, negativos e zero.
5. Analise a complexidade da solução.

## Exercício 4 - Navegação Recursiva em Estrutura de Diretórios

**Introdução**

Estruturas hierárquicas são naturalmente modeladas por recursão. Diretórios e subdiretórios formam uma árvore implícita que pode ser percorrida de maneira sistemática. Este exercício aplica recursão em um contexto prático e recorrente.

**Tarefa**

1. Implemente uma função recursiva que percorra um diretório e seus subdiretórios.
2. Liste os arquivos encontrados em cada nível.
3. Controle o nível de profundidade por meio de indentação.
4. Evite funções que realizem a travessia completa automaticamente.
5. Apresente evidências da execução.

## Exercício 5 - Geração Recursiva de Combinações (Times)

**Introdução**

A geração de combinações é um problema clássico resolvido naturalmente por recursão, envolvendo decisões sucessivas de inclusão e exclusão. Este exercício reforça o controle do estado recursivo e da construção incremental de soluções.

**Tarefa**

1. Implemente uma função recursiva teams(candidates, k).
2. Gere todas as combinações possíveis de tamanho k.
3. Utilize strings para representar os conjuntos.
4. Garanta que não haja repetições.
5. Teste com diferentes valores de k.

## Exercício 6 - Problema da Mochila (Knapsack Recursivo)

**Introdução**

O problema da mochila ilustra claramente os limites da recursão pura, pois envolve explosão combinatória. Ele serve como base para motivar técnicas de otimização posteriores.

**Tarefa**

1. Implemente uma função recursiva knapsack(target, weights, index).
2. Gere combinações de pesos que somem exatamente o valor alvo.
3. Utilize listas para armazenar combinações válidas.
4. Defina corretamente os casos base.
5. Teste com diferentes conjuntos de pesos.

## Exercício 7 - Análise de Complexidade em Algoritmos Recursivos

**Introdução**

Nem todo algoritmo recursivo é eficiente. Identificar redundâncias e crescimento excessivo de chamadas é essencial para análise algorítmica profissional.

**Tarefa**

1. Escolha uma função recursiva implementada anteriormente.
2. Identifique chamadas redundantes.
3. Analise o crescimento do número de chamadas.
4. Classifique a complexidade usando Big O.
5. Registre a análise em Markdown.

## Exercício 8 - Otimização com Programação Dinâmica

**Introdução**

A programação dinâmica surge como resposta direta aos problemas de redundância em algoritmos recursivos. Ao armazenar resultados intermediários, o custo computacional pode ser drasticamente reduzido.

**Tarefa**

1. Escolha um algoritmo recursivo com chamadas repetidas.
2. Implemente uma versão otimizada com memoização.
3. Compare o número de chamadas entre as versões.
4. Analise a redução de complexidade.
5. Apresente evidências da melhoria.

## Exercício 9 - Implementação do QuickSort

**Introdução**

O QuickSort é um algoritmo eficiente baseado em divisão e conquista. Sua implementação recursiva permite analisar claramente o impacto da escolha do pivô.

**Tarefa**

1. Implemente o QuickSort recursivo.
2. Utilize o último elemento como pivô.
3. Separe corretamente as partições.
4. Teste com arrays ordenados, invertidos e aleatórios.
5. Analise o comportamento observado.

## Exercício 10 - Instrumentação do QuickSort

**Introdução**

A instrumentação permite compreender o custo real de execução de um algoritmo. Neste exercício, você irá mensurar comparações e cópias realizadas pelo QuickSort.

**Tarefa**

1. Instrumente o QuickSort para contar comparações.
2. Considere uma troca como três cópias.
3. Execute com diferentes tipos de entrada.
4. Registre os resultados.
5. Compare os cenários analisados.

## Exercício 11 - Implementação do QuickSelect

**Introdução**

O QuickSelect resolve problemas de seleção sem ordenar todo o conjunto de dados, evitando trabalho desnecessário. Ele reforça a importância de alinhar algoritmo ao objetivo do problema.

**Tarefa**

1. Implemente o QuickSelect recursivo.
2. Permita selecionar qualquer índice desejado.
3. Utilize a lógica de partição do QuickSort.
4. Interrompa a recursão ao encontrar o índice alvo.
5. Teste para encontrar a mediana.

## Exercício 12 - Comparação entre QuickSort e QuickSelect

**Introdução**

Nem sempre ordenar é a melhor solução. Este exercício consolida a análise comparativa entre QuickSort e QuickSelect sob a ótica de eficiência.

**Tarefa**

1. Execute QuickSort e QuickSelect sobre os mesmos dados.
2. Compare comparações e cópias.
3. Analise os resultados obtidos.
4. Identifique cenários mais adequados para cada algoritmo.
5. Registre conclusões técnicas.

---

## Entrega

A entrega deste TP é composta obrigatoriamente por dois elementos:

**Relatório em PDF**

1. Reúna todos os screenshots gerados durante a execução em um único arquivo PDF.
2. Nomeie o arquivo conforme o padrão: nome_sobrenome_DR1_TP3.PDF.
3. Insira ao final do PDF o link para o vídeo descrito abaixo.

**Vídeo explicativo (obrigatório)**

Você deverá gravar um vídeo com duração entre 4 e 6 minutos, no qual deverá:

* Escolher quatro exercícios e explicar, com suas próprias palavras, o que foi feito.
* Demonstrar no terminal as principais execuções realizadas.
* Comentar brevemente cada execução e a estratégia adotada.
* Explicar decisões algorítmicas e impactos na complexidade.

Regras para o vídeo:

* O vídeo deve ser armazenado no Google Drive institucional.
* O link deve ter permissão de visualização.
* O link deve ser inserido ao final do PDF.

**Orientações para Defesa do Trabalho em Vídeo**

1. Utilize uma ferramenta adequada: é preciso que apareça a tela com seu trabalho e a imagem da sua webcam. Caso prefira, existe também a opção de baixar a ferramenta [OBS](https://obsproject.com/pt-br/download), dentre outras.
2. Escolha um local adequado: grave em um ambiente calmo, sem ruídos ou distrações, para garantir boa qualidade de áudio e foco durante a defesa.
3. Webcam ligada: certifique-se de que a webcam esteja ativada, com boa iluminação e enquadrando você de forma clara e centralizada.
4. Revise o vídeo: assista à gravação para verificar se o vídeo e o áudio estão bons.
5. Salve o vídeo no Google Drive: após a gravação, faça o upload do arquivo para o seu Google Drive de aluno Infnet.
6. Altere as permissões de acesso: configure o compartilhamento do vídeo para "qualquer pessoa com o link" poder visualizar. Copie o link gerado e envie conforme as instruções da atividade.

Assim que terminar, salve seu trabalho em PDF, nomeando o arquivo conforme a regra "nome_sobrenome_DR1_TP3.PDF" e poste como resposta a este TP. A ausência do vídeo implicará a avaliação do TP como incompleta.
