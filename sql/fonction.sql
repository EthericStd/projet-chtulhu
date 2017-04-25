create or replace function ajout_article(LibelléArticle str,
                                         DescriptionArticle bbstr,
                                         PointsArticle int,
                                         PrixArticle real,
                                         QuantitéStock int,
                                         DateMiseVente date,
                                         DateAnnulationVente date)
    returns int
    as $$
    declare
    Num int;
    begin

    INSERT INTO Article (LibelléArticle,
                         DescriptionArticle,
                         PointsArticle,
                         PrixArticle,
                         QuantitéStock,
                         DateMiseVente,
                         DateAnnulationVente)
        VALUES (LibelléArticle,
                DescriptionArticle,
                PointsArticle,
                PrixArticle,
                QuantitéStock,
                DateMiseVente,
                DateAnnulationVente)
        RETURNING NumArticle into Num;
    return Num;
    end;
    $$ language plpgsql;

create or replace function delete_article(pNumArticle int)
    returns void
    as $$
    begin

    delete from Article
    where NumArticle = pNumArticle;

    end;
    $$ language plpgsql;

create or replace function ajout_tag(NomTags str, ValeurTags int, NumArticle int)
    return void
    as $$
    begin

    INSERT INTO Tags (NomTags, ValeurTags, NumArticle)
        VALUES (NomTags, ValeurTags, NumArticle);

    end;
    $$ language plpgsql;

create or replace function delete_tag(pNumArticle int)
    return void
    as $$
    begin

    delete from ArticlePanier
    where NumArticle = pNumArticle;

    end;
    $$ language plpgsql;

create or replace function maj_article(pNumArticle int, pNombreArticle, NumArticle int)
    return void
    as $$
    begin

    INSERT INTO Tags (NomTags, ValeurTags, NumArticle)
        VALUES (NomTags, ValeurTags, NumArticle);

    end;
    $$ language plpgsql;
