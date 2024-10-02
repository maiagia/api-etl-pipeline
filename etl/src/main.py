from pyspark.sql import SparkSession, DataFrame, functions as F
import logging

# Defini logs
logging.basicConfig(level=logging.INFO)

# Função para criar a SparkSession
def spark_context_create() -> SparkSession:
    spark = SparkSession.builder \
        .appName("JSON to CSV") \
        .getOrCreate()
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

    # Salva o DataFrame transformado como CSV
    df_transformed.write.csv("../output/output.csv", header=True)


if __name__ == "__main__":
    try:
        logging.info("Criando SparkSession")
        spark = spark_context_create()
        logging.info("SparkSession criada com sucesso")
        logging.info("Lendo arquivos JSON")
        df_producao, df_exportacao = read_source()
        logging.info("Arquivos JSON lidos com sucesso")
        logging.info("Transformando DataFrames")
        df_producao = transform_producao(df_producao)
        df_exportacao =transform(df_exportacao)
        logging.info("DataFrames transformados com sucesso")
    except Exception as e:
        logging.error(f"Erro no processo de ETL: {e}")
        raise e
    finally:
     # Encerra a SparkSession
     spark.stop()