---
episodio: 003
titulo: Aprendizado supervisionado, não-supervisionado e por reforço
duracao_alvo_min: 12
prereq: [01, 02]
fontes:
  - url: https://www.anthropic.com/research
    nota: "episódio de fundamento da trilha base, sem paper específico — abre a divisão clássica de Machine Learning apresentada como promessa no episódio dois"
---

[ANA] Oi, gente, bem-vindos de volta. Eu sou a Ana.

[BIA] E eu sou a Bia. Recapitulando rapidinho pra quem está chegando agora: no episódio um a gente viu que existem duas linhagens de inteligência artificial, a simbólica, com regras escritas à mão, e a estatística, com o sistema aprendendo padrões sozinho. No episódio dois a gente abriu essa segunda linhagem por dentro, e chamou ela pelo nome técnico: Machine Learning, ou aprendizado de máquina.

[ANA] Isso. E vimos que esse aprendizado tem um processo bem definido: você junta dados, que são exemplos, resume cada exemplo em características que o sistema consegue processar, e treina o sistema mostrando exemplo atrás de exemplo, até ele ajustar o comportamento interno e parar de errar tanto. No final, você separa uma parte dos dados pra testar, garantir que ele generalizou e não só decorou, o que a gente chamou de sobreajuste.

[BIA] E aí o sistema treinado entra na fase de inferência, que é ele já pronto, sendo usado no dia a dia, sem aprender mais nada naquele momento.

[ANA] Exatamente. Só que hoje eu quero puxar um fio que a gente deixou solto de propósito. Lá no episódio dois, todo exemplo que a gente usou vinha com uma etiqueta certa grudada nele. Foto de gato, marcada como "gato". Foto de não gato, marcada como "não é gato". Mas isso não é o único jeito de aprender com dados.

[BIA] Ué, como assim? Se não tem a etiqueta certa junto do exemplo, como o sistema sabe se acertou ou errou?

[ANA] Ótima pergunta, porque é exatamente essa pergunta que separa Machine Learning em três famílias bem diferentes, dependendo do tipo de exemplo que você tem disponível. E é isso que a gente vai destrinchar hoje: aprendizado supervisionado, aprendizado não-supervisionado, e aprendizado por reforço.

[BIA] Vamos por partes, então. Supervisionado primeiro, porque imagino que seja o que a gente já viu até agora.

[ANA] Isso mesmo, é o que a gente já descreveu nos últimos dois episódios, só que agora com o nome certo. Aprendizado supervisionado é quando cada exemplo do seu conjunto de dados vem acompanhado da resposta certa. A palavra "supervisionado" vem daí: alguém, em algum momento, supervisionou o processo, revisando e marcando cada exemplo com o gabarito antes de mostrar pro sistema.

[BIA] Tipo um professor corrigindo exercício antes de devolver pro aluno estudar.

[ANA] É uma boa forma de pensar. E dentro do aprendizado supervisionado ainda tem duas variações que valem a pena distinguir, porque elas aparecem toda hora. A primeira é quando a resposta certa é uma categoria, uma escolha entre opções. Gato ou não gato. Aquele email é spam ou não é spam. Essa doença está presente ou ausente no exame. Isso se chama classificação.

[BIA] Faz sentido, é tipo escolher uma caixinha entre opções pré-definidas.

[ANA] Exatamente. E a segunda variação é quando a resposta certa não é uma categoria, é um número, um valor que pode variar numa escala contínua. Tipo prever o preço de um imóvel, ou quanto tempo uma entrega vai demorar, ou quantos milímetros de chuva vão cair amanhã, em vez de só "vai chover ou não vai". Isso se chama regressão.

[BIA] Deixa eu ver se entendi. Classificação é escolher entre caixinhas, tipo "vai chover, sim ou não". Regressão é estimar um número numa escala, tipo "quantos milímetros". Mas em ambos os casos, o sistema aprendeu olhando exemplos que já vinham com a resposta certa junto.

