create or replace function verif_panier()
    returns TRIGGER
    as $$
    begin
    if((select nbArticlePanier from articlepanier
    where new.numPanier=numPanier
    and new.numArticle=numArticle) is not null) then
        update ArticlePanier
            set nbArticlePanier = nbArticlePanier + new.nbArticlePanier
        where new.numPanier=numPanier
        and new.numArticle=numArticle;
        if((select nbArticlePanier from articlepanier
        where new.numPanier=numPanier
        and new.numArticle=numArticle) <= 0) then
            delete from articlepanier
            where new.numPanier=numPanier
            and new.numArticle=numArticle;
        end if;
        return null;
    end if;
    return new;
    end;
    $$ language plpgsql;


CREATE TRIGGER verif_panier
Before INSERT on ArticlePanier
for each row
execute procedure verif_panier();
