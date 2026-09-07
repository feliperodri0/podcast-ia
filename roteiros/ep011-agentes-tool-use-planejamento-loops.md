---
episodio: 011
titulo: "Agentes: tool use, planejamento, loops"
duracao_alvo_min: 12
prereq: [01, 02, 03, 04, 05, 06, 07, 08, 09, 10]
fontes:
  - url: https://www.anthropic.com/research
    nota: "episódio de fundamento da trilha base, sem paper específico — explica como um LLM (ep08), que só prevê o próximo token, pode agir fora da própria conversa por meio de chamada de ferramenta (tool use), e como isso vira um ciclo autônomo de ação e decisão; trata RAG (ep10) como um caso particular de ferramenta disponível a um agente"
---

[ANA] Oi, gente, bem-vindos de volta. Eu sou a Ana.

[BIA] E eu sou a Bia. Recapitulando rapidinho: no episódio dez a gente viu RAG, sigla em inglês pra Geração Aumentada por Recuperação. A ideia foi resolver o problema do conhecimento congelado do LLM, buscando pedaço de texto relevante por semelhança de embedding, antes de pedir pro modelo gerar a resposta.

[ANA] Isso. E terminei aquele episódio adiantando que RAG também é peça de um tipo de sistema mais amplo: um que não só busca informação, mas age no mundo, consulta ferramenta, executa ação, decide o próximo passo sozinho. É esse sistema, chamado de agente, o assunto de hoje.

[BIA] "Age no mundo" parece bem mais ambicioso do que só buscar um documento. Por onde a gente começa?

[ANA] Começa lembrando de uma coisa que a gente estabeleceu lá no episódio oito: um Modelo de Linguagem de Grande Escala, ou LLM, por baixo dos panos, só faz uma coisa. Ele prevê o próximo token, repetidamente, dado tudo que veio antes na conversa. Ele não "faz" nada no sentido de agir fora daquele texto. Guarda essa ideia, porque ela é a chave de tudo que vem hoje.

[BIA] Guardado. Mas então como um sistema desses consegue, por exemplo, mandar um email, ou rodar um pedaço de código? Se o modelo só prevê texto...

[ANA] É exatamente aí que entra a primeira peça de hoje: tool use, que a gente traduz como uso de ferramenta. A ideia é simples de enunciar. Junto da conversa, o sistema descreve pro modelo, em texto, quais ferramentas estão disponíveis: o nome de cada uma, o que ela faz, e que tipo de informação ela precisa receber pra funcionar. Por exemplo, uma ferramenta de busca, que precisa receber um termo de busca.

[BIA] Tá, mas isso ainda é só descrição em texto. Onde é que o modelo de fato aciona a ferramenta?

[ANA] Ele nunca aciona nada sozinho, e essa é a parte contraintuitiva. Quando o modelo "decide" usar uma ferramenta, o que ele faz, na prática, é prever um pedaço de texto num formato especial, combinado de antemão, dizendo algo como "quero usar a ferramenta tal, com esse valor de entrada". Esse texto sai do modelo do mesmo jeito que qualquer outro token previsto.

[BIA] E depois?

[ANA] Depois é o programa ao redor do modelo, não o modelo em si, que reconhece esse formato especial, entende que ali é um pedido de ferramenta, e de fato executa a ação de verdade: faz a busca, chama a função, roda o código. Esse programa então pega o resultado dessa execução e cola ele de volta na conversa, como se fosse mais um pedaço de texto, disponível pro modelo ler.

[BIA] Ah, então o modelo não sabe distinguir "isso eu decidi" de "isso é resultado real do mundo"? Pra ele é tudo só texto na mesma conversa?

[ANA] Exatamente essa é a virada de chave. Pro modelo, o resultado daquela busca, ou daquela execução de código, chega como mais um trecho de texto no meio da conversa, do mesmo jeito que chegaria uma frase digitada por você. E, tendo esse resultado novo à vista, o modelo continua gerando texto, só que agora com informação que ele não tinha antes, porque ela veio de fora, de uma ação real que aconteceu enquanto a conversa estava rolando.

[BIA] Isso já parece um primo do RAG do episódio passado. Lá, a busca em documento também virava texto extra colado na conversa antes da resposta final.

[ANA] Muito boa observação, e a relação é direta: dá pra pensar em RAG como um caso particular de ferramenta. "Buscar nos meus documentos" pode ser só mais uma das ferramentas disponíveis pro agente, ao lado de "rodar código", "consultar uma calculadora", "mandar um email". A diferença é que um agente não tem só uma ferramenta fixa usada sempre do mesmo jeito. Ele escolhe, sozinho, se usa ferramenta nenhuma, uma, ou várias, e em que ordem, dependendo do que a tarefa pede.

