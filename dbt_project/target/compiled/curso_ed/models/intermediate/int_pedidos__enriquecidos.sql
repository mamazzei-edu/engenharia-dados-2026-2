select
    pedido_id,
    cliente_id,
    produto_id,
    categoria,
    regiao,
    status_pedido,
    status_pedido = 'faturado'                          as is_faturado,
    valor_unitario,
    quantidade,
    valor_total,
    case
        when valor_total <  100  then 'baixo'
        when valor_total <  500  then 'medio'
        when valor_total < 1500  then 'alto'
        else 'premium'
    end                                                 as faixa_valor,
    avaliacao_cliente,
    avaliacao_cliente >= 4                              as is_avaliacao_positiva,
    pedido_em,
    data_pedido,
    date_trunc('month', data_pedido)::date              as mes_pedido,
    row_number() over (
        partition by cliente_id order by pedido_em
    )                                                   as sequencia_pedido_cliente,
    ingerido_em,
    current_timestamp            as _dbt_processado_em,
    '01987c77-f002-479d-940f-e6b099662dfa'        as _dbt_invocation_id,
    'int_pedidos__enriquecidos'            as _dbt_modelo
from "lakehouse"."intermediate"."int_pedidos__deduplicados"