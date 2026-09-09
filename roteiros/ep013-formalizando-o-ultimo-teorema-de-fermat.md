---
episodio: 013
titulo: "Formalizando o Último Teorema de Fermat"
duracao_alvo_min: 12
prereq: [08, 11]
fontes:
  - url: https://www.anthropic.com/research/formalizing-fermats-last-theorem
---

[ANA] Oi, gente, bem-vindos de volta. Eu sou a Ana.

[BIA] E eu sou a Bia. Recapitulando rapidinho: no episódio doze a gente viu Mixture of Experts, a Mistura de Especialistas, uma forma de deixar um modelo maior e mais capaz sem multiplicar o custo de cada resposta na mesma proporção. E terminamos aquele episódio prometendo que o episódio treze seria sobre raciocínio e sobre os modelos chamados de reasoning.

[ANA] Prometemos, e a gente ainda vai chegar lá — só que não hoje. De vez em quando essa trilha vai abrir uma exceção pra contar uma notícia fresca, saída há poucos dias de um laboratório de pesquisa, e hoje é um desses dias. Então o episódio de raciocínio vira o catorze, e o de hoje conta uma coisa que a Anthropic acabou de anunciar.

[BIA] Fiquei curiosa. O que aconteceu?

[ANA] A Anthropic contou que o Claude, trabalhando de forma largamente autônoma, ajudou a produzir a primeira prova totalmente verificada por computador do chamado Último Teorema de Fermat.

[BIA] Calma, isso tem nome importante demais numa frase só. Começa do início: o que é esse teorema?

[ANA] É uma afirmação de matemática proposta em mil seiscentos e trinta e sete por um matemático francês chamado Pierre de Fermat. Sem entrar em fórmula nenhuma, porque essa trilha não expõe matemática: ele afirmou que um certo tipo de equação, envolvendo três números inteiros elevados a uma potência maior que dois, nunca tem solução em números inteiros positivos. Fermat escreveu, na margem de um livro, que tinha achado uma prova disso, mas que a margem era pequena demais pra caber ali.

[BIA] E essa prova dele nunca apareceu?

[ANA] Nunca. Gerações de matemáticos tentaram, e falharam, por trezentos e cinquenta e oito anos. Só em mil novecentos e noventa e quatro um matemático britânico chamado Andrew Wiles conseguiu provar o teorema de verdade, com uma demonstração enorme e extremamente complexa, que levou anos pra ser escrita e outros tantos pra ser conferida por outros matemáticos.

[BIA] Então o que o Claude fez agora não foi provar o teorema de novo, foi outra coisa?

[ANA] Foi outra coisa, e é aqui que entra o segundo termo importante: formalizar. O Claude não descobriu um resultado novo. Ele pegou a prova que já existia, a de Wiles, e reescreveu ela inteira numa linguagem chamada Lean.

[BIA] O que é Lean?

[ANA] Lean é o que se chama de assistente de prova: um programa de computador que confere, passo a passo, se cada afirmação de uma demonstração matemática realmente segue da anterior, sem nenhum salto. A diferença pro jeito tradicional de provar teorema é grande. Quando um matemático humano escreve uma prova pra outros matemáticos lerem, ele pode pular passo considerado óbvio pra quem já tem a formação, confiando que o leitor completa o raciocínio sozinho.

[BIA] E o Lean não aceita esse tipo de salto?

[ANA] Não aceita nenhum. Pra ser aceita pelo Lean, uma prova precisa detalhar absolutamente todo passo lógico, por mais trivial que pareça, partindo só de um punhado de regras básicas da matemática que o programa já reconhece como verdadeiras de antemão. Se algum passo do raciocínio tiver um buraco, por menor que seja, o Lean recusa a prova. É um padrão de rigor muito mais alto do que revisão humana, porque não depende de nenhum revisor ler tudo e confiar no que está escrito, o próprio programa confere cada elo da corrente.

[BIA] Faz sentido então chamar isso de prova "verificada por computador": não é o computador que teve a ideia matemática original, é o computador que confirma, sem margem de dúvida, que cada passo da prova de Wiles realmente se sustenta.

[ANA] Exatamente essa é a distinção certa. E reescrever, nesse nível de detalhe, uma prova que já era enorme quando escrita pra humano, é um trabalho gigantesco. É aí que entra o que a gente descreveu lá no episódio onze: agente.

[BIA] Peraí, deixa eu tentar juntar os pontos. Se um agente é um LLM com ferramenta disponível e um ciclo de ação e leitura de resultado repetindo até a tarefa terminar, como isso vira "formalizar um teorema"?

