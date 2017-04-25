create or replace function tendances(limite int)
    returns table(num int, nb_total int)
    as $$
    begin

    select NumArticle, sum(NbArticlePanier)
    from ArticlePanier
    where NumPanier in (select NumPanier
                        from Panier
                        where DateCommandePanier is not null)
    group by NumArticle
    order by NbArticlePanier
    limit limite;

    end;
    $$ language plpgsql;


create or replace function recherche(limite int, nom str)
    returns table(num int)
    as $$
    begin

    select NumArticle
    from Article
    where LibelléArticle like '%nom%'
    limit limite;

    end;
    $$ language plpgsql;
