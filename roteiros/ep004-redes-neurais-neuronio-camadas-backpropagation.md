---
episodio: 004
titulo: "Redes neurais: o neurônio, camadas, backpropagation"
duracao_alvo_min: 12
prereq: [01, 02, 03]
fontes:
  - url: https://www.anthropic.com/research
    nota: "episódio de fundamento da trilha base, sem paper específico — abre por dentro o mecanismo de ajuste que os episódios dois e três trataram por fora"
---

[ANA] Oi, gente, bem-vindos de volta. Eu sou a Ana.

[BIA] E eu sou a Bia. Recapitulando rapidinho: no episódio dois a gente viu o que é treinar um sistema, mostrar exemplo atrás de exemplo e deixar ele ajustar um comportamento interno até errar cada vez menos. No episódio três a gente separou isso em três famílias, dependendo do tipo de exemplo disponível: supervisionado, quando tem resposta certa; não-supervisionado, quando não tem; e por reforço, quando o sistema aprende interagindo com um ambiente.

[ANA] Isso. Só que em nenhum dos três episódios a gente abriu o que realmente existe dentro desse "sistema" que aprende. A gente falou em "comportamento interno" e "ajuste" como se fossem uma caixa fechada. Hoje a gente abre essa caixa. E o tipo de sistema mais comum por trás disso, hoje em dia, chama-se rede neural.

[BIA] Rede neural. Isso tem a ver com neurônio de cérebro mesmo, ou é só um nome bonito?

[ANA] Tem uma inspiração vaga no cérebro biológico, sim, mas é bem mais simples do que isso. Pensa num neurônio artificial como uma peça bem pequena, quase burra sozinha, que faz só uma coisa: recebe alguns sinais de entrada, decide o quanto cada um desses sinais importa, soma tudo isso ponderado por essa importância, e manda um sinal de saída pra frente.

[BIA] Deixa eu tentar traduzir isso num exemplo, porque "sinal" e "importância" ainda tá abstrato pra mim.

[ANA] Vamos voltar no exemplo do gato. Imagina um neurônio que recebe três sinais de entrada: um que mede "quanto essa imagem tem pelo", outro que mede "quanto ela tem formato de orelha triangular", e outro que mede "quanto ela tem bigode". Esse neurônio pode dar bastante importância pro sinal de "orelha triangular" e pouca importância pro sinal de "pelo", porque cachorro também tem pelo, mas orelha triangular pontuda é mais específico de gato.

[BIA] Ah, entendi. Então essa "importância" que cada sinal recebe é justamente aquilo que muda durante o treino, aquele ajuste que a gente descreveu no episódio dois?

[ANA] Exatamente essa é a peça que faltava encaixar. Esse "quanto de importância" tem até um nome técnico, chama-se peso. E treinar uma rede neural é, no fundo, ir ajustando esses pesos, repetidamente, até o neurônio aprender a dar mais importância aos sinais que realmente ajudam a acertar, e menos importância aos que não ajudam.

[BIA] Beleza, entendi um neurônio sozinho. Mas "rede" sugere que tem vários deles conectados. Como isso funciona junto?

[ANA] É aí que entra a segunda ideia de hoje: camadas. Uma rede neural moderna não tem só um neurônio, ela tem milhares ou milhões deles, organizados em grupos, um atrás do outro. Cada grupo se chama camada.

[BIA] E por que organizar em grupos, em vez de todo mundo solto?

[ANA] Porque cada camada recebe a saída da camada anterior como sua própria entrada, e isso permite que a rede construa conceitos cada vez mais complexos, um em cima do outro. A primeira camada, chamada de camada de entrada, recebe a imagem bruta. As camadas do meio, chamadas de camadas ocultas, vão combinando sinais simples em sinais mais elaborados. E a última camada, chamada de camada de saída, entrega a resposta final, tipo "gato" ou "não é gato".

[BIA] Me dá um exemplo de como isso vai ficando mais elaborado, camada por camada.

[ANA] Numa rede que processa imagens, por exemplo, as primeiras camadas costumam aprender a detectar coisas bem simples, tipo bordas e mudanças bruscas de cor num pedacinho pequeno da imagem. As camadas do meio combinam essas bordas em formas, tipo um círculo ou um triângulo. E as camadas mais perto do final combinam essas formas em conceitos inteiros, tipo "isso parece uma orelha", até a última camada juntar tudo isso numa resposta só.

[BIA] Então cada camada é meio que um andar de um prédio, onde o andar de cima usa o que o andar de baixo já resumiu, em vez de olhar a imagem bruta de novo.

[ANA] Essa é uma analogia ótima. E repara que isso resolve um problema que a gente comentou lá no episódio dois: naquela época, eu disse que sistemas antigos precisavam de um humano escolhendo à mão quais características prestar atenção, tipo "meça o contorno". Numa rede neural com várias camadas, ninguém escolhe isso à mão. As camadas do meio aprendem sozinhas quais características valem a pena construir, só de serem expostas a muitos exemplos.

[BIA] Isso é bem poderoso. Mas ainda fiquei com uma dúvida prática: como exatamente o ajuste dos pesos acontece, quando o erro só aparece lá na última camada, na resposta final? Como o erro "volta" pras camadas do meio, que nem tocaram na resposta final diretamente?

