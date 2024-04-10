class No:
    def __init__(self, estado, pai, acao):
        self.estado = estado
        self.pai = pai
        self.acao = acao

    def expandir(self):
        """
        Retorna uma lista de nós filhos
        """
        filhos = []
        for acao in self.estado.acoes():
            novo_estado = self.estado.resultado(acao)
            novo_no = No(novo_estado, self, acao)
            filhos.append(novo_no)
        return filhos

    def caminho(self):
        """
        Retorna a sequência de ações que levam a este nó
        """
        no = self
        caminho_invertido = []
        while no.pai is not None:
            caminho_invertido.append(no.acao)
            no = no.pai
        return list(reversed(caminho_invertido))


class EstadoJogo:
    def __init__(self, tabuleiro):
        self.tabuleiro = tabuleiro

    def acoes(self):
        """
        Retorna uma lista de ações possíveis no estado atual
        """
        acoes = []
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] == 0:
                    if i > 0:
                        acoes.append(('acima', i, j))
                    if i < 2:
                        acoes.append(('abaixo', i, j))
                    if j > 0:
                        acoes.append(('esquerda', i, j))
                    if j < 2:
                        acoes.append(('direita', i, j))
        return acoes

    def resultado(self, acao):
        """
        Retorna o novo estado resultante após a ação ser tomada
        """
        direcao, i, j = acao
        novo_tabuleiro = [linha[:] for linha in self.tabuleiro]
        if direcao == 'acima':
            novo_tabuleiro[i][j], novo_tabuleiro[i - 1][j] = novo_tabuleiro[i - 1][j], novo_tabuleiro[i][j]
        elif direcao == 'abaixo':
            novo_tabuleiro[i][j], novo_tabuleiro[i + 1][j] = novo_tabuleiro[i + 1][j], novo_tabuleiro[i][j]
        elif direcao == 'esquerda':
            novo_tabuleiro[i][j], novo_tabuleiro[i][j - 1] = novo_tabuleiro[i][j - 1], novo_tabuleiro[i][j]
        elif direcao == 'direita':
            novo_tabuleiro[i][j], novo_tabuleiro[i][j + 1] = novo_tabuleiro[i][j + 1], novo_tabuleiro[i][j]
        return EstadoJogo(novo_tabuleiro)

    def objetivo(self):
        """
        Verifica se o estado atual é o estado objetivo
        """
        return self.tabuleiro == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


def busca_profundidade(estado_inicial):
    """
    Implementação do algoritmo de busca em profundidade
    """
    fronteira = [No(estado_inicial, None, None)]
    explorado = set()

    while fronteira:
        no = fronteira.pop()
        if no.estado.objetivo():
            return no.caminho()
        explorado.add(tuple(map(tuple, no.estado.tabuleiro)))

        for filho in no.expandir():
            if tuple(map(tuple, filho.estado.tabuleiro)) not in explorado:
                fronteira.append(filho)

    return None


# Exemplo de uso
tabuleiro_inicial = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
estado_inicial = EstadoJogo(tabuleiro_inicial)
solucao = busca_profundidade(estado_inicial)

if solucao:
    print("Solução encontrada:")
    for acao in solucao:
        print(acao)
else:
    print("Não foi encontrada uma solução.")
