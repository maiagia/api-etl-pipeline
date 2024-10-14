from utilidades import MLET3, DataFrame
from pandas import concat, to_numeric
from constantes import *
from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec

from requests import get

u = MLET3()

vServer = Flask(__name__)
vSpec = FlaskPydanticSpec('flask', title='API MLET3')
vSpec.register(vServer)

def pegarDados(pLink: str, pHeader: dict, pBeautifulSoupFindName: str
               , pBeautifulSoupFindAttr: dict, pHierarquiaTabela: dict
               , pTipoChaveHierarquia: str, pQuantidadeColunasTabelaHTML: int
               , pAnoMin: int, pAnoMax: int, pValorColunaOrigem: str
               , pColunas_ffill: list[str], pColunasRemoverPrimeiraLinha: list[str]
               , pColunasToNumeric: list[str], pQueryDataFrameFinal: str
               , pColunasToNumeric_FillNa: bool = True
               , pNormalizarColunas: bool = True) -> DataFrame:
    
    vBaseFinal = DataFrame()

    for vAno in range(pAnoMin, pAnoMax + 1):
        vLink = '&'.join([pLink, f'ano={vAno}'])

        vBase = u.HTMLTableRequest(
            pLinkRequest=vLink,
            pHeaderRequest=pHeader,
            pBeautifulSoupFindName=pBeautifulSoupFindName,
            pBeautifulSoupFindAttr=pBeautifulSoupFindAttr,
            pHierarquiaTabela=pHierarquiaTabela,
            pTipoChaveHierarquia=pTipoChaveHierarquia,
            pQuantidadeColunasTabelaHTML=pQuantidadeColunasTabelaHTML
        )

        # Incluir ano
        vBase['ANO'] = vAno

        # Concatenar bases
        vBaseFinal = concat([vBaseFinal, vBase], axis=0)


    # Resetar index
    vBaseFinal = vBaseFinal.reset_index(drop=True)

    # Normalizar colunas
    if (pNormalizarColunas):
        vBaseFinal.columns = [u.normalizarTexto(i) for i in vBaseFinal.columns.to_list()]

    # Incluir coluna 'ORIGEM'
    vBaseFinal['ORIGEM'] = pValorColunaOrigem

    # Preencher colunas nan com ffill
    if (pColunas_ffill):
        vBaseFinal[pColunas_ffill] = vBaseFinal[pColunas_ffill].ffill()

    # Converter colunas 'to_numeric'
    if (pColunasToNumeric):
        for vColuna in pColunasToNumeric:
            vBaseFinal[vColuna] = to_numeric(vBaseFinal[vColuna].fillna(0).astype(str).apply(u.normalizarTexto)).fillna(0)

            if (pColunasToNumeric_FillNa):
                vBaseFinal[vColuna] = vBaseFinal[vColuna].fillna(0)

    # Remover primeira linha de itens que tem subitens
    if (pColunasRemoverPrimeiraLinha):
        vListaIndex = vBaseFinal[vBaseFinal.duplicated(subset=pColunasRemoverPrimeiraLinha, keep=False)].groupby(by=pColunasRemoverPrimeiraLinha).head(1).index

        vBaseFinal = vBaseFinal[~(vBaseFinal.index.isin(vListaIndex))]

    # # # Preencher coluna 'Produto'
    # # vBaseFinal.loc[vBaseFinal['PRODUTO'].isna(), 'PRODUTO'] = vBaseFinal.loc[vBaseFinal['PRODUTO'].isna(), 'CATEGORIA']

    # Executar uma query no DataFrame final
    if (pQueryDataFrameFinal != ''):
        vBaseFinal = vBaseFinal.query(pQueryDataFrameFinal)

    # Resetar index
    vBaseFinal = vBaseFinal.reset_index(drop=True)

    return vBaseFinal

@vServer.get('/producao/<int:pAnoMin>/<int:pAnoMax>')
def pegarDados_Producao(pAnoMin: int, pAnoMax: int) -> str:

    vLink = '?'.join([LINK_VITIBRASIL, ABA_PRODUCAO])
    
    vHierarquiaTabela = {        
        'tb_item': ['CATEGORIA', 'VALOR_TOTAL'],
        'tb_subitem': ['PRODUTO', 'QUANTIDADE_L']
    }

    vBase = pegarDados(
        pLink=vLink,
        pHeader=HEADER,
        pBeautifulSoupFindName='table',
        pBeautifulSoupFindAttr={'class': 'tb_base tb_dados'},
        pHierarquiaTabela=vHierarquiaTabela,
        pTipoChaveHierarquia='class',
        pQuantidadeColunasTabelaHTML=2,
        pAnoMin=pAnoMin,
        pAnoMax=pAnoMax,
        pValorColunaOrigem='PRODUCAO',
        pColunas_ffill=['CATEGORIA', 'VALOR_TOTAL'],
        pColunasRemoverPrimeiraLinha=['ANO', 'CATEGORIA'],
        pColunasToNumeric=['VALOR_TOTAL', 'QUANTIDADE_L'],
        pQueryDataFrameFinal='CATEGORIA.str.upper().str.strip() != "TOTAL"',
        pColunasToNumeric_FillNa=True,
        pNormalizarColunas=True
    )

    return vBase.to_json(orient='records', lines=False, force_ascii=False)

