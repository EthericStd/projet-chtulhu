create or replace function verif_panier(int)
  returns TRIGGER
  as $$
  begin
  SELECT NumArticle
  from Article
  if (new.NumArticle == NumArticle) then
    update ArticlePanier
      set NbArticlePanier = NbArticlePanier + $1
      return null;
  else
    return new;
  end if;
  end;
  $$ language plpgsql;


create or replace function visite()
  returns TRIGGER
  as $$
  begin
  select c.NumClient, a.NumArticle
  from Client as c, Article as a
  if ((c.NumClient == new.NumClient) and (a.NumArticle == new.NumArticle))

    if (new.DateVisite != DateVisite) then
      update Visite
        set DateVisite = new.DateVisite
        set NbVisite = NbVisite + 1
        return null;
    else
      update Visite
        set NbVisite = NbVisite + 1
      return null;
    end if;

  else
    return new;
  end if;
  end;
  $$ language plpgsql;


CREATE TRIGGER verif_panier
Before INSERT on ArticlePanier
for each row
execute procedure verif_panier();

CREATE TRIGGER visite
Before INSERT on Visite
for each row
execute procedure visite();
