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
├── api/
│   ├── __init__.py                    # Inicialização do módulo da API
│   ├── api.py                         # Endpoints das APIs de produção e exportação
│   ├── constantes.py                  # URLs e parâmetros utilizados pelas APIs
│   ├── utilidades.py                  # Funções utilitárias para scraping e normalização de dados
├── etl/
│   ├── data/                          # Dados brutos extraídos das APIs
│   │   ├── exportacao.json            # Dados de exportação em formato JSON
│   │   └── producao.json              # Dados de produção em formato JSON
│   ├── notebook/                      # Notebooks para exploração e desenvolvimento
│   │   └── main.ipynb                 # Notebook para execução do pipeline ETL
│   ├── output/                        # Dados processados após as transformações
│   │   ├── dados_exportacao.csv       # Dados de exportação processados
│   │   └── dados_producao.csv         # Dados de produção processados
├── model/                             # Pasta com os modelos de Machine Learning
│   ├── notebook/                      # Notebooks para análise e desenvolvimento dos modelos
│   │   └── main.ipynb                 # Notebook para desenvolvimento do modelo Prophet
│   ├── src/                           # Código-fonte para os modelos
│   │   └── modelo.py                  # Implementação do modelo Prophet para previsão
├── src/
│   └── main.py                        # Orquestração do pipeline ETL completo
├── tests/
│   ├── .coverage                      # Relatório de cobertura dos testes
│   └── test_main.py                   # Testes unitários do pipeline e APIs
├── .gitignore                         # Arquivos e diretórios a serem ignorados pelo Git
├── README.md                          # Documentação do projeto
├── requirements.txt                   # Dependências do projeto


```
## APIs Disponíveis
As APIs deste projeto acessam os dados vitivinícolas do VitiBrasil, site da Embrapa (VitiBrasil), que fornece informações detalhadas sobre a produção de uvas, processamento e comercialização. As APIs são responsáveis por extrair os dados diretamente de tabelas HTML via scraping.

*Endpoints*

1. Produção de Uvas<br/>
**Endpoint**: /producao/<AnoMin>/<AnoMax><br/>
**Descrição**: Retorna dados sobre a produção de uvas no Brasil em litros e valor total por categoria de produto (ex: vinho, suco) e produto específico.<br/>
**Parâmetros**:<br/>
AnoMin: Ano inicial.<br/>
AnoMax: Ano final.<br/>
**Retorno**: JSON contendo as colunas: Categoria, Produto, Quantidade (L), Valor Total (R$)

2. Processamento de Uvas<br/>
**Endpoint**: /processamento/<Opcao>/<AnoMin>/<AnoMax><br/>
**Descrição**: Extrai dados de processamento de uvas, como uvas viníferas e híbridas, em kg.<br/>
**Opções de Processamento**:<br/>
Viníferas: subopt_01<br/>
Híbridas Americanas: subopt_02<br/>
Uvas de Mesa: subopt_03<br/>
Sem Classificação: subopt_04<br/>
**Retorno**: JSON contendo a quantidade processada (em kg) por categoria de produto.

3. Comercialização de Produtos<br/>
**Endpoint**: /comercializacao/<AnoMin>/<AnoMax><br/>
**Descrição**: Retorna dados de comercialização de produtos vitivinícolas, incluindo valor total e quantidade em litros.<br/>
**Parâmetros**:<br/>
AnoMin: Ano inicial.<br/>
AnoMax: Ano final.<br/>
**Retorno**: JSON com as colunas:Categoria, Produto, Quantidade (L), Valor Total (R$).<br/>







