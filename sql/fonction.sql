create or replace function ajout_article(LibelléArticle str,
                                         DescriptionArticle bbstr,
                                         PointsArticle int,
                                         PrixArticle real,
                                         QuantitéStock int,
                                         DateMiseVente date,
                                         NumVendeur int)
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
                         NumVendeur)
        VALUES (LibelléArticle,
                DescriptionArticle,
                PointsArticle,
                PrixArticle,
                QuantitéStock,
                DateMiseVente,
                NumVendeur)
        RETURNING NumArticle INTO NUM;

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

create or replace function ajout_tag(NomTags str, ValeurTags str, NumArticle int)
    returns void
    as $$
    begin

    INSERT INTO Tags (NomTags, ValeurTags, NumArticle)
        VALUES (NomTags, ValeurTags, NumArticle);

    end;
    $$ language plpgsql;

create or replace function delete_tag(pNumArticle int, Nomtag str)
    returns void
    as $$
    begin

    delete from Tags
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

create or replace function get_infos_client(pnum int)
    returns table(nom str, prenom str, datenaissance date, email mail, mdp str)
    as $$
    declare
    begin

    return query
    select NomClient, PrenomClient, DateNaissanceClient, MailClient, MdpClient
    from Client
    where NumClient = pnum;

    end;
    $$ language plpgsql;


create or replace function get_infos_vendeur(pnum int)
    returns table(nom str, adr str, mail_c mail, mail_d mail, descr bstr)
    as $$
    declare
    begin

    return query
    select NomVendeur, AdresseVendeur, MailCommandeVendeur, MailDiscutionVendeur, DescriptionVendeur
    from Vendeur
    where NumVendeur = pnum;

    end;
    $$ language plpgsql;


create or replace function check_vendeur(pnum int)
    returns int
    as $$
    declare
    Num int;
    begin

    select NumVendeur
    into Num
    from Vendeur
    where NumClient = pnum;

    return Num;

    end;
    $$ language plpgsql;

create or replace function changer_mdp(pNum int, pMdp str)
    returns void
    as $$
    begin

    update Client
        set MdpClient = pMdp
        where NumClient = 1;

    end;
    $$ language plpgsql;


create or replace function get_moyens_paiement_client(pnum int)
    returns table(type str, numero bigint, nom str, date dateCB, crypto int, num int)
    as $$
    declare
    begin

    return query
    select  TypeCartePaiement,
            NuméroCartePaiement,
            NomDétenteurCartePaiement,
            DateExpirationCartePaiement,
            CryptogrammeCartePaiement,
            NumCartePaiement
    from CartePaiement
    where NumCartePaiement IN (select NumCartePaiement
                               from PossedeCartePaiement
                               where NumClient = pnum);

    end;
    $$ language plpgsql;

create or replace function get_adr_facturation_client(pnum int)
    returns table(nomprenom str, adr1 str, adr2 str, ville str, pays str, cp CP, num int)
    as $$
    declare
    begin

    return query
    select  NomPrénomAdresseFacturation,
            AdresseLigne1AdresseFacturation,
            AdresseLigne2AdresseFacturation,
            VilleAdresseFacturation,
            PaysAdresseFacturation,
            CodePostalAdresseFacturation,
            NumAdresseFacturation
    from AdresseFacturation
    where NumAdresseFacturation IN (select NumAdresseFacturation
                                  from PossedeAdrFacturation
                                  where NumClient = pnum);

    end;
    $$ language plpgsql;

create or replace function get_adr_livraison_client(pnum int)
    returns table(nomprenom str, adr1 str, adr2 str, ville str, pays str, cp CP, num int)
    as $$
    declare
    begin

    return query
    select  NomPrénomAdresseLivraison,
            AdresseLigne1AdresseLivraison,
            AdresseLigne2AdresseLivraison,
            VilleAdresseLivraison,
            PaysAdresseLivraison,
            CodePostalAdresseLivraison,
            NumAdresseLivraison
    from AdresseLivraison
    where NumAdresseLivraison IN (select NumAdresseLivraison
                                  from PossedeAdrLivraison
                                  where NumClient = pnum);

    end;
    $$ language plpgsql;

