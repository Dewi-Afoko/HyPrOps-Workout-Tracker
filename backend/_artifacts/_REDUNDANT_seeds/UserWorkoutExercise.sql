DROP TABLE IF EXISTS workouts;
DROP SEQUENCE IF EXISTS user_username;
DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS username;


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username text UNIQUE,
    password text,
    workout_list text[]
);

CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    date text,
    exercise_list jsonb,
    complete boolean,
    user_id int,
    constraint fk_id foreign key(user_id)
    references users(id)
    on delete set null
    on update set default
);

DROP TABLE IF EXISTS Exercise;

CREATE TABLE Exercise (
    id SERIAL PRIMARY KEY,
    name text,
    type text[],
    muscles text[],
    equipment text[]
);