-- Créer la base de données
CREATE DATABASE my_app;

-- Créer deux schémas
CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS test;

-- ========================================
-- SCHÉMA APP (Production)
-- ========================================

-- Table users
CREATE TABLE IF NOT EXISTS app.users (
    id_user SERIAL PRIMARY KEY,
    prenom VARCHAR(100) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table activite
CREATE TABLE IF NOT EXISTS app.activite (
    id_activite SERIAL PRIMARY KEY,
    id_user INT NOT NULL,
    date_activite DATE NOT NULL,
    type_sport VARCHAR(100) NOT NULL,
    distance FLOAT NOT NULL DEFAULT 0,
    duree TIME NOT NULL,
    trace TEXT,
    titre VARCHAR(100),
    description TEXT,
    CONSTRAINT fk_activite_users
        FOREIGN KEY (id_user) REFERENCES app.users(id_user)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Table likes (avec contrainte UNIQUE pour éviter doublons)
CREATE TABLE IF NOT EXISTS app.likes (
    id_like SERIAL PRIMARY KEY,
    id_user INT NOT NULL,
    id_activite INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_likes_users
        FOREIGN KEY (id_user) REFERENCES app.users(id_user)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_likes_activite
        FOREIGN KEY (id_activite) REFERENCES app.activite(id_activite)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    -- Empêcher qu'un user like 2 fois la même activité
    CONSTRAINT unique_like_user_activite UNIQUE(id_user, id_activite)
);

-- Table commentaire
CREATE TABLE IF NOT EXISTS app.commentaire (
    id_commentaire SERIAL PRIMARY KEY,
    contenu TEXT NOT NULL,
    id_user INT NOT NULL,
    id_activite INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_commentaire_users
        FOREIGN KEY (id_user) REFERENCES app.users(id_user)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_commentaire_activite
        FOREIGN KEY (id_activite) REFERENCES app.activite(id_activite)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Table follow (avec contraintes UNIQUE et CHECK)
CREATE TABLE IF NOT EXISTS app.follow (
    id_follow SERIAL PRIMARY KEY,
    id_followed INT NOT NULL,
    id_follower INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_follow_followed
        FOREIGN KEY (id_followed) REFERENCES app.users(id_user)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_follow_follower
        FOREIGN KEY (id_follower) REFERENCES app.users(id_user)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    -- Un user ne peut suivre qu'une seule fois un autre user
    CONSTRAINT unique_follower_followed UNIQUE(id_follower, id_followed),
    -- Un user ne peut pas se suivre lui-même
    CONSTRAINT check_no_self_follow CHECK(id_follower != id_followed)
);

-- Table parcours
CREATE TABLE IF NOT EXISTS app.parcours (
    id_parcours SERIAL PRIMARY KEY,
    id_activite INT,
    id_user INT NOT NULL,
    depart TEXT,
    arrivee TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_parcours_activite
        FOREIGN KEY (id_activite) REFERENCES app.activite(id_activite)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_parcours_users
        FOREIGN KEY (id_user) REFERENCES app.users(id_user)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ========================================
-- SCHÉMA TEST (Environnement de test)
-- ========================================

-- Table users
CREATE TABLE IF NOT EXISTS test.users (
    id_user SERIAL PRIMARY KEY,
    prenom VARCHAR(100) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table activite
CREATE TABLE IF NOT EXISTS test.activite (
    id_activite SERIAL PRIMARY KEY,
    id_user INT NOT NULL,
    date_activite DATE NOT NULL,
    type_sport VARCHAR(100) NOT NULL,
    distance FLOAT NOT NULL DEFAULT 0,
    duree TIME NOT NULL,
    trace TEXT,
    titre VARCHAR(100),
    description TEXT,
    CONSTRAINT fk_activite_users
        FOREIGN KEY (id_user) REFERENCES test.users(id_user)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Table likes
CREATE TABLE IF NOT EXISTS test.likes (
    id_like SERIAL PRIMARY KEY,
    id_user INT NOT NULL,
    id_activite INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_likes_users
        FOREIGN KEY (id_user) REFERENCES test.users(id_user)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_likes_activite
        FOREIGN KEY (id_activite) REFERENCES test.activite(id_activite)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT unique_like_user_activite UNIQUE(id_user, id_activite)
);

-- Table commentaire
CREATE TABLE IF NOT EXISTS test.commentaire (
    id_commentaire SERIAL PRIMARY KEY,
    contenu TEXT NOT NULL,
    id_user INT NOT NULL,
    id_activite INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_commentaire_users
        FOREIGN KEY (id_user) REFERENCES test.users(id_user)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_commentaire_activite
        FOREIGN KEY (id_activite) REFERENCES test.activite(id_activite)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Table follow
CREATE TABLE IF NOT EXISTS test.follow (
    id_follow SERIAL PRIMARY KEY,
    id_followed INT NOT NULL,
    id_follower INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_follow_followed
        FOREIGN KEY (id_followed) REFERENCES test.users(id_user)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_follow_follower
        FOREIGN KEY (id_follower) REFERENCES test.users(id_user)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT unique_follower_followed UNIQUE(id_follower, id_followed),
    CONSTRAINT check_no_self_follow CHECK(id_follower != id_followed)
);

-- Table parcours
CREATE TABLE IF NOT EXISTS test.parcours (
    id_parcours SERIAL PRIMARY KEY,
    id_activite INT,
    id_user INT NOT NULL,
    depart TEXT,
    arrivee TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_parcours_activite
        FOREIGN KEY (id_activite) REFERENCES test.activite(id_activite)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_parcours_users
        FOREIGN KEY (id_user) REFERENCES test.users(id_user)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
