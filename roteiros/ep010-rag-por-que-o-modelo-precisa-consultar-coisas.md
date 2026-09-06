---
episodio: 010
titulo: "RAG: por que o modelo precisa consultar coisas"
duracao_alvo_min: 12
prereq: [01, 02, 03, 04, 05, 06, 07, 08, 09]
fontes:
  - url: https://www.anthropic.com/research
    nota: "episódio de fundamento da trilha base, sem paper específico — explica RAG (Geração Aumentada por Recuperação) como resposta ao problema de conhecimento congelado no pré-treino (ep08) e desconhecimento de documentos privados, reaproveitando o conceito de embedding do episódio seis"
---

[ANA] Oi, gente, bem-vindos de volta. Eu sou a Ana.

[BIA] E eu sou a Bia. Recapitulando rapidinho: no episódio nove a gente viu como um Modelo de Linguagem de Grande Escala, ou LLM, deixa de ser só um previsor de próximo token e vira assistente. Primeiro com ajuste fino supervisionado, usando pares de instrução e resposta ideal. Depois com RLHF, sigla em inglês pra Aprendizado por Reforço com Realimentação Humana, em que um modelo de recompensa aprende o gosto humano por comparação, e o LLM é empurrado a gerar respostas que esse avaliador automático nota bem. Ao conjunto dessas duas etapas a gente deu o nome de alinhamento.

[ANA] Isso. E terminei aquele episódio adiantando o assunto de hoje: mesmo um modelo bem alinhado carrega uma limitação que o alinhamento não resolve. Ele só sabe o que estava no texto que ele viu durante o pré-treino.

[BIA] Isso eu não tinha parado pra pensar. Quer dizer que, depois de treinado, o conhecimento do modelo fica congelado?

[ANA] Exatamente. Lembra do episódio oito, quando a gente descreveu pré-treino como adivinhar o próximo token repetidamente sobre uma quantidade gigantesca de texto? Pois esse texto foi coletado até uma certa data. Tudo que aconteceu depois disso, notícia nova, versão nova de um produto, resultado de jogo de ontem, simplesmente não apareceu em nenhum exemplo de treino. O modelo não tem como saber.

[BIA] Faz sentido pra notícia recente. Mas e um documento meu, uma planilha da minha empresa, um arquivo que eu tenho no computador? Isso também é esse mesmo problema?

[ANA] É o mesmo problema, só que ainda mais direto: documento privado seu nunca esteve disponível publicamente pra entrar no treino de ninguém. O modelo nunca teve chance de ver aquele conteúdo, então não tem como responder pergunta específica sobre ele, a não ser que alguém entregue esse conteúdo pra ele de alguma forma.

[BIA] E dá pra simplesmente treinar o modelo de novo, toda vez que aparece informação nova ou documento novo, pra manter ele atualizado?

[ANA] Na prática, não. Pré-treino é um processo caro e demorado, feito sobre uma rede com uma quantidade enorme de parâmetros, como vimos no episódio oito. Repetir isso toda vez que surge uma notícia nova, ou toda vez que uma empresa quer que o modelo saiba de um documento novo, seria inviável. Precisa de outra solução, uma que não passe por treinar de novo.

[BIA] E essa solução é o assunto de hoje, então? Você falou uma sigla lá no fim do episódio passado.

[ANA] Isso, RAG, sigla em inglês pra "Retrieval-Augmented Generation", que a gente traduz como Geração Aumentada por Recuperação. A ideia central é simples de enunciar: em vez de depender só do que o modelo já tem guardado dos pesos ajustados no treino, o sistema primeiro vai buscar informação relevante em algum lugar de fora, e só depois pede pro modelo gerar a resposta, já com essa informação em mãos.

[BIA] Buscar informação relevante onde, exatamente? E como o sistema sabe o que é relevante pra uma pergunta?

[ANA] Aqui é onde entra uma peça que a gente já construiu, lá no episódio seis: embedding. Lembra que a gente descreveu embedding como transformar um pedaço de texto numa lista de números que preserva significado, de um jeito que textos com sentido parecido acabam com listas de números parecidas entre si?

