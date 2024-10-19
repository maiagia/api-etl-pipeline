# Tech Challenge 3MLET
**Grupo 17**<br/> 
**Membros:**<br/> 
Kleryton de Souza Maria, Lucas Paim de Paula,Maiara Giavoni,Rafael Tafelli dos Santos.

## Sumário

## Sumário

- [Descrição do Projeto](#descrição-do-projeto)
- [Fonte dos Dados](#fonte-dos-dados)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Descrição das Pastas](#descrição-das-pastas)
  - [1. API](#1-api)
  - [2. ETL](#2-etl)
  - [3. Model](#3-model)
- [API: Coleta de Dados de Produção e Exportação](#api-coleta-de-dados-de-produção-e-exportação)
  - [1. Produção de Uvas](#1-produção-de-uvas)
  - [2. Exportação de Uvas](#2-exportação-de-uvas)
- [Como Executar o Projeto](#como-executar-o-projeto)
  - [Pré-requisitos](#pré-requisitos)
  - [Execução do Pipeline ETL](#execução-do-pipeline-etl)
  - [Executar o Modelo de Previsão](#executar-o-modelo-de-previsão)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
- [Benefícios da Arquitetura](#benefícios-da-arquitetura)
- [Contribuições](#contribuições)
- [Exemplos de Uso](#exemplos-de-uso)
- [Licença](#licença)
- [Referências e Leitura Adicional](#referências-e-leitura-adicional)


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
## Descrição das Pastas

### 1. **API**
A pasta `api/` contém os endpoints e funções relacionadas à coleta de dados a partir do site da Embrapa VitiBrasil. Estes dados são extraídos em formato JSON e usados no pipeline de ETL.

- **`api.py`**: Define os endpoints que acessam dados de produção e exportação de uvas.
- **`constantes.py`**: URLs e parâmetros de consulta utilizados nas requisições HTTP.
- **`utilidades.py`**: Funções para manipulação de HTML, normalização de texto e extração de tabelas de dados via **BeautifulSoup**.

### 2. **ETL**
A pasta `etl/` contém as funções responsáveis pelo pipeline de Extração, Transformação e Carga dos dados.

- **`data/`**: Armazena os dados brutos extraídos das APIs (JSON).
- **`output/`**: Armazena os dados processados e transformados, prontos para análises.
- **`notebook/main.ipynb`**: Notebook utilizado para testes e desenvolvimento do pipeline ETL.
- **`src/main.py`**: Arquivo principal que orquestra o pipeline ETL completo.
- **`tests/`**: Contém os arquivos de testes unitários para garantir que o pipeline e as APIs funcionem corretamente.

### 3. **Model**
A pasta `model/` é dedicada ao desenvolvimento e implementação de modelos de Machine Learning.

- **`notebook/`**: Notebooks para análise e desenvolvimento dos modelos de previsão.
  - **`main.ipynb`**: Notebook para desenvolvimento do modelo Prophet, onde são realizados testes e validações.
- **`src/`**: Código-fonte para os modelos de Machine Learning.
  - **`modelo.py`**: Implementação do modelo Prophet, que realiza previsões com base nos dados processados de produção e exportação.

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

## Como Executar o Projeto

### Pré-requisitos
- **Python 3.x**: Certifique-se de ter a versão mais recente do Python instalada.
- **Instalação das dependências**: Instale as dependências listadas em `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Execução do Pipeline ETL
1.  Executar o pipeline:
```bash
  python etl/src/main.py
```
2. Explorar os dados (opcional): Utilize o notebook etl/notebook/main.ipynb para explorar os dados e realizar ajustes.

### Executar o Modelo de Previsão
1.  Rodar o modelo Prophet:
```bash
python model/src/modelo.py
```
2. Resultados: As previsões geradas serão armazenadas no diretório de saída.

## Arquitetura do Projeto 


![Diagrama sem nome drawio (2)](https://github.com/user-attachments/assets/49898e25-e35a-4df8-b8bc-47f63f1f8659)


**Fluxo da Arquitetura**:
1.  API faz o scraping de dados do site VitiBrasil da Embrapa, formando a base do processo.
2.  O módulo ETL lê dois arquivos JSON:
    -  Dados de produção agrícola (produto, quantidade de litros e ano).
    -  Dados de exportação (país, quantidade exportada em kg, valor e ano).
3.  O módulo ETL transforma esses dados e gera um arquivo CSV.
4.  O modelo Prophet lê o CSV para análise e previsão.



### Benefícios da Arquitetura
  -  Modularidade: Cada componente (API, ETL, modelos) é isolado, facilitando a manutenção e expansão.
  -  Escalabilidade: O pipeline pode ser facilmente escalado para processar volumes maiores de dados.
  -  Automação Completa: Desde a coleta dos dados até a previsão, o processo é completamente automatizado.

## Contribuições

### Como Contribuir
Contribuições são bem-vindas! Siga estas etapas para contribuir para o projeto:

1. **Fork este repositório**: Crie uma cópia do projeto na sua conta.
2. **Crie uma branch**: Faça suas alterações em uma nova branch.
```bash
   git checkout -b minha-nova-funcionalidade
```
3. **Faça commit das suas alterações**: Registre suas modificações.
```bash
   git commit -m "Adicionando nova funcionalidade"
```
4. **Envie suas alterações:**:
```bash
   git push origin minha-nova-funcionalidade
```
5.  Crie um Pull Request: Proponha suas alterações para serem integradas ao repositório principal.

## Exemplos de Uso
Usando a API de Produção
Para acessar dados sobre a produção de uvas, você pode usar o seguinte endpoint:
```bash
   GET /producao/2020/2021
```
Este endpoint retornará os dados de produção entre os anos de 2020 e 2021.

### Interpretando os Resultados
Os dados retornados estarão em formato JSON, contendo informações sobre:

  -  Produto: Tipo de produto (ex: vinho, suco).
  -  Quantidade (L): Quantidade produzida em litros.
  -  Valor Total (R$): Valor total da produção em reais.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE). Sinta-se à vontade para usar, modificar e distribuir este software, desde que mantenha os créditos apropriados.

---

## Referências e Leitura Adicional

- [Documentação do Prophet](https://facebook.github.io/prophet/docs/quick_start.html)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [VitiBrasil - Embrapa](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01)


