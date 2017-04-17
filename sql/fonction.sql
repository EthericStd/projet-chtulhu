create or replace function ajout_article(LibelléArticle str,
                                         DescriptionArticle bbstr,
                                         PointsArticle int,
                                         PrixArticle real,
                                         QuantitéStock int,
                                         DateMiseVente date,
                                         DateAnnulationVente date)
    returns NumArticle
    as $$
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
        RETURNING NumArticle;

    end;
    $$ language plpgsql;



create or replace function ajout_tag_article(tag str)
    return void
    as $$
    begin

    INSERT INTO TagsArticle VALUES ()

    end;
    $$ language plpgsql;
