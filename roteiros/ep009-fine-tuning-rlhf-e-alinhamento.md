---
episodio: 009
titulo: "Fine-tuning, RLHF e alinhamento"
duracao_alvo_min: 12
prereq: [01, 02, 03, 04, 05, 06, 07, 08]
fontes:
  - url: https://www.anthropic.com/research
    nota: "episódio de fundamento da trilha base, sem paper específico — explica como um LLM pré-treinado (ep08) vira um assistente que segue instrução, usando ajuste fino supervisionado e RLHF, retomando o aprendizado por reforço apresentado no episódio três"
---

[ANA] Oi, gente, bem-vindos de volta. Eu sou a Ana.

[BIA] E eu sou a Bia. Recapitulando rapidinho: no episódio oito a gente viu o que é um Modelo de Linguagem de Grande Escala, ou LLM. Vimos que ele quebra texto em tokens, transforma cada token num embedding, processa tudo com atenção dentro de um Transformer, e que ele é treinado, no pré-treino, adivinhando o próximo token repetidamente sobre uma quantidade gigantesca de texto.

[ANA] Isso. E terminei aquele episódio com uma ressalva importante: um modelo que só passou pelo pré-treino sabe continuar texto de um jeito fluente, mas ele não nasce sabendo se comportar como assistente. Ele não aprendeu a seguir instrução, nem a saber quando deve recusar um pedido perigoso. Ele só aprendeu a prever o próximo pedaço de texto plausível, dado tudo que veio antes.

[BIA] Lembro sim, você até deu a entender que tem uma etapa inteira depois disso. Como assim, "prever texto plausível" não é a mesma coisa que responder direito?

[ANA] Pensa assim: se você pega um modelo só pré-treinado e manda a pergunta "qual é a capital da França?", ele não necessariamente responde "Paris". Ele pode, com a mesma naturalidade, continuar o texto como se estivesse copiando uma lista de perguntas de prova, e devolver outra pergunta parecida, porque isso também é um jeito plausível de continuar aquele texto. Ele não tem noção de que deveria responder, porque ninguém pediu isso a ele diretamente durante o pré-treino, só pediu pra prever o próximo token.

[BIA] Ah, entendi. Ele aprendeu a imitar o estilo de texto que viu, mas não aprendeu o comportamento específico de "alguém fez uma pergunta, hora de responder ela".

[ANA] Exatamente essa é a lacuna. E é isso que a etapa de hoje resolve, em duas partes: primeiro o ajuste fino supervisionado, depois uma técnica chamada RLHF. Vamos por partes, começando pelo ajuste fino.

[BIA] Beleza. E "ajuste fino" aqui quer dizer o quê, exatamente? Um treino novo do zero?

[ANA] Não, nada do zero. Lembra que no episódio dois a gente descreveu treino como mostrar exemplo atrás de exemplo pro sistema, comparando a resposta dele com um gabarito, e ajustando os pesos por retropropagação, aquilo que vimos no episódio quatro? Pois o ajuste fino é exatamente isso, só que aplicado em cima de um modelo que já passou pelo pré-treino, não usando aquela montanha de texto genérico da internet, mas um conjunto bem menor e muito mais cuidadosamente escolhido de exemplos.

[BIA] E que tipo de exemplo entra nesse conjunto menor?

[ANA] Pares de instrução e resposta ideal, escritos ou selecionados por gente treinada pra isso. Uma pergunta, seguida da resposta que a gente gostaria que um assistente desse. Um pedido, seguido de como atender esse pedido direito. Isso é aprendizado supervisionado, aquele que a gente descreveu lá no episódio três: cada exemplo já vem com o gabarito grudado, só que agora o gabarito não é "gato ou não gato", é "esse é o jeito certo de responder a essa instrução".

[BIA] Então o modelo continua sendo ajustado do mesmo jeito de sempre, só que agora aprendendo especificamente o formato de pergunta e resposta, em vez de só continuar texto solto.

[ANA] Isso mesmo. Depois dessa etapa, o modelo já se comporta muito mais como assistente: responde pergunta em vez de só continuar ela, segue instrução, mantém um formato de conversa. Mas ainda sobra um problema, e é um problema real: pra várias instruções, não existe uma única resposta certa e objetiva pra colocar nesse conjunto de exemplos.

[BIA] Como assim, não existe resposta certa? Não dá só pra escrever a resposta ideal pra cada instrução possível?

[ANA] Pensa numa instrução tipo "explica esse conceito de um jeito simples" ou "escreve esse email de um jeito educado, mas direto". Tem várias respostas boas possíveis, e a diferença entre elas é de qualidade, tom, clareza, coisas difíceis de resumir num único gabarito fixo. Escrever manualmente exemplo suficiente pra cobrir toda essa nuance, pra todo tipo de pedido que existe, seria impossível na prática.

[BIA] Entendi o problema. Então como vocês resolvem isso, se não dá pra simplesmente escrever mais exemplos?

