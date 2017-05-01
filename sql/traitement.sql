create or replace function tendances(limite int)
    returns table(num int, nombre_totale bigint)
    as $$
    begin

    return query
    select NumArticle, sum(NbArticlePanier)
    from ArticlePanier
    where NumPanier in (select NumPanier
                        from Panier
                        where DateCommandePanier is not null)
    group by NumArticle
    limit limite;

    end;
    $$ language plpgsql;


create or replace function recherche(limite int, nom str)
    returns table(num int)
    as $$
    begin

    return query
    select NumArticle
    from Article
    where NomArticle like '%'||nom||'%'
    limit limite;

    end;
    $$ language plpgsql;
