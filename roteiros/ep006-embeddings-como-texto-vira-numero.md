---
episodio: 006
titulo: "Embeddings: como texto vira número"
duracao_alvo_min: 12
prereq: [01, 02, 03, 04, 05]
fontes:
  - url: https://www.anthropic.com/research
    nota: "episódio de fundamento da trilha base, sem paper específico — explica o mecanismo de embeddings que conecta redes neurais (ep04/05) aos sistemas de linguagem que vêm mais adiante na trilha"
---

[ANA] Oi, gente, bem-vindos de volta. Eu sou a Ana.

[BIA] E eu sou a Bia. Recapitulando rapidinho: no episódio cinco a gente entendeu o que é Deep Learning, redes neurais com muitas camadas empilhadas, e por que o ano de dois mil e doze foi o momento em que essa abordagem provou que funcionava melhor que qualquer coisa vista antes, numa competição de reconhecimento de imagem.

[ANA] Isso. E repara numa coisa: todo esse episódio, e os dois anteriores também, a gente usou exemplo de imagem. Cachorro, gato, orelha triangular. Imagem já nasce como número, cada pontinho da foto é um valor de cor. Mas o resto desse podcast vai ser sobre modelos que lidam com texto, com palavras. E aí surge uma pergunta que a gente ainda não respondeu: como é que uma rede neural, que só sabe processar número, lê uma palavra?

[BIA] Boa pergunta. Porque tudo que você descreveu até agora, neurônio, peso, camada, retropropagação, era sempre número entrando e número saindo. Palavra não é número.

[ANA] Exatamente esse é o buraco que fica faltando preencher, e é o assunto de hoje: embeddings. Essa é a técnica que transforma texto em número, de um jeito que preserva o significado da palavra, não só o texto bruto dela.

[BIA] Antes de ir pro jeito certo de fazer isso, deixa eu imaginar um jeito ingênuo. Por que não simplesmente dar um número pra cada palavra? Tipo, "gato" vira o número um, "cachorro" vira o número dois, "banana" vira o número três, e assim por diante.

[ANA] Essa ideia parece razoável, mas ela cria um problema sério. Se "gato" é um e "cachorro" é dois, e "banana" é três, a rede vai enxergar "cachorro" como estando exatamente no meio do caminho entre "gato" e "banana", só porque dois está entre um e três. Mas isso não faz sentido nenhum de significado. Gato e cachorro têm muito mais a ver entre si do que qualquer um dos dois tem com banana, e essa numeração simples não capta isso, ela é arbitrária.

[BIA] Entendi o problema. E se, em vez de dar só um número pra cada palavra, a gente desse uma lista enorme de interruptores, um interruptor pra cada palavra que existe, e a única regra é: liga o interruptor da palavra que apareceu, e deixa todos os outros desligados?

[ANA] Essa ideia já existiu de verdade, tem até nome técnico, mas o problema dela é outro: ela resolve a questão da ordem falsa, porque agora nenhuma palavra fica "mais perto" da outra por acidente, mas ela joga fora completamente qualquer noção de proximidade de significado. Pra essa lista de interruptores, "gato" e "cachorro" ficam tão distantes um do outro quanto "gato" e "banana". Tudo fica igualmente distante de tudo, e a rede perde justamente a informação que a gente queria preservar: que algumas palavras se parecem mais entre si do que outras.

[BIA] Então o desafio é achar um jeito de transformar palavra em número que preserve essa noção de "quão parecidas" duas palavras são. Como um embedding resolve isso?

[ANA] A ideia central é: em vez de representar cada palavra com um número só, ou com um interruptor isolado, a gente representa cada palavra com uma lista de vários números ao mesmo tempo, tipicamente centenas deles. E essa lista de números funciona como as coordenadas da palavra dentro de um espaço, quase como as coordenadas de um ponto num mapa.

[BIA] Um mapa com centenas de direções ao mesmo tempo? Isso já foge da minha imaginação de mapa comum, que só tem norte-sul e leste-oeste.

[ANA] Foge mesmo, e tudo bem não conseguir visualizar isso todo de uma vez. Mas a ideia por trás continua sendo a mesma de um mapa normal: coisas parecidas ficam em posições próximas, coisas diferentes ficam em posições distantes. Só que em vez de duas direções, norte-sul e leste-oeste, esse espaço tem centenas de direções possíveis, cada uma captando algum aspecto sutil de significado que ninguém precisou nomear à mão.

