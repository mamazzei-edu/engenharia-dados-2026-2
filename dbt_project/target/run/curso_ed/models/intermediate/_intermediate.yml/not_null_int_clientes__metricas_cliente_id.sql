
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select cliente_id
from "lakehouse"."intermediate"."int_clientes__metricas"
where cliente_id is null



  
  
      
    ) dbt_internal_test