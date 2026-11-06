
  
  create view "lakehouse"."staging"."stg_ecommerce__pedidos__dbt_tmp" as (
    -- Staging: 1:1 com a fonte. Apenas renomear, tipar e padronizar.
with fonte as (
    select * from read_parquet('s3://bronze/ecommerce_sintetico/ano=*/**/*.parquet', hive_partitioning = false, union_by_name = true, filename = true)
),

renomeado as (
    select
        cast(id_pedido  as bigint)                   as pedido_id,
        cast(id_cliente as bigint)                   as cliente_id,
        cast(id_produto as bigint)                   as produto_id,
        nullif(lower(trim(categoria)), '')         as categoria,
        nullif(lower(trim(regiao)), '')            as regiao,
        nullif(lower(trim(status_pedido)), '')     as status_origem,
        case nullif(lower(trim(status_pedido)), '')
        when 'concluido'   then 'faturado'
        when 'reembolsado' then 'estornado'
        when 'cancelado'   then 'cancelado'
        when 'pendente'    then 'em_aberto'
        else 'desconhecido'
    end         as status_pedido,
        cast(valor_unitario as decimal(12, 2))       as valor_unitario,
        cast(quantidade     as integer)              as quantidade,
        cast(valor_total    as decimal(14, 2))       as valor_total,
        cast(avaliacao_cliente as integer)           as avaliacao_cliente,
        cast(data_pedido as timestamp)               as pedido_em,
        cast(data_pedido as date)                    as data_pedido,
        _fonte                                       as fonte_sistema,
        cast(_ingerido_em as timestamptz)            as ingerido_em,
        filename                                     as arquivo_origem
    from fonte
)

select * from renomeado
  );
