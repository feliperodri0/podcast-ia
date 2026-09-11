---
episodio: 015
titulo: "Raciocínio: chain-of-thought e modelos de reasoning"
duracao_alvo_min: 12
prereq: [07, 08, 09, 11]
fontes:
  - url: https://www.anthropic.com/research
    nota: "episódio de fundamento da trilha base, sem paper específico — explica chain-of-thought e modelos de reasoning como resposta ao limite de previsão token a token descrito no episódio oito, reaproveitando os conceitos de atenção do episódio sete, de LLM do episódio oito, de treino por reforço do episódio nove e de ciclo iterativo do episódio onze"
---

[ANA] Oi, gente, bem-vindos de volta. Eu sou a Ana.

[BIA] E eu sou a Bia. Recapitulando rapidinho: no episódio quatorze a gente contou que a Anthropic testou o próprio Claude como pesquisador de alinhamento, e que esse método automatizado conseguiu corrigir falhas como comportamento enganoso melhor do que o melhor método humano, com muito menos dado de treino. E, antes disso, no episódio treze, a gente já tinha prometido que o assunto seguinte seria raciocínio e os modelos chamados de reasoning.

[ANA] Prometemos duas vezes seguidas, e dessa vez é pra valer. Hoje a gente volta pro fio principal da trilha, e o assunto é exatamente esse: como um modelo de linguagem "pensa" antes de responder, e o que muda quando esse processo de pensar fica visível no meio da própria resposta.

[BIA] Antes de entrar no raciocínio em si, deixa eu confirmar uma coisa que ficou solta lá do episódio oito: um Modelo de Linguagem de Grande Escala, o LLM, não decidia a resposta inteira de uma vez, certo? Ele ia prevendo um token de cada vez?

[ANA] Isso mesmo, e é exatamente daí que a gente parte hoje. Token, se você lembra, é o pedacinho de texto, tipo um fragmento de palavra, que o modelo prevê um de cada vez, sempre olhando pra tudo que já foi escrito antes, usando aquele mecanismo de atenção que a gente descreveu no episódio sete. O problema aparece quando a pergunta é difícil, e exige vários passos de raciocínio até chegar na resposta certa.

[BIA] Por que isso vira um problema? O modelo não pode simplesmente prever o próximo token, e o próximo, e assim por diante, até terminar a resposta certa?

[ANA] Pode, mas repara numa coisa: se a primeira coisa que o modelo escreve já é a resposta final, ele só teve aquele único token, gerado num único passo, pra "decidir" o resultado de um problema que talvez precisasse de vários passos de raciocínio encadeados. É como se alguém te fizesse uma pergunta complicada, de várias etapas, e exigisse que você respondesse o número final na primeira palavra que sai da sua boca, sem poder pensar antes ou fazer nenhuma conta no caminho.

[BIA] Ih, eu erraria bastante assim. Eu preciso quebrar o problema em pedaços, resolver um de cada vez, e só aí juntar tudo pra dar a resposta final.

[ANA] Exatamente essa é a saída que os pesquisadores encontraram, e ela ganhou o nome de chain-of-thought, que a gente traduz como "cadeia de pensamento". A ideia é simples de descrever: em vez de pedir a resposta final direto, você pede pro modelo escrever, em texto normal, os passos intermediários do raciocínio antes de chegar na conclusão. Sem fórmula nenhuma envolvida, só frase depois de frase, explicando o caminho.

[BIA] E isso funciona porque, se o modelo escreve o raciocínio primeiro, cada token novo pode olhar pra esse raciocínio já escrito, usando a atenção do episódio sete?

[ANA] Exatamente essa é a mecânica por trás. Cada token que o modelo escreve vira, ele mesmo, parte do contexto que os próximos tokens enxergam. Então, se antes da resposta final o modelo já escreveu "primeiro isso, depois aquilo, logo a conclusão é tal", a previsão daquele último token de resposta está apoiada em tudo que foi escrito antes, e não mais isolada num único palpite. Cada passo do raciocínio vira um degrau mais fácil de prever do que o problema inteiro de uma vez.

[BIA] Isso lembra muito aquela orientação clássica de prova de matemática do colégio: "mostre o seu raciocínio", não só o número final.

[ANA] É uma comparação muito boa, embora vale lembrar que essa trilha não expõe fórmula, então pensa em qualquer problema de várias etapas, não só de matemática: planejar uma viagem com várias escalas, montar um argumento jurídico, ou decidir a melhor jogada numa situação complexa. Chain-of-thought é, literalmente, mostrar o raciocínio escrito antes da conclusão, e isso melhora bastante a taxa de acerto em tarefa complexa, comparado com pedir a resposta direto.

[BIA] Peraí, isso soa como um truque de como pedir a pergunta, tipo escrever "pense passo a passo antes de responder" no início da conversa. Isso é chain-of-thought, ou é outra coisa?

[ANA] Ótima pergunta, porque é exatamente aí que a história se divide em duas partes. A versão que a gente acabou de descrever nasceu assim mesmo: como um truque de como perguntar, aplicado em cima de um modelo comum, sem mudar nada no treino dele. Só pedir "pense passo a passo" já ajudava bastante. Mas os laboratórios foram além disso, e criaram o que se chama hoje de modelo de reasoning, ou modelo de raciocínio.

[BIA] Qual é a diferença entre pedir pro modelo comum pensar passo a passo, e um modelo de raciocínio de verdade?

