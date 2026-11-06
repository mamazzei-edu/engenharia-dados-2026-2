
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    pedido_id as unique_field,
    count(*) as n_records

from "lakehouse"."intermediate"."int_pedidos__deduplicados"
where pedido_id is not null
group by pedido_id
having count(*) > 1



  
  
      
    ) dbt_internal_test