[ANA] Aqui é onde entra a segunda etapa, RLHF, sigla em inglês pra Aprendizado por Reforço com Realimentação Humana. E pra explicar ela, eu preciso puxar de volta uma ideia do episódio três: o aprendizado por reforço, lembra? Aquele em que existe um agente que tenta ações, recebe recompensa ou punição, e ajusta o comportamento pra buscar mais recompensa.

[BIA] Lembro, foi a terceira família que a gente viu, com o exemplo do cachorro aprendendo truque com petisco. E você tinha deixado escapar, bem no fim daquele episódio, que isso ia aparecer de novo mais pra frente, ligado a assistente de conversa.

[ANA] Exatamente esse é o momento. No RLHF, o próprio LLM, já depois do ajuste fino supervisionado, vira o agente. A ação dele é gerar uma resposta pra uma instrução. E a recompensa vem de gente de verdade avaliando a qualidade dessa resposta.

[BIA] Peraí, uma pessoa avalia cada resposta gerada, uma por uma, ao vivo? Isso não seria impossivelmente lento?

[ANA] Boa desconfiança, e não, não é assim que funciona na prática. O processo tem um passo intermediário. Primeiro, o modelo gera várias respostas diferentes pra mesma instrução. Avaliadores humanos comparam essas respostas entre si, e apontam qual preferem, sem precisar escrever a resposta ideal do zero, só decidir "essa aqui é melhor que aquela". Depois, esses julgamentos de preferência são usados pra treinar um segundo sistema, separado do LLM principal, chamado de modelo de recompensa.

[BIA] Um modelo de recompensa? Explica melhor o que esse segundo modelo faz.

[ANA] Ele é treinado, com aprendizado supervisionado de novo, pra aprender a prever, dado um texto de resposta, o quanto uma pessoa provavelmente gostaria dela, imitando aquelas comparações que os avaliadores humanos fizeram. Uma vez treinado, esse modelo de recompensa consegue dar uma nota pra qualquer resposta nova, sem precisar de uma pessoa avaliando ao vivo cada vez.

[BIA] Ah, entendi a jogada. Em vez de precisar de gente avaliando cada resposta gerada durante todo o treino, vocês treinam um avaliador automático que aprendeu a imitar o gosto humano, e usam ele em escala.

[ANA] Exatamente essa é a peça que destrava tudo. E é só depois disso que o aprendizado por reforço de fato entra: o LLM gera respostas, o modelo de recompensa dá uma nota pra cada uma, e o LLM tem os próprios pesos ajustados pra aumentar a chance de gerar respostas que ganhem nota alta desse avaliador automático, do mesmo jeito que o agente do episódio três ajustava o comportamento pra buscar mais recompensa.

[BIA] Deixa eu tentar montar o quadro completo. Primeiro vem o pré-treino, prevendo o próximo token numa montanha de texto. Depois vem o ajuste fino supervisionado, com pares de instrução e resposta ideal, ensinando o formato de assistente. E por último vem o RLHF, onde um modelo de recompensa aprende o gosto humano por comparação, e o LLM é empurrado, por reforço, a gerar respostas que esse avaliador automático nota bem.

[ANA] Resumiu certinho, essas são as três etapas. E o nome que a gente dá pro objetivo de tudo isso junto, ajuste fino e RLHF, é alinhamento: fazer o comportamento do modelo corresponder ao que a gente pretende, e não só ao que ele aprendeu a imitar olhando texto da internet. Um modelo alinhado tende a ser mais útil, mais honesto sobre o que sabe e o que não sabe, e mais cuidadoso em recusar pedido que possa causar dano.

[BIA] Isso quer dizer que, depois do RLHF, o modelo fica perfeito, sem erro nenhum desse tipo?

[ANA] Não, de jeito nenhum, e essa ressalva importa. Alinhamento reduz bastante esse tipo de comportamento indesejado, mas não elimina por completo. O modelo de recompensa é, ele mesmo, uma aproximação imperfeita do gosto humano, treinada com uma quantidade limitada de comparação. Às vezes o LLM encontra um jeito de agradar esse avaliador automático sem de fato melhorar a resposta pra quem está do outro lado conversando. E existem limites de como avaliar isso direito, que a gente vai guardar pra um episódio mais à frente, sobre avaliação e limites dos modelos.

[BIA] Combinado, guardo essa curiosidade pra lá então. E o que vem no próximo episódio?

[ANA] No episódio dez a gente vai falar de RAG, sigla em inglês pra Geração Aumentada por Recuperação. É a técnica que resolve um problema bem diferente desse de hoje: mesmo um modelo bem alinhado só sabe o que estava no texto que ele viu durante o pré-treino, então ele não tem acesso nem a informação nova, publicada depois daquele treino, nem a documento privado seu. RAG é como a gente ensina o modelo a ir buscar informação de fora antes de responder, em vez de depender só do que ele já tem guardado.

[BIA] Combinado. Por hoje é isso, pessoal. Guarda suas dúvidas, porque a gente vai voltar nelas nos próximos episódios.

[ANA] Valeu por ouvir a gente. Até o próximo episódio.
