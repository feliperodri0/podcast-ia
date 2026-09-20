---
episodio: 018
titulo: "Pesos de interferência: o ruído escondido dentro de um modelo pequeno"
duracao_alvo_min: 13
prereq: [04, 07, 14]
fontes:
  - url: https://transformer-circuits.pub/2026/interference_effectiveness_helpfulness/index.html
    nota: "continuação direta do episódio dezessete: usa os conceitos de recurso interno e circuito da interpretabilidade mecanicista, junto com pesos do episódio quatro e o transformer do episódio sete, pra caracterizar pesos de interferência dentro de um modelo de fato treinado, não só num modelo de brinquedo"
---

[ANA] Oi, gente, bem-vindos de volta. Eu sou a Ana.

[BIA] E eu sou a Bia. Recapitulando rapidinho: no episódio dezessete a gente abriu o capô de um modelo de linguagem pela primeira vez de verdade. Vimos que interpretabilidade é o campo que estuda o que acontece dentro de um modelo examinando diretamente os números internos, em vez de confiar só no texto que ele escreve sobre o próprio raciocínio. Aprendemos dois conceitos centrais: recurso interno, um padrão de ativação espalhado por vários neurônios que representa uma ideia, tipo aquele exemplo da Golden Gate Bridge; e circuito, uma cadeia de recursos internos conectados, onde um influencia o próximo até produzir um comportamento do modelo. E terminamos prometendo que o episódio dezoito seria sobre avaliação e limites, tipo alucinação e testes de segurança.

[ANA] Prometemos, e a gente ainda vai chegar lá, só que não hoje. Saiu um paper novo bem na área de interpretabilidade, do mesmo grupo Transformer Circuits que a gente citou como fonte no episódio passado, e ele encaixa direto na pergunta que ficou no ar: será que dá pra olhar direto pras conexões entre os recursos internos, tipo ler um circuito elétrico, e entender o comportamento do modelo sem nem precisar rodar ele? Então o episódio de avaliação vira o dezenove, e o de hoje conta essa história.

[BIA] Peraí, "conexões entre os recursos internos", isso é a mesma coisa que peso, aquele número que a gente descreveu lá no episódio quatro, dentro da soma que cada neurônio artificial faz?

[ANA] É exatamente essa ideia, só que aplicada não entre neurônio e neurônio, mas entre recurso interno e recurso interno, ou entre recurso interno e a próxima peça de texto que o modelo está prestes a escolher. Cada uma dessas conexões tem um número associado, que diz o quanto uma coisa empurra a outra. E a esperança antiga da interpretabilidade é justamente essa: se alguém conseguisse listar todas essas conexões, teria uma espécie de esquema elétrico completo do modelo, e poderia ler o comportamento dele como quem lê um programa de computador, sem precisar rodar nada.

[BIA] E por que isso não é simplesmente óbvio de fazer? Se a conexão já existe dentro do modelo, por que não só listar elas e pronto?

[ANA] Porque, como a gente comentou no episódio dezessete sem batizar ainda, um modelo espreme várias ideias diferentes no mesmo espaço pequeno de neurônios, em vez de dar um neurônio exclusivo pra cada conceito. Isso tem nome: superposição. E a superposição não afeta só os neurônios individuais, ela também contamina as conexões entre os recursos internos que os pesquisadores reconstroem a partir deles. O resultado é que, quando alguém calcula a força de uma conexão entre dois recursos, às vezes esse número é gigante e chamativo, mas não representa nada de real que o modelo aprendeu. É só um efeito colateral de tudo estar espremido junto.

[BIA] Isso soa contraintuitivo. Uma conexão forte que não significa nada?

[ANA] Exatamente, e os pesquisadores deram um nome pra isso: peso de interferência. É uma conexão que existe matematicamente, tem um número grande associado a ela, mas na prática não corresponde a nenhuma regra real que o modelo usa, só ruído deixado pelo espremimento da superposição. E o motivo de esse paper importar é que, até agora, esse tipo de peso só tinha sido demonstrado dentro de um modelo de brinquedo, bem artificial, criado só pra ilustrar a ideia. Dessa vez, pela primeira vez, os pesquisadores acharam um exemplo real, mensurável, dentro de um modelo de linguagem treinado do jeito normal.

