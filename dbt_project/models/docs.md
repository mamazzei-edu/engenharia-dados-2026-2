{% docs status_pedido %}
Status harmonizado pela macro `mapear_status`:

| origem | status_pedido |
|---|---|
| concluido | faturado |
| reembolsado | estornado |
| cancelado | cancelado |
| pendente | em_aberto |
{% enddocs %}

{% docs modelo_churn %}
Classificador **HistGradientBoosting** treinado por `scripts/13_treinar_churn.py`.

* **Rótulo:** cliente sem pedidos nos `dias_churn` dias após a data de corte.
* **Features:** somente pedidos anteriores ao corte (*point-in-time*).
* **Métricas:** gravadas em `data/modelos/churn_metricas.json`.
{% enddocs %}