create or replace function ajout_moyens_paiement(pnum int,
                                                TypeCartePaiement str,
                                                NuméroCartePaiement bigint,
                                                NomDétenteurCartePaiement str,
                                                DateExpirationCartePaiement dateCB,
                                                CryptogrammeCartePaiement int)
    returns void
    as $$
    declare
    Num int;
    begin

    INSERT INTO CartePaiement (TypeCartePaiement,
                                NuméroCartePaiement,
                                NomDétenteurCartePaiement,
                                DateExpirationCartePaiement,
                                CryptogrammeCartePaiement)
        VALUES (TypeCartePaiement,
                NuméroCartePaiement,
                NomDétenteurCartePaiement,
                DateExpirationCartePaiement,
                CryptogrammeCartePaiement)
    RETURNING NumCartePaiement into Num;

    INSERT INTO PossedeCartePaiement (NumClient, NumCartePaiement) VALUES
    (pnum, Num);

    end;
    $$ language plpgsql;



create or replace function ajout_adresse_facturation(pnum int,
                                                NomPrénomAdresseFacturation str,
                                                AdresseLigne1AdresseFacturation str,
                                                AdresseLigne2AdresseFacturation str,
                                                VilleAdresseFacturation str,
                                                PaysAdresseFacturation str,
                                                CodePostalAdresseFacturation CP)
    returns void
    as $$
    declare
    Num int;
    begin

    INSERT INTO AdresseFacturation (NomPrénomAdresseFacturation,
                                    AdresseLigne1AdresseFacturation,
                                    AdresseLigne2AdresseFacturation,
                                    VilleAdresseFacturation,
                                    PaysAdresseFacturation,
                                    CodePostalAdresseFacturation)
        VALUES (NomPrénomAdresseFacturation,
                AdresseLigne1AdresseFacturation,
                AdresseLigne2AdresseFacturation,
                VilleAdresseFacturation,
                PaysAdresseFacturation,
                CodePostalAdresseFacturation)
    RETURNING NumAdresseFacturation into Num;

    INSERT INTO PossedeAdrFacturation (NumClient, NumAdresseFacturation) VALUES
    (pnum, Num);

    end;
    $$ language plpgsql;


create or replace function ajout_adresse_livraison(pnum int,
                                                    NomPrénomAdresseLivraison str,
                                                    AdresseLigne1AdresseLivraison str,
                                                    AdresseLigne2AdresseLivraison str,
                                                    VilleAdresseLivraison str,
                                                    PaysAdresseLivraison str,
                                                    CodePostalAdresseLivraison CP)
    returns void
    as $$
    declare
    Num int;
    begin

    INSERT INTO AdresseLivraison (NomPrénomAdresseLivraison,
                                AdresseLigne1AdresseLivraison,
                                AdresseLigne2AdresseLivraison,
                                VilleAdresseLivraison,
                                PaysAdresseLivraison,
                                CodePostalAdresseLivraison)
        VALUES (NomPrénomAdresseLivraison,
                AdresseLigne1AdresseLivraison,
                AdresseLigne2AdresseLivraison,
                VilleAdresseLivraison,
                PaysAdresseLivraison,
                CodePostalAdresseLivraison)
    RETURNING NumAdresseLivraison into Num;

    INSERT INTO PossedeAdrLivraison (NumClient, NumAdresseLivraison) VALUES
    (pnum, Num);

    end;
    $$ language plpgsql;


create or replace function ameliorer_vendeur(NomVendeur str,
                                            AdresseVendeur str,
                                            MailCommandeVendeur mail,
                                            MailDiscutionVendeur mail,
                                            DescriptionVendeur bstr,
                                            NumClient int)
    returns int
    as $$
    declare
    Num int;
    begin

    INSERT INTO Vendeur (NomVendeur,
                        AdresseVendeur,
                        MailCommandeVendeur,
                        MailDiscutionVendeur,
                        DescriptionVendeur,
                        NumClient)
        VALUES (NomVendeur,
                AdresseVendeur,
                MailCommandeVendeur,
                MailDiscutionVendeur,
                DescriptionVendeur,
                NumClient)
        RETURNING NumVendeur into Num;
    return Num;
    end;
    $$ language plpgsql;


create or replace function sup_moyens_paiement(pnum int)
    returns void
    as $$
    begin

    delete from PossedeCartePaiement
    where NumCartePaiement = pnum;

    end;
    $$ language plpgsql;

create or replace function sup_adr_facturation(pnum int)
    returns void
    as $$
    begin

    delete from PossedeAdrFacturation
    where NumAdresseFacturation = pnum;

    end;
    $$ language plpgsql;

create or replace function sup_adr_livraison(pnum int)
    returns void
    as $$
    begin

    delete from PossedeAdrLivraison
    where NumAdresseLivraison = pnum;

    end;
    $$ language plpgsql;