[BIA] Peraí, "ninguém precisou nomear à mão" é uma frase que já apareceu nos episódios anteriores, quando você falava de rede neural aprendendo características sozinha. Isso é a mesma coisa aqui?

[ANA] Exatamente a mesma lógica, e é uma ótima conexão você ter puxado. Ninguém senta e decide "a coordenada número um vai representar o quanto a palavra tem a ver com animal, a coordenada número dois vai representar o quanto ela tem a ver com comida". Essas coordenadas são aprendidas automaticamente, treinando uma rede neural com uma quantidade enorme de texto, usando exatamente aquele mecanismo de ajuste de pesos e retropropagação que a gente descreveu no episódio quatro.

[BIA] E como o treino decide se duas palavras devem ficar perto ou longe uma da outra nesse espaço? Baseado em quê?

[ANA] Baseado no contexto em que cada palavra costuma aparecer. A ideia é: palavras que aparecem cercadas de palavras parecidas, em frases parecidas, tendem a ter significados parecidos. "Gato" e "cachorro" aparecem em frases do tipo "meu animal de estimação faz tal coisa", enquanto "banana" aparece em frases sobre fruta e alimentação. Durante o treino, a rede vai ajustando as coordenadas de cada palavra até que palavras de contexto parecido acabem ficando próximas nesse espaço, e palavras de contexto bem diferente acabem ficando distantes.

[BIA] Isso explica por que "gato" e "cachorro" ficariam perto. Mas eu já ouvi falar que embeddings capturam coisas mais sutis do que só "são do mesmo assunto". Tipo relação entre palavras.

[ANA] Isso é um dos resultados mais interessantes de treinar embeddings numa quantidade gigantesca de texto. A distância e a direção entre "rei" e "rainha" nesse espaço acaba se parecendo bastante com a distância e a direção entre "homem" e "mulher". Ou seja, o espaço não só agrupa palavras parecidas, ele também acaba captando relações, tipo "isso está para aquilo, assim como isso outro está para aquilo outro", sem que ninguém tenha ensinado essa relação explicitamente. Ela emerge sozinha do padrão de uso da língua.

[BIA] Isso é bem impressionante pra algo que ninguém programou à mão. Deixa eu confirmar se entendi certo: cada palavra vira uma lista de números, essa lista funciona como coordenada num espaço com centenas de direções, e o treino ajusta essas coordenadas pra que palavras de contexto parecido fiquem próximas, o que acaba capturando até relações entre palavras, tudo isso sem ninguém decidir manualmente o que cada número significa.

[ANA] Resumiu certinho. E vale destacar uma coisa antes de fechar: essa ideia de embedding não fica restrita a palavra. A mesma lógica, transformar uma coisa em uma lista de números que preserva semelhança, é usada pra imagem, pra som, pra praticamente qualquer tipo de informação que uma rede neural precise processar. Palavra foi só o exemplo de hoje, mas o princípio é bem mais geral.

[BIA] E por que esse assunto específico, embedding de palavra, precisava vir logo antes da gente falar de modelo de linguagem na nossa trilha?

[ANA] Porque agora a gente já tem as duas peças que faltavam se encaixar: dos episódios quatro e cinco, a gente sabe como uma rede neural processa número, em camadas, ajustando peso por retropropagação. E de hoje, a gente sabe como transformar palavra em número de um jeito que preserva significado. Com essas duas peças juntas, já dá pra imaginar uma rede neural recebendo uma frase inteira, palavra por palavra, cada uma já convertida em sua lista de coordenadas.

[BIA] Mas processar palavra por palavra em ordem não parece ainda meio limitado? Tipo, uma frase depende de como as palavras se relacionam entre si, não só de cada palavra isolada.

[ANA] Você acabou de antecipar exatamente o assunto do próximo episódio. No episódio sete a gente vai falar sobre atenção e sobre o Transformer, que é o mecanismo que permite uma rede neural olhar pra uma frase inteira de uma vez e decidir quais palavras devem prestar atenção em quais outras palavras, pra entender o significado completo, não só palavra isolada.

[BIA] Combinado, então. Por hoje é isso, pessoal. Guarda suas dúvidas, porque a gente vai voltar nelas nos próximos episódios.

[ANA] Valeu por ouvir a gente. Até o próximo episódio.
