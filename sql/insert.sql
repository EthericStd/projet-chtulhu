--INSERT INTO Article (LibelléArticle) VALUES
--    ('lol'),
--    ('mdr'),
--    ('ptdr');

--INSERT INTO Panier (DateCréationPanier, DateDernièreModifPanier, DateCommandePanier) VALUES
--    (0, 0, 2003-05-21),
--    (0, 0, 2003-05-21),
--    (0, 0, null);

INSERT INTO ArticlePanier (NumPanier, NumArticle, NbArticlePanier) VALUES
    (0, 0, 3),
    (0, 0, 4),
    (0, 0, 4);

INSERT INTO Client (NomClient, PrenomCLient, DateNaissanceClient, MailClient, MdpClient) VALUES
    ('Jean', 'Dupont', '10/11/1111', 'jean@dupont', 'lol');