[ANA] Nesse caso, a ferramenta principal do agente é o próprio Lean: o agente escreve um trecho de prova, manda o Lean conferir aquele trecho, lê de volta se o Lean aceitou ou recusou, e ajusta o próximo trecho com base nisso. E aqui está o detalhe que faz esse episódio diferente de tudo que vimos até agora nessa trilha: não foi um agente sozinho fazendo esse ciclo. Foram dezenas de instâncias de Claude, rodando ao mesmo tempo, cada uma provando pedaços diferentes e cada vez mais complexos do teorema, dependendo dos pedaços já provados pelas outras.

[BIA] Dezenas de agentes trabalhando juntos, ao mesmo tempo, na mesma prova. Como é que eles evitam pisar no pé um do outro, ou repetir trabalho à toa?

[ANA] Usando uma peça extra que a Anthropic construiu pra essa tarefa, chamada de Prove2Me. Ela mantém um mapa de quais pedacinhos do teorema já foram provados, quais ainda faltam, e quais dependem de quais. Cada agente consulta esse mapa, escolhe um pedaço ainda não resolvido que ele consegue tentar naquele momento, e devolve o resultado pro mapa quando termina, liberando os próximos pedaços que dependiam daquele.

[BIA] Então o mapa é tipo uma lista de tarefas compartilhada, onde terminar uma libera a próxima, e vários agentes pescam tarefa dessa lista ao mesmo tempo, sem duplicar esforço.

[ANA] Essa é a ideia. E teve um problema prático que quase travou esse jeito de trabalhar: nas primeiras tentativas, os agentes iam perdendo, aos poucos, a noção de onde o projeto inteiro estava, e paravam de colaborar direito entre si. O Prove2Me, com esse mapa estruturado e compartilhado, foi o que resolveu isso, dando pra cada agente um jeito confiável de saber o estado real do projeto a qualquer momento, sem depender da própria memória da conversa dele.

[BIA] E quanto tempo essa formalização toda levou?

[ANA] Pouco menos de duas semanas: onze dias, trabalhando de forma largamente autônoma. O resultado final passa de treze milhões de linhas de código Lean, com mais de trinta mil teoremas menores provados no caminho, dos quais vinte e nove mil e quinhentos entraram de fato na prova final. Pra dar uma noção de escala: essa prova sozinha é cerca de cinco vezes maior que a Mathlib, que é a principal biblioteca de provas formais mantida pela comunidade matemática inteira, construída ao longo de anos por muita gente.

[BIA] Isso é um volume gigantesco de trabalho pra formalizar uma prova que já existia. Vale a pena? Qual é o ganho real disso, além do feito em si?

[ANA] Alguns ganhos concretos. Primeiro, verificação: com a prova formalizada, não sobra dúvida nenhuma sobre nenhum passo dela, porque o Lean já conferiu tudo, então fica mais fácil confiar no resultado e mais fácil detectar se algum erro tivesse escapado na versão original escrita pra humano. Segundo, isso tira peso de cima dos matemáticos que hoje revisam prova alheia manualmente, um trabalho lento e sujeito a erro humano. E terceiro, a Anthropic já mostrou um sinal de que esse jeito de trabalhar escala pra baixo, não só pra cima: pesquisadores usando só três assinaturas comuns do Claude, do tipo que qualquer pessoa pode assinar, formalizaram um outro teorema conhecido, o de Vinogradov, em apenas três dias.

[BIA] Ou seja, não precisa ser um laboratório gigante com recurso especial pra fazer esse tipo de formalização.

[ANA] É esse o sinal. E o texto da Anthropic aponta pra uma mudança de hábito possível daqui pra frente: conforme fica mais barato formalizar prova desse jeito, pode virar comum publicar um trabalho de matemática já acompanhado da versão formalizada dele, verificada por computador, lado a lado com a versão tradicional escrita pra leitor humano.

[BIA] Resumindo pra fechar: o Último Teorema de Fermat já tinha sido provado por Andrew Wiles em mil novecentos e noventa e quatro. O que o Claude fez agora foi reescrever essa prova inteira, passo a passo, sem nenhum salto, numa linguagem chamada Lean, que confere cada elo da corrente lógica automaticamente. E o jeito de fazer isso foi dezenas de agentes, dos que a gente descreveu no episódio onze, trabalhando ao mesmo tempo, coordenados por um mapa compartilhado de tarefas, ao longo de onze dias.

[ANA] Exatamente essa é a síntese. E com essa notícia contada, a gente volta pro fio principal da trilha no próximo episódio: episódio catorze, sobre raciocínio, e sobre o que muda quando o processo de "pensar" de um modelo fica visível no meio da própria resposta.

[BIA] Combinado, guardo essa curiosidade pra lá então.

[ANA] Combinado. Por hoje é isso, pessoal. Guarda suas dúvidas, porque a gente vai voltar nelas nos próximos episódios.

[BIA] Valeu por ouvir a gente. Até o próximo episódio.