[BIA] Dá pra descrever um exemplo concreto desses, tipo o da Golden Gate Bridge do episódio passado?

[ANA] Dá, e o exemplo deles é ótimo justamente por ser bem simples de acompanhar. Os pesquisadores treinaram um modelo pequeno, de propósito, com só uma camada de processamento, pra conseguir examinar cada conexão dele com precisão. E pegaram um momento em que esse modelo estava no meio de completar a palavra "acetilcolina", uma substância química do corpo, letra por letra. Depois das letras "I" e "N", o modelo precisa escolher a próxima letra, que no caso certo é "E". E o modelo realmente acerta, escolhe "E".

[BIA] Então funcionou. Qual é o problema?

[ANA] O problema aparece quando os pesquisadores abrem o capô desse acerto. Existe, dentro do modelo, uma conexão bem forte, bem "gritante" em termos de número, que liga essas mesmas letras "I" e "N" a uma continuação completamente diferente, uma terminação que nunca aparece depois de "IN" em nenhum texto usado no treino do modelo. Ou seja: essa conexão específica é grande, chamativa, mas está sempre errada. Sempre que ela pesa na decisão, ela puxa pro lado errado. Isso é candidato perfeito a peso de interferência.

[BIA] Então como os pesquisadores decidem quais conexões são dessas "gritantes, mas erradas", separando elas das conexões que realmente fazem o modelo funcionar direito?

[ANA] Eles criaram duas perguntas pra fazer sobre cada conexão, sem precisar de fórmula nenhuma pra entender a ideia. A primeira pergunta é: essa conexão realmente influencia a resposta final do modelo, ou ela é "gritante" mas acaba sendo ignorada, porque outras conexões competem e vencem? Isso os pesquisadores chamaram de efetividade. Uma conexão pode ter um número gigante associado a ela e, mesmo assim, quase nunca mudar a resposta final, porque sempre que ela tenta empurrar pra um lado, outras conexões mais numerosas empurram mais forte pro lado oposto.

[BIA] Tipo uma pessoa gritando alto numa sala cheia de gente, mas que ninguém escuta porque todo mundo mais tá falando ao mesmo tempo, mais alto ainda?

[ANA] É uma boa imagem. E a segunda pergunta só faz sentido pra quem já passou no primeiro teste, quem realmente tem efeito real na resposta: quando essa conexão empurra a resposta, ela empurra pro lado certo ou pro lado errado? Isso eles chamaram de utilidade. Uma conexão pode ser bem efetiva, mudar bastante a resposta, e mesmo assim ser prejudicial, porque empurra sempre na direção errada, como aquela conexão de "IN" pra terminação que nunca acontece.

[BIA] E aí, medindo essas duas coisas num monte de conexões, o que eles descobriram?

[ANA] Descobriram três coisas, e a primeira delas é meio desconfortável pra quem queria um atalho fácil. Conexões úteis e conexões prejudiciais aparecem espalhadas por toda a faixa de tamanho de número, do menor ao maior. Ou seja: não dá pra simplesmente olhar pras conexões "mais gritantes" achando que são as mais importantes, porque tem conexão gigante que é pura interferência, e tem conexão pequena que carrega uma regra real do modelo.

[BIA] Então tamanho sozinho não é um guia confiável.

[ANA] Não é, mas aí vem a segunda descoberta, que já é mais animadora. Quando os pesquisadores usam a efetividade, aquela primeira pergunta sobre influência real, pra ordenar as conexões, o quadro muda bastante. Eles conseguiram apagar as setenta por cento de conexões menos efetivas do modelo, e a qualidade do texto que ele gera quase não mudou. Apagando até oitenta e cinco por cento das conexões menos efetivas, a qualidade ainda ficava bem perto da original, só um pouquinho pior. E mais: entre as conexões que sobraram, as mais efetivas de todas eram, disparado, as mais úteis, superando qualquer conexão prejudicial em força por uma margem enorme.

[BIA] Isso é uma boa notícia. Parece que dá sim pra limpar bastante ruído.

