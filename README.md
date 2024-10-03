# Tech Challenge
**Membros:**<br/> 
Kleryton de Souza Maria,<br/> 
Maiara Giavoni,<br/> 
Lucas Paim de Paula,<br/> 
Rafael Tafelli dos Santos


# Previsão de Produção e Exportação de Vitivinicultura

Este projeto implementa um pipeline ETL (Extract, Transform, Load) para coletar e transformar dados relacionados à vitivinicultura, disponibilizados pela *Embrapa* (Empresa Brasileira de Pesquisa Agropecuária). O objetivo é analisar e prever tendências de produção e exportação de produtos derivados da vitivinicultura, como vinhos e sucos, ajudando empresas a otimizar suas operações no setor.

## Visão de Negócio

A análise e previsão da produção de vinhos, sucos e outros produtos derivados da uva são fundamentais para vinícolas e exportadores do setor. Os dados disponíveis no site da *Embrapa* proporcionam informações valiosas sobre a produção e exportação do Brasil, um dos principais países produtores de vinho. Com este pipeline, empresas podem:

- Monitorar o desempenho de sua produção ao longo do tempo.
- Planejar melhor suas exportações com base nas previsões de produção e demanda global.
- Aumentar a eficiência logística e comercial, otimizando o volume de exportações.

## Valor Gerado

Este pipeline ajuda a transformar dados de produção e exportação em insights práticos, permitindo às empresas tomar decisões estratégicas baseadas em análises preditivas. Isso inclui identificar tendências sazonais, ajustar a capacidade de produção, e otimizar a venda de produtos para mercados com maior retorno.

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

O pipeline ETL coleta dados de vitivinicultura disponíveis no [site da Embrapa](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01). Esses dados incluem informações sobre a produção agrícola de vinhos e sucos, bem como sobre as exportações para diversos países. O pipeline transforma esses dados em arquivos de saída processados, permitindo a previsão de tendências futuras com o uso do modelo *Prophet*.

**Variáveis de Previsão**:

As variáveis utilizadas para as previsões de produção e exportação incluem:

1. Produção:
   - **Produto**: Tipo de produto (ex: Vinho de mesa, Vinho fino, Suco, etc.).
   - **Quantidade (L)**: Quantidade de produção em litros para cada tipo de produto.

2. Exportação:
   - **Países**: Países para onde os produtos foram exportados.
   - **Quantidade (Kg)**: Quantidade de exportação em quilogramas.
   - **Valor (US$)**: Valor em dólares gerado pela exportação.

Essas variáveis são usadas para prever tendências de produção e exportação ao longo do tempo, ajudando a empresa a ajustar suas estratégias de mercado e operação.

## Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:

- [Python 3.8+](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- Um ambiente virtual separado para gerenciar as dependências do projeto.

### Bibliotecas Necessárias

- `requests`: Para chamadas às APIs.
- `pandas`: Manipulação de dados.
- `fbprophet`: Previsão de séries temporais.
- `logging`: Logs do pipeline.
- `pytest`: Testes unitários.

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/maiagia/api-etl-pipeline.git
   cd api-etl-pipeline

2. Crie um ambiente virtual separado para o ETL e ative-o:

   ```bash
   python3 -m venv etl-venv
   source etl-venv/bin/activate

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt

## Configuração
Configure o arquivo config.yaml com os detalhes das APIs:

```yaml
api:
  producao_url: "http://vitibrasil.cnpuv.embrapa.br/api/producao"
  exportacao_url: "http://vitibrasil.cnpuv.embrapa.br/api/exportacao"
  headers:
    Authorization: "Bearer <API_KEY>"
```

## Estrutura do Projeto

```
api-etl-pipeline/
├── config.yaml
├── etl/
│   ├── data/
│   │   └── (Arquivos de dados brutos extraídos das APIs)
│   ├── output/
│   │   └── (Arquivos processados com agregações e transformações)
│   ├── main.py
│   ├── notebook_etl.ipynb
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
## Módulos

- `extract.py`: Coleta dados das APIs da Embrapa para produção e exportação.
- `transform.py`: Processa e limpa os dados brutos para uso em análises.
- `load.py`: Armazena os dados transformados em arquivos de saída na pasta etl/output.
- `notebook_etl.ipynb`: Uma versão em Jupyter do pipeline ETL para exploração e visualização.
- `prediction.py`: Executa previsões de tendências com o modelo Prophet. (Será implementado em um MVP2)

## Arquitetura
A arquitetura está estruturada de forma hierárquica, começando com a fonte de dados (Embrapa) e passando por cada etapa do processo ETL até a previsão.





## API de Produção 
A API de produção oferece dados sobre a produção vitivinícola no Brasil, permitindo monitorar volumes de produção de vinhos e sucos ao longo do tempo.

## API de Exportação 
A API de exportação disponibiliza dados sobre a quantidade de produtos exportados e o valor gerado pelas exportações, permitindo uma análise detalhada do mercado externo.

## Execução
Para rodar o pipeline ETL e gerar os arquivos de saída:

   ```bash
   python etl/main.py
   ```
Os arquivos processados estarão disponíveis na pasta etl/output.

## Testes
Para executar os testes unitários:

   ```bash
   pytest
   ```
A cobertura de testes do projeto é de 90%.






   





