create or replace function tendances(limite int)
    returns table
    as $$
    declare
    table0 table;
    begin

    select NumArticle, sum(NbArticlePanier) as nb_total
    into table0
    from ArticlePanier
    where NumPanier in (select NumPanier
                        from Panier
                        where DateCommandePanier is not null)
    group by NumArticle
    order by NbArticlePanier
    limit limite;

    return table0;

    end;
    $$ language plpgsql;