[ANA] Dá, e é um resultado real, não só teórico. Só que aí entra a terceira descoberta, que é a que deixa o assunto mais honesto, e explica por que o sonho antigo da interpretabilidade ainda não virou realidade. Mesmo depois de toda essa limpeza, mesmo olhando só pras conexões mais efetivas e mais úteis, ainda sobra um número gigantesco de conexões reais pra examinar, uma por uma. Nesse modelinho de brinquedo, tão pequeno, o número de conexões úteis que sobrou depois da limpeza já é maior do que o número total de peças ajustáveis que o modelo original tinha desde o início.

[BIA] Espera, isso não devia estar ficando mais simples? Como a versão "limpa" pode ter mais peça do que a versão original?

[ANA] Porque, pra conseguir examinar as conexões entre recursos internos, os pesquisadores precisam expandir o modelo numa versão bem maior, escrita numa forma que dá pra examinar conexão por conexão, coisa que o modelo original, na sua forma compacta, não deixa fazer diretamente. Essa expansão multiplica bastante o número de peças visíveis. E mesmo removendo a maior parte do que é claramente interferência, ainda sobra muita coisa genuína, útil, mas numerosa demais pra alguém simplesmente ler cada conexão à mão e entender o modelo inteiro de uma vez.

[BIA] Então, resumindo o resultado pra quem só quer saber "e aí, conseguiram ler o modelo feito um programa de computador ou não?"

[ANA] A resposta honesta é: parcialmente, e é isso que torna esse paper valioso, mesmo sem ser um "eureca" completo. Ele prova, pela primeira vez dentro de um modelo de verdade, que peso de interferência realmente existe e pode ser identificado, não é só uma teoria. Ele mostra uma forma prática de separar, ao menos em boa parte, o ruído da superposição das regras reais que o modelo aprendeu. E, ao mesmo tempo, mostra o tamanho do desafio que ainda falta: mesmo num modelo minúsculo, escolhido de propósito pra ser fácil de examinar, o número de conexões reais que sobram depois da limpeza ainda é grande demais pra virar um mapa legível por uma pessoa.

[BIA] E é por isso que o pessoal do Transformer Circuits, que a gente citou como fonte lá no episódio dezessete, continua tentando achar outro jeito de organizar essas conexões, não é? Melhorar a forma de agrupar, não só de limpar.

[ANA] Exatamente essa é a conclusão que os próprios pesquisadores tiram no fim do artigo. Eles suspeitam que o problema não é só quantidade de ruído pra remover, é também a forma como as conexões estão organizadas hoje. Talvez, reorganizando os recursos internos de outro jeito, uma versão futura dessa mesma limpeza consiga chegar, de fato, a um circuito pequeno o bastante pra alguém ler do início ao fim. Mas essa parte ainda é trabalho futuro, não algo que esse paper resolveu.

[BIA] Resumindo pra fechar: hoje a gente viu que pesos, aquelas conexões entre partes do modelo que já conhecíamos desde o episódio quatro, também sofrem com a superposição, o mesmo espremimento de conceitos que vimos no episódio dezessete. Isso cria pesos de interferência, conexões que parecem fortes mas não significam nada real, como aquela ligação entre "IN" e uma terminação que nunca acontece. Pesquisadores mediram cada conexão por dois critérios, efetividade e utilidade, e confirmaram que dá pra apagar boa parte do ruído sem perder muita qualidade. Mas mesmo depois da limpeza, sobra conexão real demais pra ler à mão, o que mostra que o sonho de ler um modelo feito um programa de computador ainda está longe, mesmo num modelo minúsculo.

[ANA] Essa é a síntese certa. E com essa mistura de progresso real e desafio ainda grande pela frente, a gente fecha o episódio de hoje. No próximo, o dezenove, a gente finalmente volta pro fio principal da trilha, com uma pergunta bem prática: se um modelo pode alucinar, ou se comportar mal, como alguém avalia, de um jeito confiável, se ele está bom o suficiente pra confiar nele?

[BIA] Combinado, dessa vez eu cobro se deixarem passar de novo.

[ANA] Combinado. Por hoje é isso, pessoal. Guarda suas dúvidas, porque a gente vai voltar nelas nos próximos episódios.

[BIA] Valeu por ouvir a gente. Até o próximo episódio.
