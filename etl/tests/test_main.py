import unittest
from unittest.mock import patch, MagicMock
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.main import (
    spark_context_create,
    transform_producao,
    transform_exportacao,
    check_empty_df,
    save_csv,
    job_execution
)

class TestETL(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spark = spark_context_create()

    def test_spark_context_create(self):
        spark = spark_context_create()
        self.assertIsInstance(spark, SparkSession)

    def test_transform_producao(self):
        schema = StructType([
            StructField("PRODUTO", StringType(), True),
            StructField("QUANTIDADE_L", LongType(), True)
        ])
        data = [("Cerveja", 100), ("Refrigerante", 200), ("Cerveja", 300)]
        df = self.spark.createDataFrame(data, schema)
        result_df = transform_producao(df)
        result_data = result_df.collect()
        expected_data = [("Cerveja", 400), ("Refrigerante", 200)]
        self.assertEqual(len(result_data), len(expected_data))
        for row in result_data:
            self.assertIn((row['produto'], row['Total_quantidade (Litros)']), expected_data)

    def test_transform_exportacao(self):
        schema = StructType([
            StructField("PAISES", StringType(), True),
            StructField("QUANTIDADE_KG", LongType(), True),
            StructField("VALOR_US", DoubleType(), True)
        ])
        data = [("Brasil", 100, 1000.0), ("Brasil", 200, 2000.0), ("Argentina", 300, 3000.0)]
        df = self.spark.createDataFrame(data, schema)
        result_df = transform_exportacao(df)
        result_data = result_df.collect()
        expected_data = [("Brasil", 300, 3000.0), ("Argentina", 300, 3000.0)]
        self.assertEqual(len(result_data), len(expected_data))
        for row in result_data:
            self.assertIn((row['Pais'], row['Quantidade (kg)'], row['Valor (US$)']), expected_data)

    def test_check_empty_df(self):
        schema = StructType([StructField("col1", StringType(), True)])
        empty_df = self.spark.createDataFrame([], schema)
        with self.assertRaises(Exception) as context:
            check_empty_df(empty_df)
        self.assertTrue('DataFrame vazio' in str(context.exception))

        non_empty_df = self.spark.createDataFrame([("data",)], schema)
        try:
            check_empty_df(non_empty_df)
        except Exception:
            self.fail("check_empty_df() raised Exception unexpectedly!")

    def test_save_csv(self):
        mock_df = MagicMock()
        try:
            save_csv(mock_df, mock_df)
            save_csv(mock_df, None)
        except Exception:
            self.fail("save_csv() raised Exception unexpectedly!")

    @patch('src.main.spark_context_create')
    @patch('src.main.read_source')
    @patch('src.main.transform_producao')
    @patch('src.main.transform_exportacao')
    @patch('src.main.check_empty_df')
    @patch('src.main.save_csv')
    def test_job_execution(self, mock_save_csv, mock_check_empty_df, mock_transform_exportacao, mock_transform_producao, mock_read_source, mock_spark_context_create):
        mock_spark = MagicMock()
        mock_spark_context_create.return_value = mock_spark
        mock_df_producao = MagicMock()
        mock_df_exportacao = MagicMock()
        mock_read_source.return_value = (mock_df_producao, mock_df_exportacao)
        mock_transform_producao.return_value = mock_df_producao
        mock_transform_exportacao.return_value = mock_df_exportacao

        try:
            job_execution()
        except Exception:
            self.fail("job_execution() raised Exception unexpectedly!")

if __name__ == '__main__':
    unittest.main()