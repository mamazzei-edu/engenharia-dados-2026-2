
  
  create view "lakehouse"."staging"."stg_pokeapi__pokemon__dbt_tmp" as (
    select
    cast(id as integer)                          as pokemon_id,
    nullif(lower(trim(nome)), '')              as pokemon_nome,
    nullif(lower(trim(tipo_primario)), '')     as tipo_primario,
    nullif(lower(trim(tipo_secundario)), '')   as tipo_secundario,
    cast(altura_dm as integer) * 10              as altura_cm,
    cast(peso_hg   as integer) / 10.0            as peso_kg,
    cast(hp_base     as integer)                 as hp_base,
    cast(ataque_base as integer)                 as ataque_base,
    cast(defesa_base as integer)                 as defesa_base,
    cast(_ingerido_em as timestamptz)            as ingerido_em,
    filename                                     as arquivo_origem
from read_parquet('s3://bronze/pokeapi/pokemon/ano=*/**/*.parquet', union_by_name = true, filename = true)
  );
