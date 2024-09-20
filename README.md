# api-etl-project

## Descrição

Este repositório contém o desenvolvimento de uma **API pública** destinada a consultar dados de vitivinicultura da **Embrapa**, extraídos do site [VitiBrasil](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01). A API realiza consultas automáticas nas abas de **Produção** e **Exportação**, disponibilizando esses dados para uso posterior em modelos de **Machine Learning**. Além disso, o projeto inclui scripts de **ETL (Extract, Transform, Load)** para manipular e preparar os dados extraídos.

Este projeto faz parte de um desafio técnico e visa fornecer uma solução automatizada para a coleta, processamento e disponibilização de dados de vitivinicultura.

## Estrutura do Repositório

# api-etl-pipeline

## Descrição

Este repositório contém o desenvolvimento de uma **API pública** destinada a consultar dados de vitivinicultura da **Embrapa**, extraídos do site [VitiBrasil](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01). A API realiza consultas automáticas nas abas de **Produção** e **Exportação**, disponibilizando esses dados para uso posterior em modelos de **Machine Learning**. Além disso, o projeto inclui scripts de **ETL (Extract, Transform, Load)** para manipular e preparar os dados extraídos.

Este projeto faz parte de um desafio técnico e visa fornecer uma solução automatizada para a coleta, processamento e disponibilização de dados de vitivinicultura.

## Estrutura do Repositório

```plaintext
api-etl-project/
│
├── README.md                # Documentação do projeto
├── .gitignore               # Arquivo de ignorados para Git
├── requirements.txt         # Dependências do projeto
├── api/                     # Código relacionado à API
│   ├── __init__.py          # Indica que 'api' é um pacote Python
│   ├── producao.py          # API para consultar dados de Produção
│   ├── exportacao.py        # API para consultar dados de Exportação
│
└── etl/                     # Código relacionado aos processos de ETL
    ├── __init__.py          # Indica que 'etl' é um pacote Python # api-etl-project

## Descrição

Este repositório contém o desenvolvimento de uma **API pública** destinada a consultar dados de vitivinicultura da **Embrapa**, extraídos do site [VitiBrasil](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01). A API realiza consultas automáticas nas abas de **Produção** e **Exportação**, disponibilizando esses dados para uso posterior em modelos de **Machine Learning**. Além disso, o projeto inclui scripts de **ETL (Extract, Transform, Load)** para manipular e preparar os dados extraídos.

Este projeto faz parte de um desafio técnico e visa fornecer uma solução automatizada para a coleta, processamento e disponibilização de dados de vitivinicultura.

## Estrutura do Repositório

```plaintext
api-etl-project/
│
├── README.md                # Documentação do projeto
├── .gitignore               # Arquivo de ignorados para Git
├── requirements.txt         # Dependências do projeto
├── api/                     # Código relacionado à API
│   ├── __init__.py          # Indica que 'api' é um pacote Python
│   ├── producao.py          # API para consultar dados de Produção
│   ├── exportacao.py        # API para consultar dados de Exportação
│
└── etl/                     # Código relacionado aos processos de ETL
    ├── __init__.py          # Indica que 'etl' é um pacote Python
```
## Objetivo

O objetivo principal deste projeto é a criação de uma **API RESTful** em Python que:
- Consulta dados de vitivinicultura da **Embrapa** nas abas de **Produção** e **Exportação**.
- Disponibiliza os dados para serem processados por um pipeline de **ETL**, facilitando a preparação para futuras análises ou modelos de **Machine Learning**.

A API é projetada para ser escalável e flexível, permitindo que os dados sejam facilmente ingeridos em uma base de dados para alimentar futuros modelos preditivos.

## Funcionalidades

1. **API de Produção**:
   - Rota que consulta e retorna os dados de produção de vitivinicultura disponíveis no site da Embrapa.
   - Código localizado em `api/producao.py`.

2. **API de Exportação**:
   - Rota que consulta e retorna os dados de exportação de vitivinicultura.
   - Código localizado em `api/exportacao.py`.

3. **Processos de ETL**:
   - **Extração**: Os dados são extraídos da API de Produção e Exportação.
   - **Transformação**: Limpeza e preparação dos dados para consumo futuro.
   - **Carregamento**: Os dados podem ser carregados para uma base de dados.

## Como Executar o Projeto

### Pré-requisitos

- **Python 3.8+**
- **Pip** (gerenciador de pacotes)

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/api-etl-pipeline.git
   cd api-etl-project

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use: venv\Scripts\activate

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt

### Executar a API

1. Navegue até o diretório api:
   ```bash
    cd api

2. Execute a API de Produção:
   ```bash
    python producao.py

3. Execute a API de Exportação:
    ```bash
    python exportacao.py

As APIs estarão disponíveis localmente em http://localhost:5000/.

