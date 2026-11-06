
  
  create view "lakehouse"."intermediate"."int_clientes__metricas__dbt_tmp" as (
    -- Métricas por cliente e segmentação RFM (Recência, Frequência, Valor monetário)


with pedidos as (
    select * from "lakehouse"."intermediate"."int_pedidos__enriquecidos"
),

data_referencia as (
    select max(data_pedido) as data_ref from pedidos
),

agregado as (
    select
        cliente_id,
        min(data_pedido)                                     as primeiro_pedido_em,
        max(data_pedido)                                     as ultimo_pedido_em,
        count(*)                                             as total_pedidos,
        
    count(*) filter (where status_pedido = 'faturado') as qtd_faturado,
    count(*) filter (where status_pedido = 'cancelado') as qtd_cancelado,
    count(*) filter (where status_pedido = 'em_aberto') as qtd_em_aberto,
    count(*) filter (where status_pedido = 'estornado') as qtd_estornado,
        sum(valor_total) filter (where is_faturado)          as receita_total,
        avg(valor_total) filter (where is_faturado)          as ticket_medio,
        avg(avaliacao_cliente)                               as nota_media
    from pedidos
    group by cliente_id
),

rfm as (
    select
        a.*,
        d.data_ref - a.ultimo_pedido_em                                 as dias_desde_ultimo_pedido,
        ntile(5) over (order by d.data_ref - a.ultimo_pedido_em desc)   as score_r,
        ntile(5) over (order by a.qtd_faturado)                         as score_f,
        ntile(5) over (order by coalesce(a.receita_total, 0))           as score_m
    from agregado a
    cross join data_referencia d
)

select
    *,
    case
        when score_m = 5 and score_f >= 4 and score_r >= 4 then 'vip'
        when score_m >= 4                                  then 'alto_valor'
        when score_r <= 2                                  then 'em_risco'
        else 'regular'
    end as segmento_cliente
from rfm
  );
