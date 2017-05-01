INSERT INTO Client (NomClient, PrenomCLient, DateNaissanceClient, MailClient, MdpClient) VALUES
    ('Jean', 'Dupont', '10/11/1111', 'jean@dupont', 'lol');

INSERT INTO CartePaiement (NumClient) VALUES (1);

INSERT INTO AdresseFacturation (NumClient) VALUES (1);

INSERT INTO Adresselivraison (NumClient) VALUES (1);

INSERT INTO Panier (NumClient, NumAdresseFacturation, NumAdresseLivraison, NumCartePaiement) VALUES
    (1,1,1,1);

INSERT INTO Vendeur (NumClient) VALUES (1);

INSERT INTO Article (NumVendeur, NomArticle, DescriptionArticle) VALUES
    (1, 'carte_mere', 'carte msi blablabla 360 no scope mdr lol'),
    (1, 'carte_graphique', 'carte gtx blablabla 360 no scope mdr lol');

INSERT INTO ArticlePanier (NumPanier, NumArticle, NbArticlePanier) VALUES
    (1, 1, 3),
    (1, 2, 4);
