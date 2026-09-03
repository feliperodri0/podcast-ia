---
episodio: 007
titulo: "Atenção e o Transformer"
duracao_alvo_min: 12
prereq: [01, 02, 03, 04, 05, 06]
fontes:
  - url: https://www.anthropic.com/research
    nota: "episódio de fundamento da trilha base, sem paper específico — explica o mecanismo de atenção e a arquitetura Transformer, que conecta embeddings (ep06) aos modelos de linguagem que vêm a seguir na trilha"
---

[ANA] Oi, gente, bem-vindos de volta. Eu sou a Ana.

[BIA] E eu sou a Bia. Recapitulando rapidinho: no episódio seis a gente resolveu um problema que estava faltando, como transformar palavra em número. Vimos que cada palavra vira uma lista de números, um embedding, que funciona como coordenada num espaço onde palavras parecidas ficam próximas.

[ANA] Isso. E no fim daquele episódio você mesma levantou uma dúvida ótima: processar uma frase palavra por palavra, cada uma isolada em sua coordenada, não parece meio limitado? Porque o significado de uma frase depende de como as palavras se relacionam entre si, não só de cada palavra sozinha.

[BIA] Lembro sim. Dei o exemplo de que uma frase é mais do que a soma das palavras separadas.

[ANA] Exatamente. E o assunto de hoje é a peça que resolve isso: atenção, e a arquitetura que foi construída em cima dela, chamada Transformer. É esse mecanismo que permite uma rede olhar pra frase inteira de uma vez e decidir quais palavras devem influenciar o entendimento de quais outras.

[BIA] Antes de explicar como funciona, me convence de que isso é mesmo um problema. Me dá um exemplo de frase onde só olhar palavra por palavra, isolada, dá errado.

[ANA] Boa cobrança. Pega essa frase: "O banco estava cheio, então sentei na grama perto do rio." Se você olhar só a palavra "banco" sozinha, sem contexto, ela pode significar instituição financeira ou pode significar assento. O resto da frase é que desempata isso: "grama" e "rio" empurram o significado pro lado de "assento", não "instituição financeira".

[BIA] Entendi. Então o significado de uma palavra muda dependendo de quem está por perto dela na frase.

[ANA] Exatamente essa é a ideia central. E "atenção" é o nome técnico dado ao mecanismo que faz uma palavra "olhar" pras outras palavras da frase e decidir, pra cada uma delas, o quanto ela deve pesar na hora de entender o significado daquela palavra ali. No nosso exemplo, quando a rede processa "banco", o mecanismo de atenção faz ela dar bastante peso pra "grama" e "rio", e seria diferente numa frase tipo "fui ao banco sacar dinheiro", onde "sacar" e "dinheiro" puxariam o peso pro outro sentido.

[BIA] Isso parece meio parecido com o que a gente já discutiu: uma rede aprendendo sozinha o que prestar atenção, sem alguém programar à mão "banco perto de rio significa assento".

[ANA] Exatamente essa conexão de novo. Ninguém escreve regra explicando qual palavra deve prestar atenção em qual. Durante o treino, a rede ajusta, por retropropagação, o quanto cada palavra deve pesar sobre cada outra, pra cada frase que ela vê. Com uma quantidade gigantesca de texto de treino, esse mecanismo de atenção aprende sozinho a captar esse tipo de relação de contexto.

[BIA] E como isso funciona na prática? Cada palavra "olha" literalmente pra todas as outras da frase?

[ANA] Sim, é exatamente essa a mecânica, e é o que faz esse método ser tão poderoso: pra cada palavra da frase, o mecanismo de atenção calcula um peso de relevância em relação a cada uma das outras palavras da mesma frase, incluindo ela mesma. Palavras muito relevantes pro entendimento daquela palavra recebem peso alto, palavras pouco relevantes recebem peso baixo, e depois a rede combina as coordenadas das palavras usando esses pesos, criando uma versão nova daquela palavra, agora já "temperada" pelo contexto ao redor.

[BIA] Peraí, "todas as outras palavras da frase, ao mesmo tempo"? Isso é diferente de processar uma de cada vez, em ordem, como eu imaginava no fim do episódio passado?

[ANA] É bem diferente, e essa diferença importa muito na prática. Antes da atenção virar popular, era comum processar frase em sequência, palavra um, depois palavra dois, depois palavra três, cada passo dependendo do anterior ter terminado. Isso tem duas desvantagens: é mais lento, porque não dá pra paralelizar o processamento, e frases longas tendem a "esquecer" informação das primeiras palavras até chegar nas últimas. Com atenção, toda palavra olha pra todas as outras ao mesmo tempo, o que é mais rápido de processar em paralelo, e também não perde informação de palavras distantes na frase.

[BIA] Isso é uma vantagem e tanto. E qual é a relação entre esse mecanismo de atenção e essa outra palavra que você mencionou, Transformer?

[ANA] Transformer é o nome da arquitetura, ou seja, do desenho completo de rede neural, que foi construída tendo esse mecanismo de atenção como sua peça central. Antes do Transformer existir, já existia a ideia de atenção sendo usada como um complemento em outros tipos de rede. A virada foi quando pesquisadores perceberam que dava pra construir uma rede inteira baseada quase só em atenção, empilhando várias camadas desse mecanismo, sem depender daquele processamento sequencial, palavra por palavra, que a gente descreveu.

[BIA] E essa mudança de arquitetura foi um marco parecido com aquele de dois mil e doze que a gente viu no episódio cinco, com o Deep Learning?

[ANA] É uma boa comparação. Assim como dois mil e doze mostrou que empilhar mais camadas, com dados e processamento certos, batia tudo que veio antes, o Transformer mostrou que basear uma rede em atenção, em vez de processamento sequencial, treinava mais rápido e entendia melhor relações de contexto, principalmente em frases longas. Essa arquitetura virou a base de praticamente todo sistema de linguagem relevante construído depois dela.

[BIA] Deixa eu tentar montar o quadro completo até aqui. A gente tem: rede neural, que processa número em camadas, ajustando peso por retropropagação, isso veio dos episódios quatro e cinco. Tem embedding, que transforma palavra em número preservando significado, isso veio do episódio seis. E agora tem atenção, que deixa cada palavra "olhar" pras outras da mesma frase e pesar a relevância delas, empacotada numa arquitetura chamada Transformer.

[ANA] Resumiu perfeitamente, e reparar que essas três peças se encaixam é exatamente o ponto de chegar até aqui. Com essas peças juntas, já dá pra imaginar um sistema que recebe uma frase inteira, converte cada palavra em número via embedding, deixa cada palavra reponderar seu significado olhando pras outras via atenção, e processa tudo isso em camadas empilhadas de rede neural.

[BIA] E isso já é, tecnicamente, o que a gente chamaria de modelo de linguagem?

[ANA] Você antecipou o assunto certinho, mas ainda falta uma peça importante antes de chegar lá: a escala. Um Transformer pequeno, treinado com pouco texto, entende gramática básica, mas não faz o que a gente vê hoje em sistemas de conversação. No episódio oito a gente vai falar sobre o que é de fato um LLM, um Modelo de Linguagem de Grande Escala, e vai entender por que treinar essa mesma arquitetura Transformer com uma quantidade descomunal de texto muda completamente o que ela é capaz de fazer.

[BIA] Combinado, então. Por hoje é isso, pessoal. Guarda suas dúvidas, porque a gente vai voltar nelas nos próximos episódios.

[ANA] Valeu por ouvir a gente. Até o próximo episódio.
