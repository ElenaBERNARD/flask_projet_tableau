-- # sujet 17 : tableau / typeEpoque     --
DROP TABLE IF EXISTS type_epoque, tableau;

CREATE TABLE type_epoque (
    id_type_epoque INT AUTO_INCREMENT PRIMARY KEY,
    libelle VARCHAR(255),
    annee_debut INT,
    annee_fin INT
);

CREATE TABLE tableau (
    id_tableau INT AUTO_INCREMENT PRIMARY KEY,
    nom_tableau VARCHAR(255),
    prix_assurance DECIMAL(10, 2),
    date_realisation DATE,
    peintre VARCHAR(255),
    localisation_musee VARCHAR(255),
    photo VARCHAR(255),
    mouvement VARCHAR(255),
    type_epoque_id INT,
    FOREIGN KEY (type_epoque_id) REFERENCES type_epoque(id_type_epoque)
);

INSERT INTO type_epoque (id_type_epoque,libelle, annee_debut, annee_fin) VALUES 
(NULL, 'Renaissance',1700,1850),
(NULL,'Temps Modernes',1492,1789),
(NULL, 'Contemporain', 1800, 2000),
(NULL, 'Moyen-Age', 476, 1492);


INSERT INTO tableau (id_tableau, nom_tableau, prix_assurance, date_realisation, peintre , localisation_musee, photo ,mouvement, type_epoque_id)
VALUES (NULL, 'La Joconde', '4000', '1506-10-21', 'Léonard de Vinci', 'Louvre', 'laJoconde.jpeg', NULL, 1),
       (NULL, 'Le Radeau de La Méduse', '300.2','1819-03-15', 'Théodore Géricault', 'Louvre', 'leRadeauDeLaMeduse.jpeg', 'romantisme',3),
       (NULL, 'Guernica', '200.6','1937-06-04', 'Pablo Picasso', 'Reina Sofia', 'guernica.jpeg', 'cubisme',3),
       (NULL, 'L Ecole d Athène', '105.3','1512-02-21', 'Raphaël', 'Vatican', 'lEcoleDAthene.jpeg', 'maniérisme', 1),
       (NULL, 'La Jeune Fille à la perle', '2040','1665-11-12', 'Johannes Vermeer', 'Mauritshuis', 'laJeuneFilleALaPerle.jpeg', 'baroque',2),
       (NULL, 'La Laitière', '3040','1658-05-30','Johannes Vermeer', 'Rijksmuseum', 'laLaitière.jpeg', 'baroque', 2),
       (NULL, 'Le Calvaire', '5060','1505-09-30', 'Josse Lieferinxe', 'Louvre', 'leCalvaire.jpeg',NULL, 1),
       (NULL,'Portrait du bouffon Gonella','1230','1445-03-18', 'Jean Fouquet', 'Kunsthistorisches Museum', 'leProtraitduBouffonGonella.jpeg',NULL, 4),
       (NULL,'La liberté guidant le peuple', '150.5','1830-12-25', 'Eugène DelaCroix', 'Louvre', 'laLiberteGuidantlePeuple.jpeg', 'romantisme', 3),
       (NULL,'Rentable de l Agneau mystique', '1010','1432-01-05', 'Jan van Eyck', 'Cathédrale Saint-Bavon de Gand', 'AgneauMystique.jpeg',NULL, 4);