@vServer.get('/processamento/<string:pOpcao>/<int:pAnoMin>/<int:pAnoMax>')
def pegarDados_Processamento(pAnoMin: int, pAnoMax: int, pOpcao: str) -> str:

    vLink = '&'.join(['?'.join([LINK_VITIBRASIL, ABA_PROCESSAMENTO]), pOpcao])

    vHierarquiaTabela = {        
        'tb_item': ['CATEGORIA', 'QUANTIDADE_TOTAL_CATEGORIA_KG'],
        'tb_subitem': ['PRODUTO', 'QUANTIDADE_TOTAL_PRODUTO_KG']
    }

    vBase = pegarDados(
        pLink=vLink,
        pHeader=HEADER,
        pBeautifulSoupFindName='table',
        pBeautifulSoupFindAttr={'class': 'tb_base tb_dados'},
        pHierarquiaTabela=vHierarquiaTabela,
        pTipoChaveHierarquia='class',
        pQuantidadeColunasTabelaHTML=2,
        pAnoMin=pAnoMin,
        pAnoMax=pAnoMax,
        pValorColunaOrigem='PROCESSAMENTO',
        pColunas_ffill=['CATEGORIA', 'QUANTIDADE_TOTAL_CATEGORIA_KG'],
        pColunasRemoverPrimeiraLinha=['ANO', 'CATEGORIA'],
        pColunasToNumeric=['QUANTIDADE_TOTAL_CATEGORIA_KG', 'QUANTIDADE_TOTAL_PRODUTO_KG'],
        pQueryDataFrameFinal='CATEGORIA.str.upper().str.strip() != "TOTAL"',
        pColunasToNumeric_FillNa=True,
        pNormalizarColunas=True
    )

    return vBase#.to_json(orient='records', lines=False, force_ascii=False)

@vServer.get('/comercializacao/<int:pAnoMin>/<int:pAnoMax>')
def pegarDados_Comercializacao(pAnoMin: int, pAnoMax: int) -> str:

    vLink = '?'.join([LINK_VITIBRASIL, ABA_COMERCIALIZACAO])
    
    vHierarquiaTabela = {        
        'tb_item': ['CATEGORIA', 'VALOR_TOTAL'],
        'tb_subitem': ['PRODUTO', 'QUANTIDADE_L']
    }

    vBase = pegarDados(
        pLink=vLink,
        pHeader=HEADER,
        pBeautifulSoupFindName='table',
        pBeautifulSoupFindAttr={'class': 'tb_base tb_dados'},
        pHierarquiaTabela=vHierarquiaTabela,
        pTipoChaveHierarquia='class',
        pQuantidadeColunasTabelaHTML=2,
        pAnoMin=pAnoMin,
        pAnoMax=pAnoMax,
        pValorColunaOrigem='COMERCIALIZACAO',
        pColunas_ffill=['CATEGORIA', 'VALOR_TOTAL'],
        pColunasRemoverPrimeiraLinha=['ANO', 'CATEGORIA'],
        pColunasToNumeric=['VALOR_TOTAL', 'QUANTIDADE_L'],
        pQueryDataFrameFinal='CATEGORIA.str.upper().str.strip() != "TOTAL"',
        pColunasToNumeric_FillNa=True,
        pNormalizarColunas=True
    )

    return vBase.to_json(orient='records', lines=False, force_ascii=False)



vServer.run()





# vBaseProducao = pegarDados_Producao(pAnoMin=1970, pAnoMax=1971)
# vBaseComercializacao = pegarDados_Comercializacao(pAnoMin=1970, pAnoMax=1971)
# vBaseProcessamento_Viniferas = pegarDados_Processamento(pAnoMin=2023, pAnoMax=2023, pOpcao=ABA_PROCESSAMENTO_SUBOPCAO_VINIFERAS)
# vBaseProcessamento_Americanas_Hibridas = pegarDados_Processamento(pAnoMin=2023, pAnoMax=2023, pOpcao=ABA_PROCESSAMENTO_SUBOPCAO_AMERICANAS_HIBRIDAS)
# vBaseProcessamento_Uvas_Mesa = pegarDados_Processamento(pAnoMin=2023, pAnoMax=2023, pOpcao=ABA_PROCESSAMENTO_SUBOPCAO_UVAS_MESA)
# vBaseProcessamento_Sem_Classificacao = pegarDados_Processamento(pAnoMin=2023, pAnoMax=2023, pOpcao=ABA_PROCESSAMENTO_SUBOPCAO_SEM_CLASSIFICACAO)


# vBaseComercializacao.groupby(['ANO', 'CATEGORIA'])['QUANTIDADE_L'].sum()
# vBaseComercializacao[
#     (vBaseComercializacao['CATEGORIA'].isin(['VINHO DE MESA', 'VINHO FINO DE MESA', 'VINHO FRIZANTE', 'VINHO ORGÂNICO', 'VINHO ESPECIAL'])) &
#     (vBaseComercializacao['ANO'] == 1970)
#     ]


# vBaseProducao.groupby(['ANO', 'CATEGORIA']).agg(QTD=('QUANTIDADE_L', 'sum'), VALOR_TOTAL=('VALOR_TOTAL', 'mean'), A=('CATEGORIA', 'count'))
# vBaseComercializacao.groupby(['ANO', 'CATEGORIA']).agg(QTD=('QUANTIDADE_L', 'sum'), VALOR_TOTAL=('VALOR_TOTAL', 'mean'), A=('CATEGORIA', 'count'))
# vBaseProcessamento_Viniferas.groupby(['ANO', 'CATEGORIA']).agg(QUANTIDADE_TOTAL_PRODUTO_KG=('QUANTIDADE_TOTAL_PRODUTO_KG', 'sum'), QUANTIDADE_TOTAL_CATEGORIA_KG=('QUANTIDADE_TOTAL_CATEGORIA_KG', 'mean'), QTD_LINHA=('CATEGORIA', 'count'))