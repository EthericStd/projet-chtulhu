create or replace function verif_panier()
    returns TRIGGER
    as $$
    declare
    ligne record;
    begin
    for ligne in (SELECT NumArticle from Article) loop
        if (new.NumArticle == NumArticle) then
            update ArticlePanier
                set NbArticlePanier = NbArticlePanier + new.NbArticlePanier;
            return null;
        end if;
    end loop;
    return new;
    end;
    $$ language plpgsql;


CREATE TRIGGER verif_panier
Before INSERT on ArticlePanier
for each row
execute procedure verif_panier();
