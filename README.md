# Tech Challenge
Membros:
Kleryton de Souza Maria,
Maiara Giavoni,
Lucas Paim de Paula,
Rafael Tafelli dos Santos


# API ETL Pipeline - Previsão de Produção e Exportação

Este projeto implementa um pipeline ETL (Extract, Transform, Load) para coletar e transformar dados de APIs relacionadas à *Produção* e *Exportação* de produtos agrícolas, permitindo prever tendências de produção e exportação ao longo do tempo. Os dados são extraídos de um site especializado no monitoramento de dados do setor agrícola, oferecendo uma visão robusta para análises estratégicas.

## Visão de Negócio

Em um mundo cada vez mais globalizado, entender as tendências de produção e exportação é essencial para empresas que operam no setor agrícola e de bebidas, como vinícolas e exportadores de suco. Este pipeline permite que os dados de produção (em litros) e exportação (em quilogramas e valor em dólares) sejam analisados de forma automatizada. A partir dessa análise, as empresas podem:

- Identificar aumentos ou quedas de produção ao longo do tempo.
- Antecipar a demanda por exportações em mercados internacionais.
- Ajustar estratégias de logística e venda com base em previsões de mercado.
- Maximizar lucros com a exportação para os países mais rentáveis.

## Valor Gerado

Com este pipeline, a empresa pode tomar decisões estratégicas baseadas em dados históricos e previsões futuras, permitindo ajustar suas operações para aumentar a competitividade no mercado global. Isso melhora a eficiência operacional, auxilia na identificação de oportunidades de crescimento, e mitiga riscos associados à variação de oferta e demanda.

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

O pipeline ETL coleta dados de APIs que oferecem informações sobre a produção agrícola e as exportações realizadas pela empresa para diferentes países. O site da API é especializado na divulgação de estatísticas agrícolas, como volumes de produção de vinhos e sucos, e volumes exportados para mercados internacionais. Os dados extraídos são transformados e organizados em arquivos de saída, permitindo que análises preditivas sejam realizadas usando o modelo *Prophet*.

### Variáveis de Previsão

As variáveis utilizadas para as previsões de produção e exportação incluem:

#### 1. *Produção*:
   - **Produto**: Tipo de produto (ex: Vinho de mesa, Vinho fino, Suco, etc.).
   - **Quantidade (L)**: Quantidade de produção em litros para cada tipo de produto.

#### 2. *Exportação*:
   - **Países**: Países para onde os produtos foram exportados.
   - **Quantidade (Kg)**: Quantidade de exportação em quilogramas.
   - **Valor (US$)**: Valor em dólares gerado pela exportação.

Essas variáveis são usadas para prever tendências de produção e exportação ao longo do tempo, ajudando a empresa a ajustar sua estratégia de mercado.

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








