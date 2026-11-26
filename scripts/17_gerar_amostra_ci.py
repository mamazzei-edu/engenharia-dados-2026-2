"""Gera uma Bronze pequena e determinística em disco para o CI (sem MinIO)."""

from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path("ci_data/bronze")
rng = np.random.default_rng(42)
N = 5_000

pedidos = pd.DataFrame(
    {
        "id_pedido": np.arange(1, N + 1),
        "id_cliente": rng.integers(1, 501, N),
        "id_produto": rng.integers(1, 201, N),
        "categoria": rng.choice(
            ["Eletrônicos", "Roupas", "Alimentos", "Livros", "Esportes"], N
        ),
        "valor_unitario": np.round(rng.uniform(5, 2000, N), 2),
        "quantidade": rng.integers(1, 11, N),
        "status_pedido": rng.choice(
            ["concluido", "cancelado", "pendente", "reembolsado"],
            N,
            p=[0.75, 0.1, 0.1, 0.05],
        ),
        "regiao": rng.choice(
            ["Sudeste", "Sul", "Nordeste", "Norte", "Centro-Oeste"], N
        ),
        "data_pedido": pd.date_range("2022-01-01", periods=N, freq="90min"),
        "avaliacao_cliente": rng.choice([1, 2, 3, 4, 5], N).astype(float),
        "_fonte": "ci",
        "_ingerido_em": datetime.now(timezone.utc).isoformat(),
    }
)
pedidos["valor_total"] = (pedidos["valor_unitario"] * pedidos["quantidade"]).round(2)

paises = pd.DataFrame(
    {
        "cca2": ["BR"],
        "nome_comum": ["Brazil"],
        "nome_oficial": ["Federative Republic of Brazil"],
        "regiao": ["Americas"],
        "capital": ["Brasília"],
        "populacao": [212_000_000],
        "area_km2": [8_515_767.0],
        "_ingerido_em": [datetime.now(timezone.utc).isoformat()],
    }
)
pokemon = pd.DataFrame(
    {
        "id": [1],
        "nome": ["bulbasaur"],
        "tipo_primario": ["grass"],
        "tipo_secundario": ["poison"],
        "altura_dm": [7],
        "peso_hg": [69],
        "hp_base": [45],
        "ataque_base": [49],
        "defesa_base": [49],
        "_ingerido_em": [datetime.now(timezone.utc).isoformat()],
    }
)

for caminho, df in [
    ("ecommerce_sintetico/ano=2026/mes=01/dia=01/pedidos.parquet", pedidos),
    ("restcountries_api/countries/ano=2026/mes=01/dia=01/countries.parquet", paises),
    ("pokeapi/pokemon/ano=2026/mes=01/dia=01/pokemon.parquet", pokemon),
]:
    destino = RAIZ / caminho
    destino.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(destino, index=False)
for sub in ["analytics", "ml"]:
    Path("ci_data/gold", sub).mkdir(parents=True, exist_ok=True)
print("Amostra de CI gerada em", RAIZ.resolve())
