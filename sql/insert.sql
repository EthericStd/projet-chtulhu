INSERT INTO Client (NomClient, PrenomCLient, DateNaissanceClient, MailClient, MdpClient) VALUES
    ('Jean', 'Dupont', '10/11/1111', 'jean@dupont', 'lol');



INSERT INTO Vendeur (NomVendeur,
                    AdresseVendeur,
                    MailCommandeVendeur,
                    MailDiscutionVendeur,
                    DescriptionVendeur,
                    NumClient) VALUES
    ('Loreal', 'Rue des setib', 'lol@c', 'lol@d', 'Bonjour a tt et a ts cest dbx9', 1);

INSERT INTO Article (NumVendeur, LibelléArticle, DescriptionArticle) VALUES
    (1, 'Carte MSI', 'carte msi blablabla 360 no scope mdr lol'),
    (1, 'Carte GTX', 'carte gtx blablabla 360 no scope mdr lol');

INSERT INTO Tags (NomTags, ValeurTags, NumArticle) VALUES
    ('type composant', 'Carte_Mere', 1),
    ('type composant', 'Carte_Graphique', 2);

INSERT INTO ArticlePanier (NumPanier, NumArticle, NbArticlePanier) VALUES
    (1, 1, 3),
    (1, 2, 4);












INSERT INTO CartePaiement (TypeCartePaiement, NuméroCartePaiement, NomDétenteurCartePaiement,
                           DateExpirationCartePaiement, CryptogrammeCartePaiement) VALUES
    ('Visa', 0123456789012345, 'Jean Dupont', 012018, 123);

INSERT INTO PossedeCartePaiement (NumClient, NumCartePaiement) VALUES
(1, 1);

INSERT INTO AdresseFacturation (NomPrénomAdresseFacturation,
                                AdresseLigne1AdresseFacturation,
                                AdresseLigne2AdresseFacturation,
                                VilleAdresseFacturation,
                                PaysAdresseFacturation,
                                CodePostalAdresseFacturation) VALUES
    ('Jean Dupont', '80 Rue du sinep', 'batiment segrev', 'Toulon', 'France', 83000);

INSERT INTO PossedeAdrFacturation (NumClient, NumAdresseFacturation) VALUES
    (1, 1);

INSERT INTO AdresseLivraison (NomPrénomAdresseLivraison,
                              AdresseLigne1AdresseLivraison,
                              AdresseLigne2AdresseLivraison,
                              VilleAdresseLivraison,
                              PaysAdresseLivraison,
                              CodePostalAdresseLivraison) VALUES
    ('Jean Dupont', '80 Rue du sinep', 'batiment segrev', 'Toulon', 'France', 83000);

INSERT INTO PossedeAdrLivraison (NumClient, NumAdresseLivraison) VALUES
    (1, 1);

INSERT INTO AdresseLivraison (NomPrénomAdresseLivraison,
                              AdresseLigne1AdresseLivraison,
                              AdresseLigne2AdresseLivraison,
                              VilleAdresseLivraison,
                              PaysAdresseLivraison,
                              CodePostalAdresseLivraison) VALUES
    ('Jean Dupont', '80 Rue du Goûtez-moi cette farce', 'batiment Elle a le choix dans la date', 'Toulon', 'France', 83000);

INSERT INTO PossedeAdrLivraison (NumClient, NumAdresseLivraison) VALUES
    (1, 2);


INSERT INTO Panier (NumClient) VALUES
    (1);
