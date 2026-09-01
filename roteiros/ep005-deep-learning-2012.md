---
episodio: 005
titulo: "Deep Learning e por que 2012 mudou tudo"
duracao_alvo_min: 12
prereq: [01, 02, 03, 04]
fontes:
  - url: https://www.anthropic.com/research
    nota: "episódio de fundamento da trilha base, sem paper específico — usa o marco histórico do ImageNet 2012 (AlexNet) pra explicar por que empilhar mais camadas destravou o Deep Learning"
---

[ANA] Oi, gente, bem-vindos de volta. Eu sou a Ana.

[BIA] E eu sou a Bia. Recapitulando rapidinho: no episódio quatro a gente abriu a caixa da rede neural. Vimos que ela é feita de neurônios artificiais, organizados em camadas, cada uma recebendo o que a anterior já resumiu. E vimos o mecanismo que ajusta os pesos desses neurônios, a retropropagação, que pega o erro da resposta final e devolve ele pra trás, camada por camada.

[ANA] Isso. E no fim daquele episódio eu deixei escapar uma pista: tudo o que vem daqui pra frente nesse podcast é rede neural numa escala muito, muito maior do que os exemplos que a gente usou. Hoje é o dia de entender por que essa escala importa tanto que ela ganhou um nome próprio: Deep Learning, ou aprendizado profundo.

[BIA] "Profundo" aí é sobre ter mais camadas, então? Porque no episódio passado você já falou em camada de entrada, camadas ocultas no meio, e camada de saída.

[ANA] Exatamente essa é a ideia. Uma rede é chamada de "profunda" quando ela empilha bastante camadas ocultas, não só uma ou duas. E empilhar mais camadas não é só "mais do mesmo": é isso que permite a rede construir conceitos cada vez mais elaborados, um em cima do outro, do jeito que a gente descreveu com aquele exemplo de bordas virando formas, e formas virando "isso parece uma orelha".

[BIA] Então por que ninguém simplesmente empilhou um monte de camadas desde o início? Se mais camadas dão mais poder, por que esperar até dois mil e doze pra isso "mudar tudo", como você prometeu no fim do episódio passado?

[ANA] Porque empilhar camadas parece simples na teoria, mas esbarrava em três problemas bem concretos, e é justamente a combinação de resolver esses três problemas ao mesmo tempo que faz de dois mil e doze um marco. O primeiro problema é dado: pra uma rede profunda aprender algo útil, ela precisa de muitos exemplos, muitos mesmo. Redes rasas, com poucas camadas, conseguiam se virar com conjuntos de exemplos menores. Redes profundas, não.

[BIA] E antes de dois mil e doze não existia gente suficiente tirando foto pra treinar essas redes?

[ANA] Existia gente tirando foto, sim, mas não existia um conjunto de dados organizado, rotulado e gigantesco, disponível pra qualquer pesquisador usar. Isso mudou com um projeto chamado ImageNet: um banco de imagens com mais de um milhão de fotos, cada uma já classificada à mão em milhares de categorias diferentes, tipo "gato", "bicicleta", "chaleira". Foi um trabalho enorme de rotulação, e ele virou o combustível de dados que faltava.

[BIA] Beleza, esse é o primeiro problema resolvido, o de dados. Qual é o segundo?

[ANA] O segundo é poder de processamento. Treinar uma rede profunda significa fazer uma quantidade gigantesca de contas repetidas, ajustando peso atrás de peso, exemplo atrás de exemplo, muitas e muitas vezes. Os processadores de computador tradicionais, os mesmos que rodam a maioria dos programas do seu computador, fazem essas contas uma atrás da outra, e isso levaria tempo demais pra ser prático numa rede grande.

[BIA] E o que resolveu isso, então?

[ANA] Um tipo de chip que já existia, mas tinha sido criado pra outra finalidade: a placa de vídeo, originalmente feita pra desenhar gráficos de videogame na tela rapidamente. Acontece que o tipo de conta que uma placa de vídeo faz bem, muitas contas simples, ao mesmo tempo, em paralelo, é quase exatamente o tipo de conta que treinar uma rede neural exige. Pesquisadores perceberam isso e passaram a usar placas de vídeo pra treinar redes neurais, o que acelerou o treino de semanas pra dias.

[BIA] Interessante, então uma peça que já existia por outro motivo virou essencial aqui. E o terceiro problema, qual é?

