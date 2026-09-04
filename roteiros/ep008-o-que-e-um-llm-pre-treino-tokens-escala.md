---
episodio: 008
titulo: "O que é um LLM? Pré-treino, tokens, escala"
duracao_alvo_min: 12
prereq: [01, 02, 03, 04, 05, 06, 07]
fontes:
  - url: https://www.anthropic.com/research
    nota: "episódio de fundamento da trilha base, sem paper específico — define o que é um Modelo de Linguagem de Grande Escala a partir das peças já construídas nos episódios anteriores (rede neural, embedding, atenção e Transformer), cobrindo tokenização, pré-treino e o papel da escala"
---

[ANA] Oi, gente, bem-vindos de volta. Eu sou a Ana.

[BIA] E eu sou a Bia. Recapitulando rapidinho: no episódio sete a gente juntou três peças. Rede neural, que processa número em camadas. Embedding, que transforma palavra em número preservando significado. E atenção, empacotada numa arquitetura chamada Transformer, que deixa cada palavra olhar pras outras da mesma frase.

[ANA] Isso. E no fim daquele episódio eu deixei uma pergunta no ar: será que juntar essas três peças já é, tecnicamente, o que a gente chama de Modelo de Linguagem de Grande Escala, ou LLM, sigla que vem do inglês "Large Language Model"?

[BIA] E a resposta foi que ainda falta uma peça: escala. Mas fiquei sem entender direito o que isso quer dizer na prática. Escala de quê, exatamente?

[ANA] Ótima pergunta, e é o assunto de hoje inteiro. Mas antes de chegar em escala, preciso fechar um buraco que eu pulei nos últimos dois episódios: como é que um texto inteiro, uma frase, um parágrafo, vira a sequência de palavras que a gente manda pro embedding processar? Eu falei "cada palavra vira um embedding", mas um Transformer de verdade não trabalha exatamente com palavra inteira.

[BIA] Como assim, não trabalha com palavra inteira? Com o que ele trabalha, então?

[ANA] Ele trabalha com pedaços de texto chamados tokens. Um token pode ser uma palavra inteira, se ela for comum, tipo "casa" ou "gato". Mas pode ser também um pedaço de palavra. Uma palavra rara ou muito longa costuma ser quebrada em dois ou três tokens menores, e até espaço em branco e sinal de pontuação viram token.

[BIA] E por que não usar sempre a palavra inteira? Parece mais simples.

[ANA] Pareceria mais simples, mas cria um problema prático sério. Um sistema desses precisa de uma lista fixa e limitada de pedacinhos possíveis, chamada vocabulário, porque cada pedacinho diferente vai precisar do seu próprio embedding, daquela lista de números que a gente descreveu no episódio seis. Se cada palavra inteira da língua precisasse do seu próprio embedding, esse vocabulário ficaria enorme, e ainda assim palavra nova, gíria nova, nome próprio, erro de digitação, tudo isso ficaria de fora.

[BIA] Ah, entendi a lógica. Quebrando em pedaços menores, um vocabulário de tamanho controlado consegue montar qualquer palavra, mesmo uma que ele nunca viu inteira antes, juntando pedacinhos que ele já conhece.

[ANA] Exatamente isso. E o processo de decidir como quebrar um texto em tokens também é aprendido a partir de uma quantidade gigantesca de texto, buscando os pedaços que aparecem com mais frequência, pra que palavras comuns virem um token só e só palavras raras precisem ser fatiadas em pedaços menores. Depois que o texto vira uma sequência de tokens, cada token recebe seu embedding, e é essa sequência de embeddings que entra no Transformer, exatamente como a gente descreveu nos episódios seis e sete.

[BIA] Beleza, peça do token encaixada. Agora volta pra escala. O que muda de um Transformer pequeno pra um LLM de verdade?

[ANA] Aqui entra o segundo conceito de hoje: pré-treino. A tarefa que se usa pra treinar um LLM é enganosamente simples: dado um pedaço de texto, adivinhar qual é o próximo token. Só isso. Pega um trecho de texto real, esconde o token seguinte, pede pro modelo chutar, compara o chute com o token verdadeiro, e ajusta os pesos da rede por retropropagação, exatamente o mecanismo que a gente descreveu lá no episódio quatro.

