from pyspark.sql import SparkSession, DataFrame, functions as F
import logging
import findspark

findspark.init()

# Defini logs
logging.basicConfig(level=logging.INFO)

# Função para criar a SparkSession


def spark_context_create() -> SparkSession:
    spark = SparkSession.builder.appName("ETL").getOrCreate()
    return spark

# Função para ler os arquivos de exportação e produção .JSON


def read_source() -> tuple:
    df_producao = spark.read.json("../data/exportacao.json")
    df_exportacao = spark.read.json("../data/producao.json")
    return df_producao, df_exportacao

# Função para transformar os dados de produção


def transform_producao(df: DataFrame) -> DataFrame:
    try:
        df_producao = df.select("PRODUTO", "QUANTIDADE_L").distinct() \
            .withColumnRenamed("PRODUTO", "produto") \
            .withColumnRenamed("QUANTIDADE_L", "quantidade (Litros)") \
            .groupBy("produto") \
            .agg(
            F.sum("quantidade (Litros)").alias("Total_quantidade (Litros)")
        )
        return df_producao
    except Exception as e:
        logging.error(f"Erro ao transformar DataFrame: {e}")
        raise e

# Função para transformar os dados de exportação


def transform_exportacao(df: DataFrame) -> DataFrame:
    try:
        df_exportacao = df.select("PAISES", "QUANTIDADE_KG", "VALOR_US").distinct() \
            .groupBy("PAISES") \
            .agg(
            F.sum("QUANTIDADE_KG").alias("Quantidade (kg)"),
            F.sum("VALOR_US").alias("Valor (US$)")
        ) \
            .withColumnRenamed("PAISES", "Pais")
        return df_exportacao
    except Exception as e:
        logging.error(f"Erro ao transformar DataFrame: {e}")
        raise e

# Verifica se o DataFrame é vazio


def check_empty_df(df: DataFrame):
    if df.count() == 0:
        raise Exception("DataFrame vazio")

# Salva o DataFrame em um arquivo CSV


def save_csv(df: DataFrame, df_producao):
    try:
        if df_producao is not None:
            df.write.csv("../output/producao.csv", header=True)
        df.write.csv("../output/exportacao.csv", header=True)
    except Exception as e:
        logging.error(f"Erro ao salvar DataFrame em CSV: {e}")
        raise e


if __name__ == "__main__":
    try:
        logging.info("Criando SparkSession")
        spark = spark_context_create()
        logging.info("SparkSession criada com sucesso")
        logging.info("Lendo arquivos JSON")
        df_producao, df_exportacao = read_source()
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
    except Exception as e:
        logging.error(f"Erro no processo de ETL: {e}")
        raise e
    finally:
        spark.stop()
