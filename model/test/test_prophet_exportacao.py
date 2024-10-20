import sys
import os

# Adiciona o diretório src ao caminho do sistema
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
import pandas as pd
import numpy as np
from src.prophet_exportacao import smape, carregar_dados, treinar_modelo_prophet

class TestModeloExportacao(unittest.TestCase):

    def setUp(self):
        # Configurações iniciais para os testes
        self.df = pd.DataFrame({
            'ano': pd.date_range(start='1970-01-01', periods=10, freq='Y'),
            'quantidade_kg': np.random.randint(1000, 10000, size=10)
        })
        self.df['ano'] = pd.to_datetime(self.df['ano'], format='%Y')
        self.df = self.df.groupby('ano').agg({'quantidade_kg': 'sum'}).reset_index()
        self.df = self.df.rename(columns={'ano': 'ds', 'quantidade_kg': 'y'})

    def test_smape(self):
        y_true = np.array([100, 200, 300])
        y_pred = np.array([110, 190, 290])
        result = smape(y_true, y_pred)
        expected = 6.666666666666667  # Calcule o valor esperado manualmente
        self.assertAlmostEqual(result, expected, places=2)

    def test_carregar_dados(self):
        # Testa se os dados carregados não estão vazios
        df_carregado = carregar_dados()  # Certifique-se de que o caminho do arquivo seja acessível
        self.assertFalse(df_carregado.empty)

    def test_treinar_modelo_prophet(self):
        # Testa se o modelo Prophet é treinado e retorna previsões
        df_treino = self.df[self.df['ds'].dt.year <= 1980]
        previsoes = treinar_modelo_prophet(df_treino)
        self.assertEqual(len(previsoes), 10)  # Deve prever 10 períodos futuros

if __name__ == '__main__':
    unittest.main()
