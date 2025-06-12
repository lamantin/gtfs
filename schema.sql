-- 1. Szolgáltató / Cég
CREATE TABLE agency (
    id SERIAL PRIMARY KEY,
    agency_id VARCHAR(50) UNIQUE NOT NULL,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    timezone TEXT NOT NULL,
    lang VARCHAR(2),
    phone TEXT
);

-- 2. Megállók
CREATE TABLE stop (
    id SERIAL PRIMARY KEY,
    stop_id VARCHAR(50) UNIQUE NOT NULL,
    name TEXT NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    location_type SMALLINT DEFAULT 0, -- 0 = megálló, 1 = állomás
    parent_station VARCHAR(50) -- kapcsolat állomáshoz
);

-- 3. Útvonalak
CREATE TABLE route (
    id SERIAL PRIMARY KEY,
    route_id VARCHAR(50) UNIQUE NOT NULL,
    agency_id VARCHAR(50) NOT NULL REFERENCES agency(agency_id),
    short_name TEXT,
    long_name TEXT,
    route_type SMALLINT NOT NULL, -- 3 = busz
    color VARCHAR(6),
    text_color VARCHAR(6)
);

-- 4. Naptár / Szolgáltatási idő
CREATE TABLE service (
    id SERIAL PRIMARY KEY,
    service_id VARCHAR(50) UNIQUE NOT NULL,
    monday BOOLEAN,
    tuesday BOOLEAN,
    wednesday BOOLEAN,
    thursday BOOLEAN,
    friday BOOLEAN,
    saturday BOOLEAN,
    sunday BOOLEAN,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

-- 5. Járatok (egy útvonalon belüli menetrendi variáció)
CREATE TABLE trip (
    id SERIAL PRIMARY KEY,
    trip_id VARCHAR(50) UNIQUE NOT NULL,
    route_id VARCHAR(50) NOT NULL REFERENCES route(route_id),
    service_id VARCHAR(50) NOT NULL REFERENCES service(service_id),
    headsign TEXT,
    direction_id SMALLINT,
    shape_id VARCHAR(50)
);

-- 6. Megállók egy adott járaton
CREATE TABLE stop_time (
    id SERIAL PRIMARY KEY,
    trip_id VARCHAR(50) NOT NULL REFERENCES trip(trip_id),
    stop_id VARCHAR(50) NOT NULL REFERENCES stop(stop_id),
    stop_sequence INTEGER NOT NULL,
    arrival_time TIME NOT NULL,
    departure_time TIME NOT NULL,
    pickup_type SMALLINT DEFAULT 0,
    drop_off_type SMALLINT DEFAULT 0
);

-- 7. Shape (útvonal vonal geometriák - opcionális, vizuális térképhez)
CREATE TABLE shape (
    id SERIAL PRIMARY KEY,
    shape_id VARCHAR(50) NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    sequence INTEGER NOT NULL
);


CREATE INDEX idx_trip_service ON trip(service_id);
CREATE INDEX idx_stop_time_trip ON stop_time(trip_id);
CREATE INDEX idx_stop_time_stop ON stop_time(stop_id);
CREATE INDEX idx_shape_seq ON shape(shape_id, sequence);