[BIA] Só isso mesmo? Adivinhar a próxima palavra parece uma tarefa bem mais simples do que eu esperava pra algo que depois consegue conversar, escrever texto, responder pergunta.

[ANA] E é exatamente aí que a escala entra. Essa tarefa de adivinhar o próximo token é repetida um número descomunal de vezes, sobre uma quantidade de texto que soma trilhões de tokens, vindos de uma fatia enorme de tudo que já foi escrito e publicado digitalmente. E a rede que faz esse trabalho não é pequena: os LLMs mais usados hoje têm bilhões, ou até mais de um trilhão, de pesos ajustáveis, aquilo que a gente chamou de parâmetros lá no episódio quatro.

[BIA] Então "escala" quer dizer, ao mesmo tempo, uma quantidade gigantesca de texto de treino e uma rede gigantesca de parâmetros pra ajustar.

[ANA] Isso, as duas coisas crescendo juntas. E o resultado observado, muitas vezes até de forma surpreendente pra quem pesquisa isso, é que aumentar essas duas coisas ao mesmo tempo não só deixa o modelo um pouco melhor em adivinhar a próxima palavra. Em certos patamares de tamanho, a rede passa a fazer coisas que ninguém pediu explicitamente na tarefa de treino: seguir o estilo de um texto, responder pergunta com informação que ela nunca viu formulada daquele jeito exato, até seguir um raciocínio em vários passos. Nenhuma dessas coisas foi ensinada como tarefa separada, elas emergem só de prever o próximo token, em escala gigantesca.

[BIA] Isso é impressionante, mas também meio contraintuitivo. Como é que só prever a próxima palavra ensina o modelo a fazer coisa tão mais complexa que isso?

[ANA] A explicação mais aceita é que, pra ficar bom em prever o próximo token numa quantidade de texto tão variada quanto praticamente tudo que a humanidade escreveu, o modelo é empurrado a captar padrão de gramática, de fato, de argumento, de estilo, de raciocínio, porque tudo isso ajuda a prever melhor o que vem a seguir num texto real. Ninguém programa "aprenda gramática" ou "aprenda a somar", isso surge como efeito colateral de ficar bom na tarefa simples, só que em escala descomunal.

[BIA] Deixa eu tentar juntar tudo. Um LLM pega texto, quebra em tokens, transforma cada token num embedding, processa essa sequência com atenção dentro de uma arquitetura Transformer, e foi treinado, por pré-treino, adivinhando o próximo token repetidamente sobre uma quantidade gigantesca de texto, usando uma rede com uma quantidade gigantesca de parâmetros. E é essa combinação de escala que faz capacidades mais complexas emergirem, sem terem sido ensinadas direto.

[ANA] Resumiu perfeitamente. E vale fechar com um ponto importante, que já é gancho pro próximo episódio: um modelo que só passou por esse pré-treino sabe prever texto de forma muito fluente, mas ele não nasce sabendo se comportar como assistente que conversa com você, que segue instrução, que evita responder coisa perigosa. Ele só aprendeu a continuar texto de um jeito plausível, sem ideia agindo do modo que a gente empresa quando conversa com um Claude ou um ChatGPT no dia a dia.

[BIA] Então tem outra etapa depois do pré-treino, pra chegar nesse comportamento de assistente que a gente conhece?

[ANA] Exatamente, e é o assunto do episódio nove: fine-tuning, ou ajuste fino, e uma técnica chamada RLHF, sigla em inglês pra Aprendizado por Reforço com Realimentação Humana. É nessa etapa seguinte que um LLM pré-treinado, que só sabe prever próximo token, começa a virar um assistente que segue instrução e se comporta de um jeito alinhado ao que a gente espera dele.

[BIA] Combinado, então. Por hoje é isso, pessoal. Guarda suas dúvidas, porque a gente vai voltar nelas nos próximos episódios.

[ANA] Valeu por ouvir a gente. Até o próximo episódio.