[ANA] Essa pergunta é exatamente o assunto principal de hoje, porque é a pergunta que ficou sem resposta nos últimos dois episódios. A técnica que resolve isso se chama backpropagation, ou retropropagação do erro, em português. E o nome já entrega a ideia central: o erro se propaga de trás pra frente.

[BIA] "De trás pra frente" como assim, exatamente?

[ANA] Pensa no caminho que um exemplo percorre dentro da rede: ele entra pela camada de entrada, passa pelas camadas ocultas, uma atrás da outra, e sai como resposta na camada de saída. Isso é o caminho de ida. A retropropagação faz o caminho contrário: ela pega o erro que apareceu na saída, e vai devolvendo esse erro pra trás, camada por camada, até chegar na entrada de novo.

[BIA] Mas por que precisa devolver o erro pra trás? Por que não ajustar só a última camada, já que é ela que errou a resposta final?

[ANA] Porque a última camada só errou porque recebeu sinais ruins das camadas anteriores. Se a camada do meio mandou pra frente um sinal fraco de "orelha triangular" numa foto que era claramente de gato, a culpa daquele erro não é só da última camada, é também de como a camada do meio processou aquela imagem. A retropropagação existe justamente pra distribuir a "culpa" do erro entre todas as camadas que participaram da resposta, cada uma recebendo a parcela de ajuste que lhe cabe.

[BIA] Ah, entendi. É tipo um jogo de telefone sem fio ao contrário. Em vez do erro só ficar acumulado na última pessoa que falou errado, a informação de "isso saiu errado, e por quê" volta pra cada pessoa da fila, pra cada uma corrigir sua própria parte.

[ANA] Adorei essa analogia, porque captura bem o espírito. E o resultado prático disso é: depois que o erro terminou de se propagar pra trás, cada peso individual, em cada camada, em cada neurônio, recebe um pequeno ajuste, na direção que teria reduzido aquele erro específico. E isso é feito de novo, e de novo, exemplo atrás de exemplo, exatamente aquele processo de treino que a gente descreveu no episódio dois, só que agora você já sabe o mecanismo exato que torna esse ajuste possível numa rede com várias camadas.

[BIA] Então backpropagation não é uma alternativa ao treino que a gente já tinha visto, é literalmente como o treino acontece por dentro de uma rede neural.

[ANA] Isso, exatamente essa é a peça que faltava. Treino, lá no episódio dois, era o nome geral do processo de mostrar exemplos e ajustar comportamento. Backpropagation é o mecanismo específico que permite fazer esse ajuste numa rede organizada em várias camadas empilhadas, calculando exatamente o quanto cada peso, em cada camada, deveria mudar.

[BIA] E antes do treino começar, esses pesos começam como quê? Zero? Alguma coisa definida?

[ANA] Boa pergunta, e a resposta conecta direto com aquele "chute aleatório" que a gente mencionou no episódio dois, sobre o começo do treino. Os pesos de uma rede neural, antes de qualquer treino, começam com valores praticamente aleatórios. É por isso que uma rede recém-criada, sem treino nenhum, chuta as respostas quase ao acaso. É só depois de muitas rodadas de retropropagação, ajustando esses pesos aleatórios pouco a pouco, que a rede vai deixando de chutar e passando a acertar de verdade.

[BIA] Deixa eu tentar resumir tudo isso, pra fechar o episódio de hoje. Uma rede neural é feita de neurônios artificiais, cada um recebendo sinais de entrada, dando um peso, uma importância, pra cada sinal, e somando tudo isso numa saída.

[ANA] Isso.

[BIA] Esses neurônios ficam organizados em camadas, uma atrás da outra: entrada, camadas ocultas no meio, e saída no final. Cada camada usa o que a anterior já resumiu, o que deixa a rede capaz de construir conceitos cada vez mais complexos sem que ninguém precise escolher essas características à mão.

[ANA] Exatamente.

[BIA] E o ajuste desses pesos, que começam quase aleatórios, acontece através da retropropagação, que pega o erro da resposta final e devolve ele pra trás, camada por camada, distribuindo o tanto de ajuste que cada peso individual precisa receber.

[ANA] Resumiu tudo certinho. E vale fechar dizendo uma coisa importante: isso que a gente descreveu hoje é a base estrutural de praticamente tudo que vem daqui pra frente nesse podcast. Os grandes modelos de linguagem, os sistemas que geram imagem, tudo isso é rede neural, com camadas e retropropagação, só que numa escala muito, muito maior do que qualquer exemplo que a gente usou hoje.

[BIA] E é justamente essa escala que puxa o assunto do próximo episódio, né?

[ANA] Isso mesmo. No episódio cinco a gente vai falar sobre Deep Learning, ou aprendizado profundo, e por que o ano de dois mil e doze mudou tudo nesse campo. A gente vai ver o que muda quando você empilha muito mais camadas do que as redes de antes conseguiam treinar direito, e por que isso destravou uma nova era inteira.

[BIA] Combinado. Por hoje é isso, pessoal. Guarda suas dúvidas, porque a gente vai voltar nelas nos próximos episódios.

[ANA] Valeu por ouvir a gente. Até o próximo episódio.