[BIA] Lembro, foi o exemplo de "rei" e "rainha" ficando com embeddings próximos, por causa da relação de significado entre eles.

[ANA] Isso mesmo. Pois num sistema de RAG, antes de qualquer pergunta ser feita, todo o conjunto de documentos disponível, seja a base de conhecimento de uma empresa, seja um conjunto de notícias recentes, é quebrado em pedaços menores, e cada pedaço passa pelo mesmo processo de virar um embedding. O resultado é guardado numa espécie de banco de dados especializado nesse tipo de busca por semelhança.

[BIA] E quando eu faço uma pergunta pro sistema, o que acontece?

[ANA] A sua pergunta também é transformada num embedding, do mesmo jeito. E o sistema busca, dentro daquele banco de pedaços de documento, quais embeddings estão mais próximos do embedding da sua pergunta. Como embeddings próximos indicam significado parecido, os pedaços de texto encontrados tendem a ser, de fato, relevantes pra responder aquela pergunta específica, mesmo sem nenhuma palavra idêntica entre pergunta e documento.

[BIA] Ah, entendi a jogada. Em vez de o modelo precisar ter aprendido aquela informação de cor durante o treino, o sistema vai buscar o trecho certo bem na hora, usando semelhança de significado, não busca de palavra exata.

[ANA] Exatamente essa é a virada. E aí vem a parte de "Geração" do nome: esses pedaços de texto recuperados são colocados junto da sua pergunta original, formando uma instrução maior, que é essa a que de fato é entregue pro LLM. O modelo então gera a resposta com aquele contexto extra na frente dos olhos, em vez de depender só do que ele memorizou no pré-treino.

[BIA] Deixa eu tentar montar o quadro completo. Primeiro, os documentos disponíveis são quebrados em pedaços e viram embeddings, guardados num banco de busca. Quando chega uma pergunta, ela também vira embedding, e o sistema busca os pedaços de documento com embedding mais parecido. Esses pedaços são colocados junto da pergunta, e é esse pacote inteiro que o LLM recebe pra gerar a resposta final.

[ANA] Resumiu certinho, essas são as duas etapas: recuperação, achando o trecho certo por semelhança de embedding, e geração, o LLM respondendo com aquele trecho à vista. E o ganho prático é grande: dá pra atualizar a informação disponível pro modelo só trocando o conteúdo desse banco de documentos, sem precisar treinar a rede de novo. Notícia de hoje, documento novo, política interna que mudou semana passada, tudo isso entra imediatamente, só reindexando.

[BIA] Isso quer dizer que, com RAG, o modelo passa a saber de tudo que tiver nesse banco de documentos, sem erro?

[ANA] Não, de jeito nenhum, e vale marcar essa ressalva. A qualidade da resposta depende diretamente da etapa de recuperação ter achado o pedaço certo. Se a pergunta for ambígua, ou se o jeito de quebrar os documentos em pedaços tiver cortado uma informação no meio, o sistema pode recuperar um trecho pouco relevante, ou incompleto, e o LLM vai gerar a resposta em cima dessa base já falha. RAG reduz bastante o problema do conhecimento congelado e do documento privado desconhecido, mas depende de uma etapa de busca que também pode errar.

[BIA] Entendi, então RAG resolve "o modelo não sabe isso", mas não resolve todo tipo de erro que o modelo pode cometer na hora de responder.

[ANA] Exatamente essa é a fronteira dela. E RAG, além de resolver conhecimento congelado, também é uma peça central de um tipo de sistema mais amplo, que não só busca informação, mas age no mundo: consulta ferramenta, executa ação, decide o próximo passo sozinho. E é justamente esse o assunto do episódio onze: agentes.

[BIA] Combinado, guardo essa curiosidade pra lá então.

[ANA] Combinado. Por hoje é isso, pessoal. Guarda suas dúvidas, porque a gente vai voltar nelas nos próximos episódios.

[BIA] Valeu por ouvir a gente. Até o próximo episódio.
