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
                       
## Estrutura do Projeto

```bash
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
│   ├── src/                           # Código-fonte do pipeline ETL
│   │   └── main.py                    # Orquestração do pipeline ETL completo
│   ├── tests/                         # Testes unitários do pipeline e APIs
│   │   ├── .coverage                  # Relatório de cobertura dos testes
│   │   └── test_main.py               # Testes unitários do pipeline e APIs
├── model/                             # Pasta com os modelos de Machine Learning
│   ├── notebook/                      # Notebooks para análise e desenvolvimento dos modelos
│   │   └── main.ipynb                 # Notebook para desenvolvimento do modelo Prophet
│   ├── src/                           # Código-fonte para os modelos
│   │   └── modelo.py                  # Implementação do modelo Prophet para previsão
├── .gitignore                         # Arquivos e diretórios a serem ignorados pelo Git
├── README.md                          # Documentação do projeto
├── requirements.txt                   # Dependências do projeto
```

## API: Coleta de Dados de Produção e Exportação

### Fonte: VitiBrasil (Embrapa)
As APIs fazem requisições ao site **VitiBrasil**, da **Embrapa**, para extrair dados sobre a produção e exportação de uvas no Brasil.

### Endpoints Disponíveis

#### 1. **Produção de Uvas**
- **Endpoint**: `/producao/<AnoMin>/<AnoMax>`
- **Descrição**: Extrai dados sobre a produção de uvas em litros e o valor total, categorizados por produto (vinho, suco, etc.).
- **Parâmetros**:
  - **AnoMin**: Ano inicial.
  - **AnoMax**: Ano final.
- **Retorno**: Dados em JSON com categorias como:
  - **Produto**
  - **Quantidade (L)**
  - **Valor Total (R$)**

#### 2. **Exportação de Uvas**
- **Endpoint**: `/exportacao/<AnoMin>/<AnoMax>`
- **Descrição**: Extrai dados de exportação de uvas e derivados, incluindo quantidades exportadas (em kg) e valor gerado (em USD).
- **Parâmetros**:
  - **AnoMin**: Ano inicial.
  - **AnoMax**: Ano final.
- **Retorno**: Dados em JSON contendo:
  - **País**
  - **Produto**
  - **Quantidade (Kg)**
  - **Valor (US$)**








