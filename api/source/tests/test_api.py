import sys
import os
import pytest
from flask import json

# Adiciona o diretório raiz ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  # Agora o pytest deve encontrar o app corretamente

@pytest.fixture
def client():
    """Cria um cliente de teste para a API Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_data(client):
    """Testa a rota de obtenção de dados."""
    response = client.get('/data/initialdate/2025-03-26000000/finaldate/2025-03-26230000')
    assert response.status_code == 200  # Ajuste conforme o esperado
    data = json.loads(response.data)
    assert "data" in data  # Verifica se a resposta contém "data"

