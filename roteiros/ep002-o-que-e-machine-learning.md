---
episodio: 002
titulo: O que é Machine Learning?
duracao_alvo_min: 12
prereq: [01]
fontes:
  - url: https://www.anthropic.com/research
    nota: "episódio de fundamento da trilha base, sem paper específico — aprofunda o conceito de aprendizado estatístico apresentado no episódio um"
---

[ANA] Oi, gente, bem-vindos de volta. Eu sou a Ana.

[BIA] E eu sou a Bia. Rapidinho, pra quem está chegando agora: no episódio passado a gente falou sobre os dois grandes caminhos da inteligência artificial. A I A simbólica, que é regra escrita à mão por um humano, e a I A estatística, que é o sistema aprendendo padrões sozinho, olhando muitos exemplos.

[ANA] Isso. E a gente fechou dizendo que quase tudo que existe hoje, os assistentes virtuais, os tradutores automáticos, vem dessa segunda linhagem, a estatística. Só que a gente usou uma palavra várias vezes sem explicar direito o que ela significa de verdade.

[BIA] Deixa eu adivinhar. "Aprender".

[ANA] Exatamente. Hoje o episódio é sobre isso: o que quer dizer, na prática, um computador "aprender" com exemplos. E o nome técnico desse campo inteiro é Machine Learning, ou aprendizado de máquina.

[BIA] Então Machine Learning não é uma coisa nova, é só o nome bonito pra essa ideia de "aprender com exemplos" que a gente já comentou?

[ANA] É basicamente isso, sim. Machine Learning é a área da inteligência artificial que estuda como fazer um sistema melhorar numa tarefa observando dados, em vez de seguir regras fixas escritas por uma pessoa. E pra entender como isso funciona, eu preciso te apresentar três palavras que aparecem toda hora nesse assunto: dados, características e treino.

[BIA] Beleza, vamos por partes. Dados primeiro. Isso é só... informação?

[ANA] É informação organizada em exemplos. Pensa no exemplo que eu dei no episódio passado: um milhão de fotos marcadas como "gato" ou "não é gato". Cada foto, junto com a marcação dela, é um exemplo. E o conjunto de todos esses exemplos é o que chamamos de dados, ou dataset, em inglês.

[BIA] E cada foto individual, com a etiqueta "gato" ou "não é gato" grudada nela, é um exemplo. Tá, entendi. E "características"?

[ANA] Essa é mais sutil. Um computador não "vê" uma foto do jeito que a gente vê. Pra ele, uma foto é só um monte de números, um número pra cada pontinho colorido da imagem. Então, antes de aprender qualquer coisa, o sistema precisa de um jeito de resumir essa imagem em características que sejam úteis pra distinguir gato de não gato.

[BIA] Tipo o quê, por exemplo?

[ANA] Nos sistemas mais antigos, um humano ainda ajudava a escolher isso. Tipo: "meça o formato dos contornos", "meça a distribuição de cores". Mas o pulo do gato dos sistemas modernos, e a gente vai chegar nisso em episódios futuros, é que eles aprendem sozinhos até quais características prestar atenção. Por enquanto, o importante é só entender que existe essa etapa: transformar o exemplo bruto em alguma coisa que o sistema consiga processar.

[BIA] Tá, e "treino" é a parte em que ele efetivamente aprende?

[ANA] Isso, e aqui mora o coração do assunto de hoje. Treinar é o processo de mostrar exemplo atrás de exemplo pro sistema, e deixar ele ajustar um comportamento interno até acertar cada vez mais. No começo desse processo, o sistema erra muito. Ele olha uma foto de gato e chuta, tipo, "cinquenta por cento de chance de ser gato", que é basicamente um chute aleatório.

[BIA] E aí?

[ANA] Aí entra a parte interessante. Depois de cada chute, o sistema compara a resposta dele com a resposta certa, que já vinha junto no exemplo. Se ele errou, ele ajusta um pouquinho o jeito como processa aquele tipo de imagem, pra chegar mais perto do certo da próxima vez. E isso se repete, exemplo atrás de exemplo, milhares ou milhões de vezes.

[BIA] Então é tipo... tentativa e erro, só que em escala gigantesca, e com o sistema corrigindo o próprio rumo a cada erro.

[ANA] É uma boa forma de pensar nisso, sim. Tentativa, comparação com o certo, pequeno ajuste, e repete. E aos poucos, esses pequenos ajustes vão se acumulando até o sistema acertar a esmagadora maioria dos exemplos que já viu.

