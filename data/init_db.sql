-- Créer la base de données
CREATE DATABASE my_app;

-- Créer deux schémas
CREATE SCHEMA app;
CREATE SCHEMA test;

-- Créer une table users dans chaque schéma
CREATE TABLE app.users (
    id_user SERIAL PRIMARY KEY,
    prenom VARCHAR(100) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE test.users (
    id_user SERIAL PRIMARY KEY,
    prenom VARCHAR(100) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE app.activite (
    id_activite     SERIAL PRIMARY KEY,
    id_user         INT NOT NULL,
    date_activite   DATE NOT NULL,
    type_sport      VARCHAR(100),
    distance        FLOAT,
    duree           TIME,
    trace           TEXT,
    titre           VARCHAR(100),
    description     TEXT,
    id_parcours     INT,
    CONSTRAINT clef_activite_users
        FOREIGN KEY (id_user) REFERENCES app.users(id_user)
);
CREATE TABLE test.activite (
    id_activite     SERIAL PRIMARY KEY,
    id_user         INT NOT NULL,
    date_activite   DATE NOT NULL,
    type_sport      VARCHAR(100),
    distance        FLOAT,
    duree           TIME,
    trace           TEXT,
    titre           VARCHAR(100),
    description     TEXT,
    id_parcours     INT,
    CONSTRAINT clef_activite_users
        FOREIGN KEY (id_user) REFERENCES test.users(id_user)
);

CREATE TABLE app.likes (
    id_like SERIAL PRIMARY KEY,
    id_user INT NOT NULL,
    id_activite INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT clef_likes_users
        FOREIGN KEY (id_user) REFERENCES users(id_user)
          ON DELETE CASCADE
          ON UPDATE CASCADE,
    CONSTRAINT clef_likes_activite
        FOREIGN KEY (id_activite) REFERENCES activite(id_activite)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE test.likes (
    id_like SERIAL PRIMARY KEY,
    id_user INT NOT NULL,
    id_activite INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT clef_likes_users
        FOREIGN KEY (id_user) REFERENCES users(id_user)
          ON DELETE CASCADE
          ON UPDATE CASCADE,
    CONSTRAINT clef_likes_activite
        FOREIGN KEY (id_activite) REFERENCES activite(id_activite)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE app.commentaire (
    id_commentaire SERIAL PRIMARY KEY,
    contenu TEXT NOT NULL,
    id_user INT NOT NULL REFERENCES users(id_user) ON DELETE CASCADE ON UPDATE CASCADE,
    id_activite INT NOT NULL REFERENCES activite(id_activite) ON DELETE CASCADE ON UPDATE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE test.commentaire (
    id_commentaire SERIAL PRIMARY KEY,
    contenu TEXT NOT NULL,
    id_user INT NOT NULL REFERENCES users(id_user) ON DELETE CASCADE ON UPDATE CASCADE,
    id_activite INT NOT NULL REFERENCES activite(id_activite) ON DELETE CASCADE ON UPDATE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS app.follow (
    id_follow SERIAL PRIMARY KEY,
    id_followed INT NOT NULL REFERENCES users(id_user) ON DELETE CASCADE ON UPDATE CASCADE,
    id_follower INT NOT NULL REFERENCES users(id_user) ON DELETE CASCADE ON UPDATE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS test.follow (
    id_follow SERIAL PRIMARY KEY,
    id_followed INT NOT NULL REFERENCES users(id_user) ON DELETE CASCADE ON UPDATE CASCADE,
    id_follower INT NOT NULL REFERENCES users(id_user) ON DELETE CASCADE ON UPDATE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS app.parcours (
    id_parcours SERIAL PRIMARY KEY,
    id_activite INT REFERENCES activite(id_activite) ON DELETE CASCADE ON UPDATE CASCADE,
    id_user INT NOT NULL REFERENCES users(id_user) ON DELETE CASCADE ON UPDATE CASCADE,
    depart TEXT,
    arrivee TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS test.parcours (
    id_parcours SERIAL PRIMARY KEY,
    id_activite INT REFERENCES activite(id_activite) ON DELETE CASCADE ON UPDATE CASCADE,
    id_user INT NOT NULL REFERENCES users(id_user) ON DELETE CASCADE ON UPDATE CASCADE,
    depart TEXT,
    arrivee TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

