# Tech Challenge
Membros:
Kleryton de Souza Maria,
Maiara Giavoni,
Lucas Paim de Paula,
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
- [Contribuições](#contribuições)
- [Licença](#licença)

## Descrição do Projeto

Este pipeline realiza a extração de dados de APIs, a transformação e a carga em um banco de dados. Com os dados armazenados, previsões são realizadas para analisar tendências de *Produção* e *Exportação* ao longo do tempo, utilizando o modelo preditivo *Prophet*.

As variáveis utilizadas para previsão são:

### 1. *Produção*:
   - **Produto**: Tipo de produto (ex: Vinho de mesa, Vinho fino, Suco, etc.)
   - **Quantidade (L)**: Quantidade de produção em litros para cada tipo de produto.

### 2. *Exportação*:
   - **Países**: Países para onde os produtos foram exportados.
   - **Quantidade (Kg)**: Quantidade de exportação em quilogramas.
   - **Valor (US$)**: Valor em dólares gerado pela exportação.

Esses dados são usados para prever tendências de produção e exportação ao longo do tempo.

## Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:

- [Python 3.8+](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- Um banco de dados (PostgreSQL, MySQL, etc.)

### Bibliotecas Necessárias

- `requests`: Para chamadas às APIs.
- `pandas`: Manipulação de dados.
- `sqlalchemy`: Interação com o banco de dados.
- `fbprophet`: Previsão de séries temporais.
- `logging`: Logs do pipeline.
- `pytest`: Testes unitários.

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/maiagia/api-etl-pipeline.git
   cd api-etl-pipeline

2. Crie um ambiente virtual e ative-o:

   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt

## Configuração
Configure o arquivo config.yaml com os detalhes das APIs e do banco de dados:

[ATUALIZAR QUANDO TIVER NO REPO]

### Estrutura do Projeto
```
api-etl-pipeline/
├── config.yaml
├── main.py
├── etl/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── prophet/
│   └── prediction.py
├── tests/
│   └── test_pipeline.py
├── requirements.txt
└── README.md
```

### Módulos

- `extract.py`: Coleta dados das APIs de Produção e Exportação.
- `transform.py`: Processa os dados brutos para análises.
- `load.py`: Armazena os dados transformados no banco de dados.
- `prediction.py`: Realiza a previsão usando o modelo Prophet. (Será implementado em um MVP2)


### Arquitetura