[ANA] Isso, essa é a característica que define o aprendizado supervisionado inteiro: sempre tem um gabarito disponível durante o treino, seja ele uma categoria ou um número. E é justamente por causa desse gabarito que o sistema consegue comparar a própria resposta com a certa, e se ajustar, do jeito que a gente descreveu no episódio passado.

[BIA] Beleza, entendi supervisionado. E o não-supervisionado, então, é quando não tem gabarito nenhum?

[ANA] É exatamente isso, e é aí que a coisa fica mais interessante. No aprendizado não-supervisionado, você dá pro sistema um monte de exemplos, mas ninguém marcou nada. Não tem etiqueta "gato", não tem etiqueta "não é gato". É só um monte de dados crus.

[BIA] Mas então o que exatamente o sistema faz com isso? Se não tem resposta certa pra comparar, como ele "aprende" alguma coisa?

[ANA] Ele não aprende a prever uma resposta certa, porque essa resposta simplesmente não existe nos dados. O que ele faz, em vez disso, é procurar estrutura escondida: padrões, agrupamentos, semelhanças entre os exemplos, sem que ninguém tenha dito de antemão quais são essas categorias.

[BIA] Me dá um exemplo concreto, porque isso ainda soa abstrato pra mim.

[ANA] Pensa numa loja online com um milhão de clientes. Ninguém sentou e marcou cada cliente com uma categoria tipo "cliente econômico" ou "cliente de luxo". Mas você pode pegar o histórico de compra de cada cliente e pedir pro sistema: separa esses clientes em grupos, de um jeito que clientes parecidos fiquem no mesmo grupo, e clientes diferentes fiquem em grupos diferentes.

[BIA] E o sistema descobre esses grupos sozinho, sem ninguém falar quais grupos existem?

[ANA] Exatamente, isso se chama agrupamento, ou clustering, em inglês. O sistema pode descobrir, por exemplo, que existe um grupo de gente que compra pouco mas com frequência, outro grupo que compra caro raramente, outro que só compra em promoção. Ninguém definiu essas categorias de antemão, elas emergiram dos próprios dados.

[BIA] Isso é bem diferente do exemplo do gato, então. Lá, o objetivo era prever uma etiqueta que já existia. Aqui, o objetivo é descobrir que etiquetas fariam sentido, sem ninguém ter dito quais são.

[ANA] Essa é a diferença central entre as duas famílias, sim. Supervisionado tem uma resposta certa pra perseguir. Não-supervisionado só tem os dados, e a tarefa é encontrar organização onde, à primeira vista, parece que não tem nenhuma.

[BIA] E onde isso é útil na prática, além de separar clientes em grupos?

[ANA] Aparece bastante em situações onde marcar cada exemplo à mão seria caro demais ou até impossível. Por exemplo, resumir milhões de notícias por assunto, sem ninguém ter que ler e categorizar cada uma manualmente. Ou detectar transações bancárias fora do padrão, sem que exista uma lista prévia de "isso é fraude, isso não é", porque fraudes novas aparecem o tempo todo, de jeitos que ninguém catalogou ainda.

[BIA] Ah, interessante, então dá pra usar até pra achar coisa esquisita, coisa que foge do padrão comum, mesmo sem saber de antemão o que é "esquisito".

[ANA] Exatamente, isso é outro uso comum do aprendizado não-supervisionado, chamado de detecção de anomalias. O sistema aprende como é o padrão normal dos dados, e depois sinaliza qualquer coisa que fuja bastante desse padrão, mesmo sem ter visto um exemplo rotulado daquele tipo específico de anomalia antes.

[BIA] Beleza, entendi as duas primeiras famílias. Agora fiquei curiosa com a terceira. Aprendizado por reforço parece o nome mais estranho dos três.

[ANA] O nome é estranho mesmo, mas a ideia por trás é bem intuitiva, porque é parecida com como a gente aprende várias coisas na vida real. Nas duas famílias anteriores, o sistema recebe um conjunto de dados prontos, seja com etiqueta ou sem, e aprende observando esse conjunto inteiro. No aprendizado por reforço, não existe esse conjunto de dados pronto de antemão.

[BIA] Não tem dados prontos? Então de onde vêm os exemplos?

