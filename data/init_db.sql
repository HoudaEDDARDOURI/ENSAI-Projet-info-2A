-- Créer la base de données
CREATE DATABASE my_app;


-- Créer deux schémas
CREATE SCHEMA app;
CREATE SCHEMA test;

-- Créer une table User dans chaque schéma
CREATE TABLE app.user (
    id_user SERIAL PRIMARY KEY AUTO INCREMENT,
    prenom VARCHAR(100) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    nom VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE test.user (
    id_user SERIAL PRIMARY KEY AUTO INCREMENT,
    prenom VARCHAR(100) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    nom VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

