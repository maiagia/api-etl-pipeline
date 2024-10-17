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

O pipeline ETL coleta dados de vitivinicultura disponíveis no [site da Embrapa](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01). Esses dados incluem informações sobre a produção agrícola de vinhos e sucos, bem como sobre as exportações para diversos países. O pipeline transforma esses dados em arquivos de saída processados, permitindo a previsão de tendências futuras com o uso do modelo *Prophet*.

## Documentação da API MLET3

Esta documentação descreve uma API desenvolvida para extrair, processar e disponibilizar dados relacionados à produção, processamento e comercialização de produtos vitivinícolas no Brasil. Os dados são obtidos do site oficial da Embrapa Uva e Vinho [VitiBrasil](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01) e disponibilizados através de endpoints RESTful.

A API utiliza bibliotecas como Flask, Pandas, BeautifulSoup e Requests para manipulação dos dados e criação dos serviços web.






### Bibliotecas Necessárias

- `requests`: Para chamadas às APIs.
- `pandas`: Manipulação de dados.
- `pyspark`: Manipulação de dados.
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
   coverage run -m unittest test_main.py
   ```
A cobertura de testes do projeto é de 90%.






   