[ANA] O terceiro é mais sutil, e tem a ver com a própria retropropagação que a gente descreveu no episódio passado. Em redes com muitas camadas empilhadas, o ajuste que volta lá da última camada até a primeira tende a ficar cada vez mais fraco, quase desaparecendo, antes de chegar nas camadas iniciais. Isso tem até um nome técnico, chamado de "desvanecimento do gradiente", mas o que importa aqui é o efeito prático: as primeiras camadas de uma rede muito profunda praticamente paravam de aprender, porque o sinal de ajuste chegava fraco demais nelas.

[BIA] Então de que adianta ter mais camadas se boa parte delas nem consegue aprender direito?

[ANA] Exatamente esse era o impasse. E foi uma combinação de pequenos ajustes técnicos na forma como cada neurônio processa seu sinal, junto com formas melhores de começar os pesos antes do treino, que amenizou esse problema o suficiente pra redes profundas finalmente treinarem bem. Nenhuma dessas peças sozinha resolveria tudo, mas dados em quantidade, poder de processamento das placas de vídeo, e esses ajustes técnicos, juntos, destravaram redes muito mais profundas do que qualquer coisa treinada antes.

[BIA] E é aí que entra dois mil e doze especificamente? O que aconteceu naquele ano, exatamente?

[ANA] Todo ano, o projeto ImageNet promovia uma competição: pesquisadores do mundo inteiro treinavam seus sistemas pra classificar aquele banco de mais de um milhão de imagens em suas categorias corretas, e o sistema mais preciso vencia. Em dois mil e doze, uma equipe treinou uma rede neural bem mais profunda do que era comum na época, usando placas de vídeo pra treinar rápido, e essa rede venceu a competição com uma margem de vitória muito maior do que qualquer coisa vista antes.

[BIA] Uma margem grande assim é tão importante? Não é só mais um ano de competição com um vencedor diferente?

[ANA] É importante porque até ali, os avanços de ano pra ano vinham sendo pequenos, incrementais. E de repente aparece uma abordagem que erra muito menos do que tudo que veio antes, numa única virada. Isso convenceu a comunidade inteira de pesquisadores, quase da noite pro dia, de que Deep Learning não era só mais uma técnica entre várias, era a direção certa a seguir. A partir dali, o investimento em pesquisa, em dados, e em placas de vídeo pra treinar redes profundas disparou.

[BIA] Então dois mil e doze não é o momento em que Deep Learning foi inventado, é o momento em que ele provou que funcionava melhor que tudo o mais, de um jeito que ninguém mais conseguiu ignorar.

[ANA] Essa é a forma perfeita de resumir. As ideias de rede neural profunda, camadas empilhadas, retropropagação, já existiam havia décadas antes disso, em versões mais simples. O que faltava era essa combinação específica: dados em escala de ImageNet, processamento em escala de placa de vídeo, e os ajustes técnicos que permitiram o treino funcionar bem em redes bem mais profundas. Dois mil e doze é quando essas peças finalmente se encaixaram todas juntas, na frente de todo mundo, numa competição pública.

[BIA] Deixa eu tentar resumir tudo isso, pra fechar o episódio de hoje. Deep Learning é o nome que se dá pra redes neurais com muitas camadas empilhadas, o que permite construir conceitos cada vez mais elaborados.

[ANA] Isso.

[BIA] E treinar essas redes profundas exigia resolver três problemas ao mesmo tempo: dados em grande quantidade, que veio com o ImageNet; poder de processamento rápido o bastante, que veio das placas de vídeo; e um jeito de fazer o ajuste dos pesos não enfraquecer demais nas primeiras camadas.

[ANA] Exatamente.

[BIA] E dois mil e doze foi o ano em que uma rede profunda treinada com essas três peças juntas venceu a competição do ImageNet por uma margem tão grande, que convenceu a comunidade inteira a apostar em Deep Learning.

[ANA] Resumiu tudo certinho. E vale fechar dizendo uma coisa importante: esse pivô de dois mil e doze é o motivo de praticamente tudo que a gente vai discutir daqui pra frente nesse podcast existir na forma como existe hoje. Sem essa virada, não teria acontecido a explosão de pesquisa que levou aos sistemas que reconhecem imagem, traduzem texto, e, mais adiante na nossa trilha, conversam com você.

[BIA] E é justamente sobre conversar com texto que entra o próximo episódio, né?

[ANA] Isso mesmo. No episódio seis a gente vai falar sobre embeddings, e como um texto, feito de palavras, vira número de um jeito que uma rede neural consegue processar. Essa é a ponte que faltava entre tudo que a gente já viu sobre redes neurais, e os sistemas de linguagem que a gente vai chegar mais adiante na trilha.

[BIA] Combinado. Por hoje é isso, pessoal. Guarda suas dúvidas, porque a gente vai voltar nelas nos próximos episódios.

[ANA] Valeu por ouvir a gente. Até o próximo episódio.
