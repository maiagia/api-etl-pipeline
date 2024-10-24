# Tech Challenge 3MLET
**Grupo 17**<br/> 
**Membros:**<br/> 
Kleryton de Souza Maria, Lucas Paim de Paula,Maiara Giavoni,Rafael Tafelli dos Santos.

**O video de apresentação está disponivel em : https://github.com/maiagia/api-etl-pipeline/releases/tag/%23apresentacao**

## Sumário
- [Descrição do Projeto](#descrição-do-projeto)
- [Fonte dos Dados](#fonte-dos-dados)
- [Estrutura do Projeto](#estrutura-do-projeto)
  - [1. API](#1-api)
  - [2. ETL](#2-etl)
  - [3. Model](#3-model)
- [API: Coleta de Dados de Produção e Exportação](#api-coleta-de-dados-de-produção-e-exportação)
  - [Endpoints Disponíveis](#endpoints-disponíveis)
    - [1. Produção de Uvas](#1-produção-de-uvas)
    - [2. Exportação de Uvas](#2-exportação-de-uvas)
- [Pipeline ETL](#pipeline-etl)
- [Modelos de Previsão](#modelos-de-previsão)
  - [1. Prophet](#1-prophet)
  - [2. ARIMA](#2-arima)
  - [3. Comparação dos Modelos](#3-comparação-dos-modelos)
- [Como Executar o Projeto](#como-executar-o-projeto)
  - [Pré-requisitos](#pré-requisitos)
  - [Execução do Pipeline ETL](#execução-do-pipeline-etl)
  - [Executar o Modelo de Previsão](#executar-o-modelo-de-previsão)
- [Desenho de Arquitetura](#desenho-de-arquitetura)
- [Contribuições](#contribuições)
  - [Como Contribuir](#como-contribuir)
- [Exemplos de Uso](#exemplos-de-uso)
- [Licença](#licença)
- [Referências e Leitura Adicional](#referências-e-leitura-adicional)

## Descrição do Projeto

Este projeto é composto por três módulos interligados: uma API que coleta dados do site VitiBrasil da Embrapa via scraping, um módulo de ETL que transforma dados brutos em informações estruturadas, e um Modelo de Previsão para identificar padrões e prever tendências no setor vinícola. Essa abordagem oferece insights valiosos para produtores e exportadores, permitindo decisões informadas.

O site da Embrapa Uva e Vinho [VitiBrasil](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01) é a fonte principal de dados. Ele fornece informações detalhadas sobre a produção de uvas, exportações, comercialização e processamento de uvas por ano. O projeto acessa diretamente tabelas HTML desse portal para transformar os dados em formatos utilizáveis.
                       
## Estrutura do Projeto

```bash
api-etl-pipeline/
├── api/                               # Módulo responsável por coletar dados via scraping
├── etl/                               # Pipeline de ETL que processa os dados brutos
├── model/                             # Modelos de previsão de séries temporais
├── .gitignore                         # Arquivos ignorados pelo Git
├── README.md                          # Documentação do projeto
├── requirements.txt                   # Dependências do projeto
```

## Descrição das Pastas

### 1. **API**
A pasta `api/` contém os scripts de scraping que coletam dados diretamente do site VitiBrasil da Embrapa. Ela extrai informações de produção e exportação de uvas em diferentes anos e formata esses dados em JSON para que possam ser utilizados no pipeline ETL.

### 2. **ETL**
A pasta `etl/` contém o pipeline de Extração, Transformação e Carga (ETL), que processa os dados brutos coletados pela API. Este pipeline é responsável por limpar, transformar e estruturar os dados, que serão usados posteriormente para as previsões.

Componentes principais do ETL:
- **Extração**: O scraping coleta os dados do VitiBrasil em formato HTML, e os transforma em JSON.
- **Transformação**: Limpeza e padronização dos dados brutos para remover inconsistências e formatar colunas corretamente.
- **Carga**: Os dados são carregados em arquivos CSV para serem utilizados nos modelos de previsão.

### 3. **Model**
A pasta `model/` contém os modelos preditivos usados para prever as tendências de produção e exportação de vinhos. São implementados dois modelos principais:
- **Prophet**: Modelo de séries temporais desenvolvido pelo Facebook para previsão com sazonalidade.
- **ARIMA**: Um dos modelos estatísticos mais comuns para análise de séries temporais, focado em captura de padrões autoregressivos.


## API: Coleta de Dados de Produção e Exportação

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
 
## Pipeline ETL

O pipeline de ETL realiza as seguintes etapas:

1. **Coleta de Dados**: Usa a API desenvolvida para fazer scraping dos dados de produção e exportação do site VitiBrasil.
2. **Processamento**: Os dados brutos são transformados para remover ruídos, lidar com valores ausentes e normalizar as colunas para facilitar a análise.
3. **Estruturação**: Após a transformação, os dados são estruturados em CSV, categorizados por ano, tipo de uva, país de exportação e outros fatores relevantes.

O objetivo do pipeline é criar uma base de dados que possa ser utilizada diretamente pelos modelos de previsão, permitindo análise histórica e antecipação de futuras tendências no setor vitivinícola.

## Modelos de Previsão

Os modelos de previsão são utilizados para antecipar a produção e exportação de vinhos com base em dados históricos. O objetivo é fornecer previsões que ajudem no planejamento estratégico de produtores e exportadores do setor vitivinícola.

### 1. **Prophet**
O Prophet é um modelo de séries temporais desenvolvido pelo Facebook, especialmente útil para dados com sazonalidade e eventos recorrentes. Ele permite que se façam previsões diárias, mensais ou anuais, capturando tendências e padrões ao longo do tempo.

**Características principais**:
- Adequado para dados com variações sazonais.
- Suporta inclusão de feriados ou eventos especiais.
- Rápido e eficaz para conjuntos de dados maiores.

**Aplicação no projeto**:
No Tech Challenge 3MLET, o Prophet é utilizado para prever a produção e exportação de vinhos nos próximos anos, com base em dados históricos extraídos do VitiBrasil. Ele ajuda a identificar variações sazonais de produção e padrões de exportação ao longo do tempo.

### 2. **ARIMA**
ARIMA (AutoRegressive Integrated Moving Average) é um dos modelos mais populares para séries temporais, especialmente para dados não estacionários, onde as médias e variações mudam com o tempo.

**Características principais**:
- Adequado para dados onde há tendência ou variações em diferentes períodos.
- Baseado em três componentes: autoregressão (AR), diferenciação (I) e média móvel (MA).
- Flexível, podendo ajustar-se a diferentes tipos de séries temporais.

**Aplicação no projeto**:
No projeto, o ARIMA é utilizado para prever a produção de vinhos com base em padrões históricos de exportação e produção, fornecendo uma análise mais detalhada das tendências de curto prazo.

### 3. **Comparação dos Modelos**
Os dois modelos são utilizados de maneira complementar:
- O Prophet é melhor para captar sazonalidade e eventos recorrentes.
- O ARIMA é mais robusto para dados com tendências de curto prazo e variações sutis.

Ambos os modelos oferecem diferentes perspectivas e ajudam a fornecer previsões mais precisas e completas para os produtores e exportadores de vinho.

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

## Desenho de Arquitetura:

![Diagrama sem nome drawio (4)](https://github.com/user-attachments/assets/e2ec26e0-c4c9-41b4-a250-9bafda043069)

**Fluxo da Arquitetura**:
1.  API: A API realiza o scraping dos dados do site VitiBrasil da Embrapa, extraindo informações sobre a produção agrícola e exportação de uvas. Esses dados brutos formam a base para o pipeline.

2.  ETL (Extração, Transformação e Carga): O módulo ETL processa os dados extraídos pela API, lendo dois arquivos JSON:

Dados de produção agrícola: Informações sobre o produto (tipo de uva), quantidade produzida (em litros) e o ano correspondente.
Dados de exportação: Detalhes sobre o país de destino, quantidade exportada (em kg), valor gerado (em USD) e o ano correspondente.
Esses dados são limpos, transformados e estruturados, resultando em um arquivo CSV final que será usado para previsões.

3.  Modelos de Previsão:

Prophet: O modelo Prophet utiliza o arquivo CSV gerado pelo ETL para fazer previsões de produção e exportação de vinhos, focando em tendências de longo prazo e sazonalidade.
ARIMA: O modelo ARIMA também lê o mesmo arquivo CSV, mas é empregado para capturar padrões de curto prazo e realizar previsões mais detalhadas sobre variações de produção e exportação de vinhos.

### Benefícios da Arquitetura
  -  Modularidade: Cada componente (API, ETL, modelos) é isolado, facilitando a manutenção e expansão.
  -  Escalabilidade: O pipeline pode ser facilmente escalado para processar volumes maiores de dados.

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


