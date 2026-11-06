
    
    

select
    cliente_id as unique_field,
    count(*) as n_records

from "lakehouse"."intermediate"."int_clientes__metricas"
where cliente_id is not null
group by cliente_id
having count(*) > 1