[BIA] E como o modelo decide isso, quando usar qual ferramenta, e quando parar de usar ferramenta e simplesmente responder?

[ANA] Aqui entra a segunda peça de hoje: o loop, que a gente traduz como ciclo. Um agente raramente resolve uma tarefa com uma única chamada de ferramenta. O padrão típico é: o modelo olha a tarefa, decide uma ação, o sistema executa essa ação e devolve o resultado, o modelo olha esse resultado novo e decide a próxima ação, e assim por diante, repetindo esse ciclo várias vezes, até o próprio modelo decidir que já tem informação suficiente pra dar uma resposta final, sem mais pedido de ferramenta.

[BIA] Dá um exemplo concreto? Ajuda a visualizar.

[ANA] Imagina um agente de programação, que recebe a tarefa "corrige esse erro no meu código". Primeiro ele usa uma ferramenta pra ler o arquivo. Lendo o conteúdo, ele tenta uma correção, e usa outra ferramenta pra rodar os testes automáticos daquele código. Se o teste falhar, o resultado do erro volta pro modelo, que lê aquilo, ajusta a correção, e manda rodar o teste de novo. Isso repete quantas vezes for preciso, até o teste passar, e só aí o agente conclui a tarefa.

[BIA] Entendi, então cada volta desse ciclo é: agir, ver o resultado, decidir a próxima ação, baseado no que aconteceu de fato, não só no que foi planejado antes.

[ANA] Exatamente esse é o loop. E antes mesmo da primeira ação, ainda tem uma coisa que ajuda bastante em tarefa mais complexa, que é planejamento: o modelo, olhando uma tarefa grande, quebra ela em passos menores, mais fáceis de resolver um de cada vez, em vez de tentar acertar tudo de uma vez só. No exemplo do bug, o plano seria mais ou menos "primeiro leio o código, depois entendo o erro, depois tento uma correção, depois confiro com teste".

[BIA] Isso quer dizer que o modelo sempre segue esse plano à risca, do início ao fim, sem desviar?

[ANA] Não necessariamente, e aí que entra a força do loop de novo: o plano pode, e costuma, mudar no meio do caminho, porque cada resultado real de ferramenta pode revelar algo que o plano original não previa. Se o teste falha de um jeito inesperado, o agente replaneja ali mesmo, em cima da informação nova, em vez de insistir cegamente no plano original.

[BIA] Isso parece bem mais poderoso que RAG sozinho. Mas eu imagino que também vem com risco novo, que RAG sozinho não tinha.

[ANA] Vem, e vale marcar essa ressalva. Primeiro, erro pode se acumular: se o modelo interpreta mal um resultado de ferramenta, ou escolhe a ferramenta errada pra aquela situação, a próxima ação já parte de uma base equivocada, e o ciclo inteiro pode seguir por um caminho ruim sem se corrigir sozinho. Segundo, sem um limite claro de quando parar, o loop pode simplesmente continuar rodando ação atrás de ação, sem nunca chegar numa resposta final. E terceiro, cada volta do ciclo custa: cada chamada de ferramenta, cada nova geração do modelo, leva tempo e tem custo, então uma tarefa que dá muitas voltas fica lenta e cara na mesma proporção.

[BIA] Então dá pra dizer que agente não é mágica, é o mesmo LLM de sempre, só que agora dentro de um ciclo de ação e leitura de resultado, podendo errar em cascata se algum passo no meio sair torto.

[ANA] Essa é a síntese certa. Um agente continua sendo, por baixo, o mesmo previsor de próximo token que a gente descreveu desde o episódio oito. O que muda é a estrutura ao redor dele: ferramentas disponíveis, descritas em texto; um formato especial pra pedir uso de uma ferramenta; um programa externo que de fato executa a ação e devolve o resultado como texto; e um ciclo que repete esse vaivém várias vezes, com planejamento ajudando a organizar os passos, até a tarefa estar resolvida ou o limite de tentativas ser atingido.

[BIA] Combinado, acho que agora entendo por que tanta gente fala de agente como o próximo salto depois de assistente de conversa simples.

[ANA] E hoje ainda sobra um problema que a gente só tocou de leve: com tanta chamada de modelo dentro de um único ciclo, o custo computacional de rodar tudo isso importa cada vez mais. E é exatamente esse o assunto do episódio doze: Mixture of Experts, que a gente traduz como Mistura de Especialistas, uma forma de deixar o modelo maior e mais capaz sem multiplicar o custo de cada chamada na mesma proporção.

[BIA] Combinado, guardo essa curiosidade pra lá então.

[ANA] Combinado. Por hoje é isso, pessoal. Guarda suas dúvidas, porque a gente vai voltar nelas nos próximos episódios.

[BIA] Valeu por ouvir a gente. Até o próximo episódio.
