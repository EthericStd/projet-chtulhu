create or replace function tendances()
    returns table
    (ArticlePanier_NumArticle int,
    ArticlePanier__NbArticlePanier int)
    as $$
    begin

    select NumArticle, NbArticlePanier
    from ArticlePanier
    where NumPanier in (select NumPanier
                        from Panier
                        where DateCommandePanier is null);
                    
    end;
    $$ language plpgsql;