[ANA] O sistema, nesse caso chamado de agente, aprende interagindo com um ambiente, ao vivo, tentando ações e recebendo consequências. Ele faz uma ação, o ambiente responde de algum jeito, e essa resposta vem junto com um sinal de recompensa ou de punição. O agente vai ajustando o comportamento dele pra buscar mais recompensa e menos punição ao longo do tempo.

[BIA] Isso parece o jeito como a gente ensina um cachorro a fazer truque. Ele tenta um comportamento, se acerta ganha um petisco, se erra não ganha nada, e com o tempo ele vai repetindo mais o que dá petisco.

[ANA] É uma analogia excelente, e não é à toa, porque o nome "reforço" vem justamente da psicologia, da ideia de reforçar um comportamento repetindo a recompensa que segue ele. Um exemplo bem usado pra explicar isso é um sistema aprendendo a jogar um jogo de videogame do zero, sem ninguém explicar as regras. Ele só sabe que certas ações aumentam a pontuação, e outras derrubam a pontuação ou terminam o jogo.

[BIA] E ele vai testando ações à toa no começo?

[ANA] No começo sim, bem parecido com o chute aleatório que a gente descreveu no episódio passado sobre o começo do treino supervisionado. Só que aqui, em vez de comparar com uma resposta certa fixa, o agente vai testando ações, observando se a recompensa aumentou ou diminuiu, e ajustando a estratégia dele pra repetir mais as ações que trouxeram recompensa.

[BIA] E isso funciona só pra jogo, ou aparece em outros lugares também?

[ANA] Aparece em várias situações onde a ideia central é tomar uma sequência de decisões, e não só prever uma resposta isolada. Robôs aprendendo a andar, tentando várias formas de mover as pernas até achar uma que não derruba o robô. Sistemas que decidem lances de compra e venda automatizados. E, um exemplo que vai ficar bem relevante mais pra frente nesse podcast, é uma peça importante de como certos assistentes de conversa são ajustados depois do treino inicial deles, mas isso a gente guarda pra um episódio futuro, quando já tiver todo o resto da base montada.

[BIA] Combinado, guardo essa curiosidade pra mais tarde então. Deixa eu tentar juntar as três famílias num resumo, pra fechar. Supervisionado é quando cada exemplo já vem com a resposta certa, e o sistema aprende a prever essa resposta, seja ela uma categoria, que é classificação, ou um número, que é regressão.

[ANA] Isso.

[BIA] Não-supervisionado é quando os dados não têm resposta certa nenhuma, e o sistema procura estrutura escondida sozinho, tipo agrupar exemplos parecidos ou encontrar o que foge do padrão.

[ANA] Perfeito.

[BIA] E por reforço é quando não existe um conjunto de dados pronto de jeito nenhum. O sistema, chamado de agente, aprende interagindo com um ambiente, tentando ações, e ajustando o comportamento a partir de recompensa e punição, parecido com ensinar um truque pra um cachorro.

[ANA] Resumiu tudo certinho. E vale fechar dizendo uma coisa: essas três famílias não são caixinhas totalmente isoladas. Na prática, sistemas modernos às vezes misturam ideias das três, principalmente quando a gente chegar nos modelos de linguagem, mais pra frente na trilha. Mas entender essa divisão clássica agora vai te ajudar a reconhecer, episódio após episódio, qual dessas lógicas está por trás de cada técnica nova que a gente for apresentando.

[BIA] E no próximo episódio a gente vai entrar num assunto que até agora a gente só tratou meio por fora: o que realmente é uma rede neural por dentro. O neurônio, as camadas, e como o ajuste que a gente descreveu no episódio dois efetivamente acontece dentro desse tipo de sistema.

[ANA] Isso, o episódio quatro vai se chamar "Redes neurais: o neurônio, camadas, backpropagation", e a gente promete de novo: sem fórmula na tela, tudo explicado por ideia, não por conta.

[BIA] Combinado. Por hoje é isso, pessoal. Guarda suas dúvidas, porque a gente vai voltar nelas nos próximos episódios.

[ANA] Valeu por ouvir a gente. Até o próximo episódio.
