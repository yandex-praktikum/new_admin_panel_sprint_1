--
-- PostgreSQL database dump
--

-- Dumped from database version 15.6 (Debian 15.6-1.pgdg120+2)
-- Dumped by pg_dump version 15.6 (Debian 15.6-1.pgdg120+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: content; Type: SCHEMA; Schema: -; Owner: app
--

CREATE SCHEMA content;


ALTER SCHEMA content OWNER TO app;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: filmwork; Type: TABLE; Schema: content; Owner: app
--

CREATE TABLE content.filmwork (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    premiere_date date,
    type character varying(10) NOT NULL,
    rating double precision,
    file_path character varying(255)
);


ALTER TABLE content.filmwork OWNER TO app;

--
-- Name: genre; Type: TABLE; Schema: content; Owner: app
--

CREATE TABLE content.genre (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE content.genre OWNER TO app;

--
-- Name: genre_film_work; Type: TABLE; Schema: content; Owner: app
--

CREATE TABLE content.genre_film_work (
    id uuid NOT NULL,
    created timestamp with time zone NOT NULL,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL
);


ALTER TABLE content.genre_film_work OWNER TO app;

--
-- Name: person; Type: TABLE; Schema: content; Owner: app
--

CREATE TABLE content.person (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    full_name character varying(255) NOT NULL,
    gender text
);


ALTER TABLE content.person OWNER TO app;

--
-- Name: person_film_work; Type: TABLE; Schema: content; Owner: app
--

CREATE TABLE content.person_film_work (
    id uuid NOT NULL,
    role character varying(20),
    created timestamp with time zone NOT NULL,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL
);


ALTER TABLE content.person_film_work OWNER TO app;

--
-- Name: person_film_work film_work_id_person_id_uniq; Type: CONSTRAINT; Schema: content; Owner: app
--

ALTER TABLE ONLY content.person_film_work
    ADD CONSTRAINT film_work_id_person_id_uniq UNIQUE (role, film_work_id, person_id);


--
-- Name: filmwork filmwork_pkey; Type: CONSTRAINT; Schema: content; Owner: app
--

ALTER TABLE ONLY content.filmwork
    ADD CONSTRAINT filmwork_pkey PRIMARY KEY (id);


--
-- Name: genre_film_work genre_film_work_film_work_id_genre_id_uniq; Type: CONSTRAINT; Schema: content; Owner: app
--

ALTER TABLE ONLY content.genre_film_work
    ADD CONSTRAINT genre_film_work_film_work_id_genre_id_uniq UNIQUE (film_work_id, genre_id);


--
-- Name: genre_film_work genre_film_work_pkey; Type: CONSTRAINT; Schema: content; Owner: app
--

ALTER TABLE ONLY content.genre_film_work
    ADD CONSTRAINT genre_film_work_pkey PRIMARY KEY (id);


--
-- Name: genre genre_pkey; Type: CONSTRAINT; Schema: content; Owner: app
--

ALTER TABLE ONLY content.genre
    ADD CONSTRAINT genre_pkey PRIMARY KEY (id);


--
-- Name: person_film_work person_film_work_pkey; Type: CONSTRAINT; Schema: content; Owner: app
--

ALTER TABLE ONLY content.person_film_work
    ADD CONSTRAINT person_film_work_pkey PRIMARY KEY (id);


--
-- Name: person person_pkey; Type: CONSTRAINT; Schema: content; Owner: app
--

ALTER TABLE ONLY content.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (id);


--
-- Name: genre_film_work_film_work_id_65abe300; Type: INDEX; Schema: content; Owner: app
--

CREATE INDEX genre_film_work_film_work_id_65abe300 ON content.genre_film_work USING btree (film_work_id);


--
-- Name: genre_film_work_genre_id_88fbcf0d; Type: INDEX; Schema: content; Owner: app
--

CREATE INDEX genre_film_work_genre_id_88fbcf0d ON content.genre_film_work USING btree (genre_id);


--
-- Name: person_film_work_film_work_id_1724c536; Type: INDEX; Schema: content; Owner: app
--

CREATE INDEX person_film_work_film_work_id_1724c536 ON content.person_film_work USING btree (film_work_id);


--
-- Name: person_film_work_person_id_196d24de; Type: INDEX; Schema: content; Owner: app
--

CREATE INDEX person_film_work_person_id_196d24de ON content.person_film_work USING btree (person_id);


--
-- Name: genre_film_work genre_film_work_film_work_id_65abe300_fk_filmwork_id; Type: FK CONSTRAINT; Schema: content; Owner: app
--

ALTER TABLE ONLY content.genre_film_work
    ADD CONSTRAINT genre_film_work_film_work_id_65abe300_fk_filmwork_id FOREIGN KEY (film_work_id) REFERENCES content.filmwork(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genre_film_work genre_film_work_genre_id_88fbcf0d_fk_genre_id; Type: FK CONSTRAINT; Schema: content; Owner: app
--

ALTER TABLE ONLY content.genre_film_work
    ADD CONSTRAINT genre_film_work_genre_id_88fbcf0d_fk_genre_id FOREIGN KEY (genre_id) REFERENCES content.genre(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: person_film_work person_film_work_film_work_id_1724c536_fk_filmwork_id; Type: FK CONSTRAINT; Schema: content; Owner: app
--

ALTER TABLE ONLY content.person_film_work
    ADD CONSTRAINT person_film_work_film_work_id_1724c536_fk_filmwork_id FOREIGN KEY (film_work_id) REFERENCES content.filmwork(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: person_film_work person_film_work_person_id_196d24de_fk_person_id; Type: FK CONSTRAINT; Schema: content; Owner: app
--

ALTER TABLE ONLY content.person_film_work
    ADD CONSTRAINT person_film_work_person_id_196d24de_fk_person_id FOREIGN KEY (person_id) REFERENCES content.person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--