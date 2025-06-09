-- NASA Asteroids Database Schema

CREATE DATABASE IF NOT EXISTS nasa;
USE nasa;

-- Table for asteroid basic information
CREATE TABLE asteroids (
    id INT,
    name VARCHAR(45),
    absolute_magnitude_h FLOAT,
    estimated_diameter_min_km FLOAT,
    estimated_diameter_max_km FLOAT,
    is_potentially_hazardous_asteroid BOOLEAN
);

-- Table for close approach data
CREATE TABLE close_approaches (
    neo_reference_id INT,
    close_approach_date DATE,
    relative_velocity_kmph FLOAT,
    astronomical_AU FLOAT,
    miss_distance_km FLOAT,
    miss_distance_lunar FLOAT,
    orbiting_body VARCHAR(50)
);


-- Indexes for better performance
CREATE INDEX idx_asteroids_hazardous ON asteroids(is_potentially_hazardous_asteroid);
CREATE INDEX idx_asteroids_diameter ON asteroids(estimated_diameter_min_km, estimated_diameter_max_km);
CREATE INDEX idx_approaches_velocity ON close_approaches(relative_velocity_kmph);
CREATE INDEX idx_approaches_distance ON close_approaches(miss_distance_lunar);
