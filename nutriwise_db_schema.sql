-- NutriWise AI - Database Schema
-- Cara penggunaan: Import file ini ke dalam database MySQL Anda, atau gunakan Flask-Migrate (flask db upgrade)

CREATE DATABASE IF NOT EXISTS nutriwise_db;
USE nutriwise_db;

-- 1. Tabel Users (Untuk Autentikasi)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabel Health Profiles (Data Biometrik Input)
CREATE TABLE IF NOT EXISTS health_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    nama_guest VARCHAR(100) NULL,
    umur INT NOT NULL,
    jenis_kelamin VARCHAR(1) NOT NULL,
    berat_badan FLOAT NOT NULL,
    tinggi_badan INT NOT NULL,
    aktivitas VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Tabel Results (Hasil Output Kalkulasi AI)
CREATE TABLE IF NOT EXISTS results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profile_id INT NOT NULL,
    bmi FLOAT NOT NULL,
    status_bmi VARCHAR(50) NOT NULL,
    kalori_tdee INT NOT NULL,
    kalori_fuzzy INT NOT NULL,
    protein_g INT NOT NULL,
    lemak_g INT NOT NULL,
    karbo_g INT NOT NULL,
    fuzzy_detail JSON NOT NULL, -- Menyimpan log Explainable AI
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES health_profiles(id) ON DELETE CASCADE
);

-- 4. Tabel Progress Logs (Jurnal Harian)
CREATE TABLE IF NOT EXISTS progress_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    tanggal DATE NOT NULL,
    berat_badan FLOAT NOT NULL,
    kalori_aktual INT NOT NULL,
    target_kalori INT NOT NULL,
    catatan TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