[BIA] Peraí, mas se ele só está acertando os exemplos que já viu, isso não seria tipo decorar as respostas? Tipo um aluno que decora o gabarito da prova, mas não aprendeu a matéria de verdade?

[ANA] Ótima pergunta, porque isso é exatamente o maior risco de todo esse processo, e tem até um nome pra esse problema: chama-se overfitting, ou, em português, sobreajuste. É quando o sistema decora os exemplos específicos que viu, em vez de aprender o padrão geral por trás deles.

[BIA] E como é que alguém percebe que isso aconteceu?

[ANA] É aí que entra uma prática fundamental de Machine Learning: você nunca usa cem por cento dos seus dados só pra treinar. Você separa uma parte, guardada de lado, escondida do sistema durante o treino inteiro. Depois que o treino termina, você testa o sistema justamente nesses exemplos que ele nunca viu.

[BIA] Ah, entendi, é tipo aplicar uma prova com questões diferentes das que o aluno estudou, pra ver se ele entendeu o assunto ou só decorou.

[ANA] Exatamente essa é a analogia certa. Se o sistema vai bem nos exemplos novos, que ele nunca viu, a gente diz que ele generalizou, ou seja, aprendeu um padrão de verdade, que funciona além dos exemplos originais. Se ele vai mal nos exemplos novos, mas foi muito bem nos exemplos de treino, isso é sinal claro de sobreajuste.

[BIA] E isso me leva a uma pergunta que eu sempre quis entender. Por que tanta gente fala em "fase de treino" e "fase de uso" como se fossem coisas separadas? Não é tudo a mesma coisa, o sistema rodando?

[ANA] Não, são fases bem diferentes, e essa é outra distinção importante de hoje. A fase de treino é quando o sistema ainda está ajustando o comportamento dele, olhando exemplo atrás de exemplo, como a gente descreveu. Isso geralmente acontece uma vez, ou de tempos em tempos, e pode levar de minutos a semanas, dependendo do tamanho do problema.

[BIA] E a fase de uso?

[ANA] A fase de uso, que também é chamada de inferência, é quando o treino já terminou, o comportamento interno do sistema já está fixado, e ele está sendo usado pra fazer previsões em situações reais, do dia a dia. Quando você manda uma mensagem pra um assistente virtual e ele responde na hora, isso é inferência. O aprendizado dele já aconteceu antes, num momento separado.

[BIA] Então é tipo: primeiro o aluno estuda pra prova, isso é o treino. Depois ele faz a prova de verdade, isso é a inferência, e nesse momento ele já não está mais aprendendo, só está aplicando o que sabe.

[ANA] Perfeita analogia. E vale notar uma coisa: durante a inferência, o sistema normalmente não muda mais. Ele responde do mesmo jeito consistente pra situações parecidas, porque o ajuste dele já foi feito e ficou congelado depois do treino.

[BIA] Deixa eu tentar juntar tudo que a gente viu hoje num resumo. Machine Learning é a área que estuda como um sistema aprende com dados, que são exemplos. Cada exemplo é resumido em características que o sistema consegue processar. O treino é o processo de mostrar exemplos repetidamente e ajustar o comportamento interno a cada erro. A gente sempre separa uma parte dos dados pra testar depois, pra garantir que o sistema generalizou, e não só decorou, o que seria sobreajuste. E depois do treino vem a inferência, que é o sistema já pronto sendo usado no dia a dia, sem aprender mais nada novo naquele momento.

[ANA] Resumiu tudo certinho. E é importante fechar dizendo: tudo isso que a gente descreveu hoje, dados, treino, generalização, é a base de absolutamente tudo que vem depois nesse podcast. Redes neurais, os grandes modelos de linguagem, tudo é uma variação mais sofisticada desse mesmo processo básico de aprender com exemplos.

[BIA] E no próximo episódio a gente vai abrir uma divisão importante dentro de Machine Learning: os diferentes jeitos de aprender, dependendo do tipo de exemplo que você tem disponível.

[ANA] Isso, o episódio três vai se chamar "Aprendizado supervisionado, não-supervisionado e por reforço", e a gente vai destrinchar essas três famílias, sempre sem matemática, prometido.

[BIA] Combinado. Por hoje é isso, pessoal. Guarda suas dúvidas, porque a gente vai voltar nelas nos próximos episódios.

[ANA] Valeu por ouvir a gente. Até o próximo episódio.