[ANA] A diferença está em como o modelo foi treinado, não só em como ele é usado. Lembra do episódio nove, quando a gente falou de treino por reforço, o RLHF, onde o modelo recebe uma espécie de recompensa por se comportar de um jeito desejado? Um modelo de reasoning passa por um treino parecido, só que a recompensa aqui está ligada a chegar na resposta final certa, depois de um processo de raciocínio que o próprio modelo constrói, sem alguém escrever esse raciocínio pra ele de antemão.

[BIA] Então, em vez de um humano ensinar "esse é o jeito certo de pensar sobre esse tipo de problema", o modelo descobre sozinho um jeito de pensar que funciona, só porque é recompensado quando acerta a resposta no final?

[ANA] Essa é a virada de chave. Durante esse treino, o modelo tenta caminhos de raciocínio diferentes, e os caminhos que terminam em resposta certa vão sendo reforçados, ficando mais prováveis de aparecer de novo no futuro. Com isso, o modelo aprende sozinho comportamentos bem úteis: explorar mais de um jeito de atacar o problema antes de se decidir, verificar o próprio raciocínio no meio do caminho, e até voltar atrás quando percebe, ainda durante o processo, que um passo anterior não fazia sentido.

[BIA] Voltar atrás no meio do próprio raciocínio? Isso parece um pouco com aquele ciclo que a gente descreveu no episódio onze, de agente: ação, leitura do resultado, ajuste, e repete.

[ANA] A comparação faz muito sentido, embora valha uma distinção importante. Um agente, do jeito que descrevemos no episódio onze, repete um ciclo chamando ferramenta de fora, tipo rodar um programa ou buscar uma informação, e lendo o resultado real que volta de fora pra decidir o próximo passo. Um modelo de reasoning, na versão mais simples, faz esse vaivém de tentar, checar e ajustar todo dentro da própria geração de texto, sem chamar nada de fora. Mas os dois podem, sim, se combinar: existe modelo de reasoning que também usa ferramenta no meio do raciocínio, virando ao mesmo tempo as duas coisas.

[BIA] Isso quer dizer que um modelo de reasoning sempre demora mais pra responder do que um modelo comum, já que ele escreve um monte de raciocínio antes da resposta final?

[ANA] Demora, sim, e esse é um dos principais custos dessa abordagem. Mais texto de raciocínio gerado significa mais token processado, o que significa mais tempo de espera e mais custo computacional por resposta, na mesma lógica de custo por token que a gente já tocou lá no episódio oito. Por isso, modelo de reasoning normalmente não é a escolha certa pra toda pergunta: uma pergunta simples, tipo "qual a capital de um país", não ganha nada com um raciocínio longo, só fica mais lenta e mais cara à toa.

[BIA] Então tem um tipo de problema onde vale a pena esse raciocínio mais longo, e outro tipo onde não vale?

[ANA] Exatamente. O ganho de um modelo de reasoning aparece forte em tarefa com várias etapas encadeadas, onde um erro isolado no meio do caminho pode derrubar a resposta inteira: problema lógico complexo, planejamento com muitas restrições, ou depuração de um programa de computador com um bug difícil de achar. Nesses casos, o tempo extra gasto pensando compensa bastante a diferença na taxa de acerto final. Já numa pergunta direta, de resposta imediata, esse tempo extra normalmente é desperdício.

[BIA] E o raciocínio que o modelo escreve antes da resposta, a gente sempre vê ele, ou às vezes fica escondido?

[ANA] Depende do produto que está usando o modelo. Alguns mostram o raciocínio completo pro usuário, deixando a pessoa acompanhar o caminho até a conclusão. Outros escondem esse raciocínio bruto, e só mostram a resposta final, às vezes com um resumo curto do que foi pensado. Os motivos variam: o raciocínio bruto pode ficar longo demais de ler, pode conter tentativas erradas no meio do caminho que confundiriam mais do que ajudariam, e alguns laboratórios preferem não expor esse processo interno em detalhe por razões de segurança e de vantagem competitiva.

[BIA] Isso me deixa com uma dúvida meio incômoda: se o modelo escreve esse raciocínio em português normal, dá pra confiar que aquilo é, palavra por palavra, o que está realmente acontecendo por dentro dele enquanto ele processa a pergunta?

[ANA] Ótima pergunta pra guardar, porque é literalmente o gancho pro próximo episódio. O raciocínio escrito é uma explicação em linguagem, gerada pelo próprio modelo, e não necessariamente uma fotografia fiel do que acontece, de fato, dentro da rede neural enquanto ela calcula. Pode haver diferença entre o que o modelo "diz" que está pensando, e o que matematicamente está de fato acontecendo lá dentro. Investigar essa diferença é justamente o assunto do episódio dezesseis: interpretabilidade, ou seja, o que realmente acontece dentro do modelo.

[BIA] Resumindo pra fechar: prever resposta direto, token a token, é limitado em problema de várias etapas, porque o modelo só tem um único passo de previsão pra decidir tudo. Chain-of-thought resolve isso pedindo pro modelo escrever o raciocínio antes da resposta final, aproveitando que cada token novo enxerga o que já foi escrito. Modelo de reasoning vai além disso: é treinado, com uma recompensa parecida com a do RLHF do episódio nove, pra descobrir sozinho um jeito de explorar, verificar e corrigir o próprio raciocínio, ao custo de gerar mais texto, gastar mais tempo e custar mais caro por resposta.

[ANA] Exatamente essa é a síntese. E com essa dúvida sobre o que realmente acontece por dentro do modelo enquanto ele "pensa", a gente fecha por hoje.

[BIA] Combinado, guardo essa curiosidade pra lá então.

[ANA] Combinado. Por hoje é isso, pessoal. Guarda suas dúvidas, porque a gente vai voltar nelas nos próximos episódios.

[BIA] Valeu por ouvir a gente. Até o próximo episódio.
