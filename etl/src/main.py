from pyspark.sql import SparkSession, DataFrame, functions as F
import logging
import pandas as pd
import findspark

findspark.init()

# Defini padrões de log
MSG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(format=MSG_FORMAT, datefmt=DATE_FORMAT)
logger = logging.getLogger("vitiBrasil")
logger.setLevel(logging.INFO)

def spark_context_create() -> SparkSession:
    """
        Função para criar a SparkSession
        return: SparkSession
    """
    spark = SparkSession.builder.appName("ETL").getOrCreate()
    return spark

def read_source(spark) -> tuple:
    """
        Função para ler os arquivos de exportação e produção .JSON
        spark: SparkSession
        return: DataFrame
    """
    df_exportacao = spark.read.json("../data/exportacao.json")
    df_producao = spark.read.json("../data/producao.json")
    return df_producao, df_exportacao

def transform_producao(df: DataFrame) -> DataFrame:
    """
        Função para transformar os dados de produção
        df: DataFrame
        return: DataFrame
    """
    try:
        df_producao = df.select("PRODUTO", "QUANTIDADE_L", "ANO").distinct() \
            .withColumnRenamed("PRODUTO", "produto") \
            .withColumnRenamed("ANO", "ano") \
            .groupBy("produto", "ano") \
            .agg(
                F.sum("QUANTIDADE_L").alias("total_litros")
            ) \
            .filter((F.col("total_litros") > 0))\
            .orderBy("ano")
        return df_producao
    except Exception as e:
        logging.error(f"Erro ao transformar DataFrame: {e}")
        raise e

def transform_exportacao(df: DataFrame) -> DataFrame:
    """
        Função para transformar os dados de exportação
        df: DataFrame
        return: DataFrame
    """
    try:
        df_exportacao = df.select("PAISES", "QUANTIDADE_KG", "VALOR_US", "ANO").distinct() \
            .withColumnRenamed("PAISES", "pais") \
            .withColumnRenamed("ANO", "ano") \
            .groupBy("pais", "ano") \
            .agg(
                F.sum("QUANTIDADE_KG").alias("quantidade_kg"),
                F.sum("VALOR_US").alias("valor")
            ) \
            .orderBy("ano") \
            .filter((F.col("quantidade_kg") > 0) & (F.col("valor") > 0))
        return df_exportacao
    except Exception as e:
        logging.error(f"Erro ao transformar DataFrame: {e}")
        raise e

def check_empty_df(df: DataFrame):
    """
        Verifica se o DataFrame é vazio
        df: DataFrame
    """
    if df.count() == 0:
        raise Exception("DataFrame vazio")

def save_csv(df: DataFrame, df_producao):
    """
        Salva o DataFrame em um arquivo CSV
        df: DataFrame
    """
    df_pandas = df.toPandas()
    try:
        if df_producao is not None:
            df_pandas.to_csv("../output/dados_producao.csv", index=False, header=True)
        df_pandas.to_csv("../output/dados_exportacao.csv", index=False, header=True)
    except Exception as e:
        logging.error(f"Erro ao salvar DataFrame em CSV: {e}")
        raise e

def job_execution():
    """
        Função principal para execução do job
    """
    logging.info("Criando SparkSession")
    spark = spark_context_create()
    logging.info("SparkSession criada com sucesso")
    logging.info("Lendo arquivos JSON")
    df_producao, df_exportacao = read_source(spark)
    logging.info("Arquivos JSON lidos com sucesso")
    logging.info("Transformando dados de produção")
    df_producao = transform_producao(df_producao)
    logging.info("Verifica se DataFrame é vazio")
    check_empty_df(df_producao)
    logging.info("Transformando dados de exportação")
    df_exportacao = transform_exportacao(df_exportacao)
    logging.info("Verifica se DataFrame é vazio")
    check_empty_df(df_exportacao)
    logging.info("Salvando dados em CSV")
    save_csv(df_producao, df_exportacao)
    save_csv(df_exportacao, None)
    logging.info("Dados salvos com sucesso")
    return None
if __name__ == "__main__":
    job_execution()
