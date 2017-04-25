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

    create or replace function ajout_client(NomClient str,
                                             PrenomClient str,
                                             DateNaissanceClient date,
                                             MailClient mail,
                                             MDP str)
        returns int
        as $$
        declare
        Num int;
        begin

        INSERT INTO Client (NomClient,
                            PrenomClient,
                            DateNaissanceClient,
                            MailClient,
                            MDP)
            VALUES (NomClient,
                    PrenomClient,
                    DateNaissanceClient,
                    MailClient,
                    MDP)
            RETURNING NumClient into Num;
        return Num;
        end;
        $$ language plpgsql;

create or replace function ajout_tag(NomTags str, ValeurTags int, NumArticle int)
    returns void
    as $$
    begin

    INSERT INTO Tags (NomTags, ValeurTags, NumArticle)
        VALUES (NomTags, ValeurTags, NumArticle);

    end;
    $$ language plpgsql;

create or replace function delete_tag(pNumArticle int)
    returns void
    as $$
    begin

    delete from ArticlePanier
    where NumArticle = pNumArticle;

    end;
    $$ language plpgsql;

create or replace function maj_article(pNumArticle int, pNombreArticle int, NumArticle int)
    returns void
    as $$
    begin

    INSERT INTO Tags (NomTags, ValeurTags, NumArticle)
        VALUES (NomTags, ValeurTags, NumArticle);

    end;
    $$ language plpgsql;

create or replace function get_infos_client(num int)
    returns table(nom str, prenom str, datenaissance date, email mail, mdp str)
    as $$
    declare
    begin

    return query
    select NomClient, PrenomClient, DateNaissanceClient, MailClient, MdpClient
    from Client
    where NumClient = num;

    end;
    $$ language plpgsql;
