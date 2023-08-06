import hashlib
import re
import sys
import os
from argparse import ArgumentParser
import numpy as np
import tkinter as tk
from tkinter import filedialog

"""
    VERIFICADOR DE RESPOSTAS 
    _________________________ 

    Utilizado para gerar hash de respostas e salvar em arquivos na pasta _DIR_RESPOSTAS.
    Também disponibiliza funções de verificação de respostas salvas na mesma pasta.
    
    Executar com a flag -h para instruções de uso.
"""

_DEBUG_ = False;

def _dlog(msg):
    """
        Printa a mensagem com o prefixo [DEBUG]
    """
    global _DEBUG_
    if not _DEBUG_:
        return
    print(f'[DEBUG] {msg}')

def _hash(obj):
    """
        Gera um hash do objeto providenciado com o algoritmo SHA256.

        Returns
        __________
        bytes: Hash gerado.
    """
    m = hashlib.sha256()
    m.update(obj)
    return m.digest()

def gerar_resposta(resposta):
    """
    Converte uma resposta numérica em um hash.

    Parameters
    ----------
    resposta
        Resposta. 

    Returns
    _________
    bytes : Hash gerado.
    """
    try:
        s = resposta

        # Se resposta for única criar array com único elemento
        s_types = [ int, float, str ]
        if type(s) is not np.array:
            s = np.array([ s ])

        # Se matriz, mudar pra array de uma dimensão
        if type(s) == np.matrix:
            # reshape(-1) com matrizes não tem o comportamento esperado
            s = s.A1 # mudar para array 1d
        else:
            s = s.reshape(-1) 

        # Cast pra float, matrizes de tipos diferentes
        # vão resultar em hashes diferentes 
        s = s.astype(float)
        
        # Arredondamento para 10 casas decimais.
        s = np.round(s, 10)

        return _hash(s)
    except ValueError:
        print("Resposta em formato inválido.")
        return b'0'


def ler_resposta_de_arquivo(caminho):
    """
        Lê resposta numérica de um arquivo de texto especificado em <caminho>.

        Returns
        ________
        bytes: Hash da resposta lida.
    """
    global _DEBUG_

    with open(caminho, 'r') as f:
        linhas = f.readlines() # Lê todas as linhas do arquivo
        str_arquivo = ''.join(linhas)  # Junta linhas
        _dlog(f'Carregando arquivo: \n{str_arquivo}')

        # Extrai todos os valores numéricos da string
        regex = re.compile('(-?(\d)+(.(\d)+)?)')
        valores = [ float(v[0]) for v in regex.findall(str_arquivo) ]
        _dlog(f'Valores: {valores}')

        hash_resposta = gerar_resposta(valores)
        _dlog(f'Hash da resposta: {hash_resposta}')

        return hash_resposta

def ler_solucao_salva(arquivo_solucao: str):
    """
    Lê uma solução salva no diretório de soluções sob o nome de <problema>.

    Parameters 
    ----------
    problema : str
        Nome do problema.

    Returns
    ----------
    bytes
        Hash da solução.
    """

    data = None
    with open(arquivo_solucao, 'rb') as f:
        data = f.read()

    return data


def salvar_resposta_em_arquivo(caminho : str, resposta : bytes):
    """
    Salva a resposta providenciada em <caminho>

    Parameters
    ----------
    caminho : str
        Nome do arquivo final, sem extensão.

    resposta : bytes
        Resposta em bytes a ser salva no arquivo.

    Raises
    ---------- 
    ValueError
        Caso tipo de <caminho> é diferente de str,
        ou <resposta> é diferente de bytes.

        Caso tamanho de <caminho> é igual a 0.
    """

    if type(resposta) != bytes:
        raise ValueError("Parâmetro <resposta> deve ser do tipo <bytes>")

    if len(caminho) == 0:
        raise ValueError("nome_arquivo deve ter tamanho maior que 0.")

    print(f'Salvando resposta em arquivo: {caminho}')
    with open(caminho, 'wb+') as f:
        f.write(resposta)

    print('Resposta salva com sucesso.')

def _comparar_resposta(resposta, solucao : bytes):
    """
    Gera o hash de uma resposta e compara com a solução providenciada.

    Parameters
    ----------

    resposta : 
        Objeto ao qual o hash gerado será comparado com a solução. Tipicamente um array ou matriz.
    solucao : bytes
        Hash em bytes no qual a resposta será comparada.

    Returns
    ----------
    bool
        Comparação dos dois hashes.

    Raises
    ----------
    TypeError
        Se a solução providenciada não é do tipo bytes.

    """

    if type(solucao) is not bytes:
        raise TypeError("solução deve ser um hash gerado pela função _hash(obj)")

    hash_resposta = gerar_resposta(resposta)
    resposta_certa = hash_resposta == solucao
    msg = 'Resposta correta!' if resposta_certa else "Resposta errada."
    print(msg)
    return resposta_certa

