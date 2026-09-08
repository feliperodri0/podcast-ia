---
episodio: 012
titulo: "Mixture of Experts e eficiência"
duracao_alvo_min: 12
prereq: [01, 02, 03, 04, 05, 08, 11]
fontes:
  - url: https://www.anthropic.com/research
    nota: "episódio de fundamento da trilha base, sem paper específico — explica Mixture of Experts (Mistura de Especialistas) como resposta ao problema de custo computacional levantado no fim do episódio onze, reaproveitando os conceitos de rede neural e camada do episódio quatro e de escala do episódio oito"
---

[ANA] Oi, gente, bem-vindos de volta. Eu sou a Ana.

[BIA] E eu sou a Bia. Recapitulando rapidinho: no episódio onze a gente viu o que é um agente. Vimos que um Modelo de Linguagem de Grande Escala, ou LLM, continua sendo só um previsor de próximo token, mas ganha ferramenta, um jeito de pedir uma ação de verdade pro programa ao redor dele, e um ciclo, que repete ação e leitura de resultado várias vezes até a tarefa estar pronta.

[ANA] Isso. E terminei aquele episódio apontando um problema que fica maior justamente por causa do agente: com tanta chamada de modelo dentro de um único ciclo, o custo computacional de rodar tudo isso importa cada vez mais. É esse o assunto de hoje: uma forma de deixar o modelo maior e mais capaz, sem multiplicar o custo de cada chamada na mesma proporção.

[BIA] Antes de entrar nisso, deixa eu confirmar uma coisa: por que um modelo maior custa mais caro pra rodar? Isso não tinha ficado claro desde o episódio oito?

[ANA] Ficou, e vale reforçar. Lembra do episódio quatro, quando a gente descreveu rede neural como uma sequência de camadas, cada uma cheia de parâmetros que são ajustados no treino? Todo modelo que a gente descreveu até aqui é o que chamamos de modelo denso: quando uma pergunta entra, ela passa por todas as camadas, e dentro de cada camada, por todos os parâmetros daquela camada. Nenhum parâmetro fica de fora.

[BIA] Ou seja, quanto mais parâmetro o modelo tem no total, mais conta ele faz pra responder qualquer coisa, mesmo uma pergunta simples.

[ANA] Exatamente. Num modelo denso, tamanho do modelo e custo de cada resposta andam juntos, sempre na mesma proporção. Se você dobra o número de parâmetros pra deixar o modelo mais capaz, você também dobra, mais ou menos, o custo de cada vez que ele responde alguma coisa. E é aqui que entra a ideia de hoje: Mixture of Experts, que a gente traduz como Mistura de Especialistas, ou só MoE, pela sigla em inglês.

[BIA] Pelo nome, parece que em vez de uma rede única, tem várias redes menores, cada uma especializada em alguma coisa?

[ANA] Essa é a intuição certa, embora "especializada" mereça uma ressalva que a gente vai chegar já já. Em algumas camadas do modelo, em vez de um único bloco de parâmetros por onde tudo passa, existem vários blocos paralelos, chamados de especialistas. Cada especialista é, ele mesmo, uma rede neural pequena, do mesmo tipo que a gente já descreveu no episódio quatro. E, junto dos especialistas, existe uma peça nova, chamada de roteador.

[BIA] Roteador faz o quê, decide qual especialista responde?

[ANA] Isso. O roteador olha o pedaço de texto que está passando por aquele ponto do modelo, e decide, pra aquele pedaço específico, quais poucos especialistas, entre os muitos disponíveis, vão de fato processar aquilo. Normalmente só um ou dois, mesmo quando existem dezenas de especialistas na camada inteira. Os outros especialistas, os não escolhidos, simplesmente não fazem conta nenhuma pra aquele pedaço de texto.

[BIA] Então o modelo pode ter um número gigante de parâmetros no total, somando todos os especialistas, mas cada resposta individual só usa uma fração pequena desses parâmetros?

[ANA] Exatamente essa é a virada de chave, e o motivo do nome "eficiência" no título do episódio de hoje. A gente separa duas coisas que, num modelo denso, ficavam grudadas: o tamanho total do modelo, que é a soma de todos os parâmetros de todos os especialistas, e o custo de cada resposta, que depende só dos parâmetros dos poucos especialistas ativados pelo roteador naquela vez. Dá pra ter um modelo enorme no papel, sem pagar o preço computacional de um modelo enorme em cada chamada.

