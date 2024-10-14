from requests import get
from bs4 import BeautifulSoup, Tag
from pandas import DataFrame
from unicodedata import normalize, combining
from re import sub
from numpy import nan

class MLET3():

    def __init__(self) -> None:
        pass
    

    def normalizarTexto(self, pString: str, pSubstituirEspaco: str = '_') -> str:
        """
            Normaliza um texto removendo caracteres especiais e acentuação, removendo o excesso de espaços e convertendo para maiúsculas.

            Parâmetros:
            - pString (str): A string de entrada a ser normalizada.
            - pSubstituirEspaco (str, opcional): O caractere a ser usado para substituir os espaços. Padrão é '_'.

            Retorna:
            - str: Texto normalizado
        """
        vStringNormalizada = normalize('NFKD', pString)
        vStringNormalizada = sub('[^A-Za-z0-9_ ]','', vStringNormalizada)
        vStringNormalizada = vStringNormalizada.strip().upper().replace(' ', '><').replace('<>', '').replace('><', pSubstituirEspaco)
        vStringNormalizada = ''.join([c for c in vStringNormalizada if not combining(c)])
       
        return vStringNormalizada
    

    def requestFind(self, pURL: str, pHeader: dict, pBeautifulSoupFindName: str, pBeautifulSoupFindAttr: dict, pBeautifulSoupParser: str = 'html.parser') -> Tag:
        vRequest = get(url=pURL, headers=pHeader).text
        vBeautifulSoupTags = BeautifulSoup(vRequest, features=pBeautifulSoupParser).find(pBeautifulSoupFindName, pBeautifulSoupFindAttr)
        
        return vBeautifulSoupTags
    

    def extrairTabelaHTML(self, pTextoHTML: Tag, pHierarquiaTabela: dict, pTipoChaveHierarquia: str, pQuantidadeColunasTabelaHTML: int) -> DataFrame:
        vDictDataFrame = {}

        # Criar colunas do DataFrame
        for vColunas in pHierarquiaTabela.values():
            for vColuna in vColunas:
                if not vColuna in vDictDataFrame:
                    vDictDataFrame[vColuna] = []


        # Percorre todas as linhas (tr) e colunas (td) da tabela HTML
        for vLinhaHTML in pTextoHTML.find_all('tr'):
            vColunasHTML = vLinhaHTML.find_all('td')

            # Verifica se a quantidade de colunas da linha atual é igual a quantidade de colunas informada
            if len(vColunasHTML) == pQuantidadeColunasTabelaHTML:
                vAtributoColuna = next(iter(vColunasHTML[0].get(pTipoChaveHierarquia, [])), '')
                vAtributoColuna = vAtributoColuna if vAtributoColuna else list(pHierarquiaTabela.keys())[0]

                # Busca na hierarquia as colunas onde devem ser adicionadas as informações das colunas do HTML
                if pHierarquiaTabela.get(vAtributoColuna):
                    vColunasHierarquia = pHierarquiaTabela.get(vAtributoColuna)

                    # Adiciona as informações das colunas HTML nas colunas do dict final, respeitando a ordem informada na hierarquia
                    for vPosicao, vColuna in enumerate(vColunasHierarquia):
                         vDictDataFrame[vColuna].append(vColunasHTML[vPosicao].text.strip())

                    # Preenche as colunas não preenchidas na linha atual para que as listas sempre tenham a mesma quantidade de itens
                    vColunasNaoPreenchidas = set(list(vDictDataFrame.keys())) - set(vColunasHierarquia)

                    for vColunaFaltante in vColunasNaoPreenchidas:
                        # vItensColunaFaltante = vDictDataFrame.get(vColunaFaltante)

                        # # Se a lista da coluna não preenchida for vazia, adiciona 'nan'
                        # # Caso contrário, repete o item anterior (n-1)
                        # if not vItensColunaFaltante:
                        #     vDictDataFrame[vColunaFaltante].append(nan)
                        # else:
                        #     vDictDataFrame[vColunaFaltante].append(vDictDataFrame[vColunaFaltante][len(vItensColunaFaltante) - 1])

                        vDictDataFrame[vColunaFaltante].append(nan)

        vBaseFinal = DataFrame(vDictDataFrame)
        
        return vBaseFinal
    

    def HTMLTableRequest(self, pLinkRequest: str, pHeaderRequest: dict, pBeautifulSoupFindName: str,
                         pBeautifulSoupFindAttr: dict, pHierarquiaTabela: dict, pTipoChaveHierarquia: str, pQuantidadeColunasTabelaHTML: int) -> DataFrame:
        
        vBaseFinal = DataFrame()

        # Request
        vTabela = self.requestFind(
            pURL=pLinkRequest,
            pHeader=pHeaderRequest,
            pBeautifulSoupFindName=pBeautifulSoupFindName,
            pBeautifulSoupFindAttr=pBeautifulSoupFindAttr
        )

        # Extrair tabela
        vBase = self.extrairTabelaHTML(
            pTextoHTML=vTabela,
            pHierarquiaTabela=pHierarquiaTabela,
            pTipoChaveHierarquia=pTipoChaveHierarquia,
            pQuantidadeColunasTabelaHTML=pQuantidadeColunasTabelaHTML
        )

        return vBase