def verificar_resposta(arquivo_solucao : str, resposta):
    """
    Carrega a solução salva no arquivo <nome_problema> e compara com a resposta providenciada.

    Parameters
    ----------
    nome_problema : str
        Nome do problema a ser verificado.
    resposta
        Hash desse objeto será comparado com o hash da solução. 

    Returns
    ----------
    bool
        Comparação dos dois hashes.
    """

    solucao = ler_solucao_salva(arquivo_solucao)
    return _comparar_resposta(resposta, solucao)

class Verificador:
    """
    Helper para verificação de respostas.
    No seu comportamento padrão, carrega a solução de um arquivo chamado
    "solucao", no diretório onde o script está sendo executado.
    """
    def __init__(self, arquivo_solucao="solucao"):
        if not os.path.isfile(arquivo_solucao):
            raise FileNotFoundError(arquivo_solucao)

        self.arquivo = arquivo_solucao

    def verificar_resposta(self, resposta : bytes):
        return verificar_resposta(self.arquivo, resposta)

def executar_testes():
    """
    Executa testes do módulo.
    """

    _dlog("Executando testes...")

    # Testes
    resp = gerar_resposta([1, 2, 3])
    assert(_comparar_resposta([1, 2, 3], resp))
    assert(_comparar_resposta([1.0, 2.0, 3.0], resp))
    assert(_comparar_resposta(["1.0", "2.0", "3.0"], resp))
    assert(_comparar_resposta([1.0, 2, "3.0"], resp))
    assert(_comparar_resposta([1.0, 2.0, 3.0], resp))
    assert(_comparar_resposta([" 1", "2 ", "3   "], resp))
    assert(not _comparar_resposta([1.000001, 2.000001, 3.0000001], resp))
    assert(not _comparar_resposta([" 0", "2 ", "3   "], resp))

    assert(not _comparar_resposta("resposta", resp))
    assert(not _comparar_resposta(b'0100010110', resp))
    assert(not _comparar_resposta([[[]]], resp))
    assert(not _comparar_resposta([[['a'], -1], b'0000'], resp))

    resp = gerar_resposta(np.matrix([[3.4, 8.1], [7.2, 9.2]]))
    assert(_comparar_resposta(np.matrix([[3.4, 8.1], [7.2, 9.2]]), resp))
    assert(_comparar_resposta([3.4, 8.1, 7.2, 9.2], resp))
    assert(_comparar_resposta(["3.4", "8.1", "7.2", "9.2"], resp))
    assert(_comparar_resposta(np.matrix([["3.4", "8.1"], ["7.2", "9.2"]]), resp))

    print("Testes executados com sucesso.")


if __name__ == "__main__":
    parser = ArgumentParser(description="Verifica e gera respostas para o Laboratório de IPython do IMEF-FURG.")
    parser.add_argument("-f", nargs=1, type=str, help="Arquivo de texto contendo a resposta numérica.")
    parser.add_argument("-d", nargs=1, type=str, help="Arquivo destino.")
    parser.add_argument("--testar", action='store_const', const=0, help="Testa funções de utilidade.")
    parser.add_argument("--debug",  action='store_const', const=0, help="Flag de debug. Printa verificações no cmd.")
    args = parser.parse_args()

    _DEBUG_ = args.debug is not None or args.testar is not None
    if _DEBUG_:
        _dlog('Script inicializado em modo de debug...')
        _dlog(f'{args}')
    
    if args.testar is not None:
        executar_testes()
        sys.exit(0)

    root = tk.Tk()
    root.withdraw()

    # Pegar caminho do txt com a solução
    caminho = None
    if args.f is not None:
        caminho = args.f[0]
    else:
        arquivo = filedialog.askopenfile()
        if arquivo == None:
            print("Operação cancelada.")
            sys.exit(0)

        caminho = arquivo.name
    _dlog(caminho)

    resposta = ler_resposta_de_arquivo(caminho)
    _dlog(resposta)

    # Pegar destino do hash
    destino = None
    if args.d is not None:
        destino = args.d[0]
        _dlog(destino)
    else:
        destino = filedialog.asksaveasfilename()
        if len(destino) == 0:
            print("Operação cancelada")
            sys.exit(0)
        
    # Salvar resposta
    salvar_resposta_em_arquivo(destino, resposta)
