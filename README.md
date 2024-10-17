# Tech Challenge
**Membros:**<br/> 
Kleryton de Souza Maria,<br/> 
Maiara Giavoni,<br/> 
Lucas Paim de Paula,<br/> 
Rafael Tafelli dos Santos


## Sumário

- [Descrição do Projeto](#descrição-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Arquitetura](#arquitetura)
- [Execução](#execução)
- [Testes](#testes)

## Descrição do Projeto

Este projeto realiza um pipeline completo de ETL (Extração, Transformação e Carga) com dados vitivinícolas extraídos de APIs públicas da Embrapa. Após a extração e processamento dos dados, são aplicados modelos de previsão com Prophet para identificar tendências futuras, especialmente relacionadas à produção e comercialização de uvas e derivados (vinhos, sucos, etc.). O projeto permite uma análise automatizada e preditiva de dados de vitivinicultura no Brasil.

**Fonte dos Dados**: Site VitiBrasil
O site da Embrapa Uva e Vinho [VitiBrasil](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01) é a fonte principal de dados. Ele fornece informações detalhadas sobre a produção de uvas, exportações, comercialização e processamento de uvas por ano. O projeto acessa diretamente tabelas HTML desse portal para transformar os dados em formatos utilizáveis.

*Benefícios*:
1.   Automatização Completa: O processo de ETL é completamente automatizado, o que facilita a coleta e o processamento dos dados brutos provenientes das APIs do VitiBrasil.
2.   Transformação dos Dados: Dados extraídos são normalizados, transformados e processados, garantindo alta qualidade e padronização.
3.   Modelagem Preditiva: O modelo Prophet gera previsões de tendências futuras de produção e comercialização, oferecendo insights para planejamento estratégico.
4.   Escalabilidade: O pipeline pode ser escalado para lidar com volumes maiores de dados e pode ser estendido para incluir novos endpoints ou fontes de dados.

## Arquitetura 
A arquitetura do projeto foi projetada para facilitar a escalabilidade, a modularidade e a integração de novas fontes de dados e modelos preditivos.

+----------------+          +---------------+         +---------------+          +-----------+
|                |          |               |         |               |          |           |
| API Vitibrasil | -------> | ETL Pipeline  | ----->  |  Data Output  | ----->   |  Prophet  |
|                |          | (Extração,    |         | (CSV, JSON)   |          | (Modelo)  |
|                |          | Transformação |         |               |          |           |
+----------------+          |  e Carga)     |         +---------------+          +-----------+
                             +--------------+                                   
                       

## Estrutura do Projeto
```
api-etl-pipeline/
├── api/                             # Pasta da API
│   ├── __init__.py                  # Inicialização do módulo API
│   ├── api.py                       # Endpoints das APIs
│   ├── constantes.py                # Constantes usadas pelas APIs
│   ├── utilidades.py                # Funções utilitárias da API
├── etl/                             # Pipeline de ETL
│   ├── data/                        # Dados brutos extraídos das APIs
│   ├── output/                      # Dados processados
│   ├── extract.py                   # Funções de extração
│   ├── transform.py                 # Funções de transformação
│   ├── load.py                      # Funções de carga
│   ├── main.py                      # Pipeline completo de ETL
│   └── notebook_etl.ipynb           # Análise exploratória do ETL
├── model/                           # Pasta de modelos
│   ├── __init__.py                  # Inicialização do módulo de modelos
│   ├── prophet_model.py             # Modelo Prophet para previsão
│   └── evaluation.py                # Avaliação dos modelos
├── tests/                           # Testes unitários
│   └── test_pipeline.py             # Testes para o pipeline e modelos
├── config.yaml                      # Arquivo de configuração
├── requirements.txt                 # Dependências do projeto
└── README.md                        # Documentação do projeto

```
## APIs Disponíveis
As APIs deste projeto acessam os dados vitivinícolas do VitiBrasil, site da Embrapa (VitiBrasil), que fornece informações detalhadas sobre a produção de uvas, processamento e comercialização. As APIs são responsáveis por extrair os dados diretamente de tabelas HTML via scraping.

*Endpoints*

1. Produção de Uvas
**Endpoint**: /producao/<AnoMin>/<AnoMax>
**Descrição**: Retorna dados sobre a produção de uvas no Brasil em litros e valor total por categoria de produto (ex: vinho, suco) e produto específico.
**Parâmetros**:
AnoMin: Ano inicial.
AnoMax: Ano final.
**Retorno**: JSON contendo as colunas: Categoria, Produto, Quantidade (L), Valor Total (R$)

2. Processamento de Uvas
**Endpoint**: /processamento/<Opcao>/<AnoMin>/<AnoMax>
**Descrição**: Extrai dados de processamento de uvas, como uvas viníferas e híbridas, em kg.
**Opções de Processamento**:
Viníferas: subopt_01
Híbridas Americanas: subopt_02
Uvas de Mesa: subopt_03
Sem Classificação: subopt_04
**Retorno**: JSON contendo a quantidade processada (em kg) por categoria de produto.

3. Comercialização de Produtos
**Endpoint**: /comercializacao/<AnoMin>/<AnoMax>
**Descrição**: Retorna dados de comercialização de produtos vitivinícolas, incluindo valor total e quantidade em litros.
**Parâmetros**:
AnoMin: Ano inicial.
AnoMax: Ano final.
**Retorno**: JSON com as colunas:Categoria, Produto, Quantidade (L), Valor Total (R$).