[BIA] Isso lembra alguma coisa do mundo real. Tipo um hospital cheio de médico especialista, cardiologista, dermatologista, ortopedista, mas você, como paciente, só é encaminhado pra um ou dois deles, dependendo do sintoma. O hospital inteiro é grande, mas o seu atendimento passa por pouca gente.

[ANA] Ótima analogia, e ela ajuda a explicar até a palavra "especialista" no nome. Mas cabe uma ressalva importante: ninguém decide de antemão que um especialista vai cuidar só de matemática e outro só de português, por exemplo. O roteador aprende sozinho, durante o treino, que tipo de pedaço de texto mandar pra cada especialista, junto com os próprios especialistas aprendendo a processar bem aquilo que recebem. O resultado costuma ser algum tipo de especialização, mas ela emerge do treino, não é definida por um humano de antemão.

[BIA] Entendi. E dá pra treinar um roteador desses sem risco de dar errado? Tipo, será que ele não fica sempre mandando tudo pro mesmo especialista favorito, e deixando o resto parado à toa?

[ANA] Essa preocupação é real, e é um dos problemas centrais de treinar um MoE. Se o roteador aprende a preferir sempre os mesmos poucos especialistas, o modelo efetivamente desperdiça a capacidade extra dos especialistas menos usados, e ainda sobrecarrega computacionalmente os favoritos. Por isso, o treino de um MoE normalmente inclui um incentivo extra, empurrando o roteador a distribuir o trabalho de forma mais equilibrada entre os especialistas disponíveis, em vez de deixar a rede cair num padrão preguiçoso de usar sempre os mesmos.

[BIA] Faz sentido. E o ganho de eficiência é só na hora de responder, ou também ajuda a treinar o modelo mais barato?

[ANA] O ganho principal costuma aparecer na hora de responder, que é chamada de inferência: o custo por resposta cai, porque só uma fração dos parâmetros participa daquela conta. Mas vale marcar uma ressalva do lado oposto: mesmo os especialistas não usados numa resposta específica continuam precisando ficar carregados na memória do computador, prontos pra serem chamados a qualquer momento por outro pedaço de texto diferente. Então um MoE economiza conta feita a cada resposta, mas não necessariamente economiza memória ocupada, porque o modelo inteiro, com todos os especialistas, ainda precisa estar disponível.

[BIA] Ou seja, é uma troca: mais parâmetro no total, capacidade maior, sem pagar o custo de conta proporcional a esse total, mas ainda pagando o custo de guardar tudo isso em algum lugar.

[ANA] Essa é a síntese certa. E o ganho compensa bastante, principalmente porque os laboratórios vinham esbarrando num limite: deixar um modelo denso maior de verdade custa caro demais pra rodar em escala, o que a gente já discutiu como parte do problema de escala lá no episódio oito. Mixture of Experts é uma das respostas mais usadas hoje pra continuar aumentando capacidade, sem deixar o custo de cada resposta crescer na mesma velocidade.

[BIA] E isso conversa com aquele problema que você levantou no fim do episódio passado, do agente fazendo muita chamada de modelo dentro de um mesmo ciclo?

[ANA] Conversa direto. Se cada chamada individual do modelo, dentro daquele ciclo de ação e leitura de resultado, sai mais barata graças a uma arquitetura como essa, o custo total do agente inteiro, somando todas as voltas do ciclo, também fica mais controlado. Eficiência por chamada e viabilidade de sistemas mais complexos, como agente, andam de mãos dadas.

[BIA] Ficou claro. Resumindo pra fechar: modelo denso usa todo parâmetro em toda resposta; Mixture of Experts quebra parte do modelo em vários especialistas menores, e um roteador aprendido escolhe só poucos deles pra cada pedaço de texto, deixando o modelo maior no total sem deixar cada resposta proporcionalmente mais cara, ao custo de ainda precisar guardar tudo na memória e de precisar equilibrar o uso entre especialistas durante o treino.

[ANA] Exatamente isso. E, com o problema de custo computacional pelo menos amenizado, sobra outra pergunta grande, que a gente ainda não tocou de verdade nesta trilha: como um modelo "pensa" antes de responder, quando o próprio processo de pensar fica visível no meio da resposta? É esse o assunto do episódio treze: raciocínio, e os modelos chamados de reasoning.

[BIA] Combinado, guardo essa curiosidade pra lá então.

[ANA] Combinado. Por hoje é isso, pessoal. Guarda suas dúvidas, porque a gente vai voltar nelas nos próximos episódios.

[BIA] Valeu por ouvir a gente. Até o próximo episódio.
