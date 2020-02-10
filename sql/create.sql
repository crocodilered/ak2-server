--
-- PostgreSQL database dump
--

-- Dumped from database version 12.0
-- Dumped by pg_dump version 12.0

-- Started on 2020-02-04 18:47:04

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
-- TOC entry 6 (class 2615 OID 78608)
-- Name: ak2; Type: SCHEMA; Schema: -; Owner: ak2
--

CREATE SCHEMA ak2;


ALTER SCHEMA ak2 OWNER TO ak2;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 209 (class 1259 OID 78652)
-- Name: i18n; Type: TABLE; Schema: ak2; Owner: ak2
--

CREATE TABLE ak2.i18n (
    video_id bigint,
    section_id bigint,
    lang character(2) NOT NULL,
    value character varying(2000) NOT NULL,
    code character varying(50) NOT NULL
);


ALTER TABLE ak2.i18n OWNER TO ak2;

--
-- TOC entry 210 (class 1259 OID 78841)
-- Name: place_id_seq; Type: SEQUENCE; Schema: ak2; Owner: ak2
--

CREATE SEQUENCE ak2.place_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ak2.place_id_seq OWNER TO ak2;

--
-- TOC entry 211 (class 1259 OID 78843)
-- Name: place; Type: TABLE; Schema: ak2; Owner: ak2
--

CREATE TABLE ak2.place (
    id bigint DEFAULT nextval('ak2.place_id_seq'::regclass) NOT NULL,
    owner_id bigint NOT NULL,
    lng double precision NOT NULL,
    lat double precision NOT NULL,
    enabled boolean NOT NULL,
    CONSTRAINT place_lat_check CHECK (((lat > ('-90'::integer)::double precision) AND (lat <= (90)::double precision))),
    CONSTRAINT place_lng_check CHECK (((lng > ('-180'::integer)::double precision) AND (lng <= (180)::double precision)))
);


ALTER TABLE ak2.place OWNER TO ak2;

--
-- TOC entry 206 (class 1259 OID 78630)
-- Name: section_id_seq; Type: SEQUENCE; Schema: ak2; Owner: ak2
--

CREATE SEQUENCE ak2.section_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ak2.section_id_seq OWNER TO ak2;

--
-- TOC entry 205 (class 1259 OID 78622)
-- Name: section; Type: TABLE; Schema: ak2; Owner: ak2
--

CREATE TABLE ak2.section (
    id bigint DEFAULT nextval('ak2.section_id_seq'::regclass) NOT NULL,
    parent_id bigint DEFAULT 0 NOT NULL,
    enabled boolean NOT NULL,
    order_key bigint DEFAULT round(date_part('epoch'::text, now())) NOT NULL
);


ALTER TABLE ak2.section OWNER TO ak2;

--
-- TOC entry 204 (class 1259 OID 78617)
-- Name: user_id_seq; Type: SEQUENCE; Schema: ak2; Owner: ak2
--

CREATE SEQUENCE ak2.user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ak2.user_id_seq OWNER TO ak2;

--
-- TOC entry 203 (class 1259 OID 78609)
-- Name: user; Type: TABLE; Schema: ak2; Owner: ak2
--

CREATE TABLE ak2."user" (
    id bigint DEFAULT nextval('ak2.user_id_seq'::regclass) NOT NULL,
    name character varying(200),
    email character varying(200) NOT NULL,
    password character varying(200) NOT NULL,
    authorized boolean NOT NULL,
    enabled boolean NOT NULL,
    admin boolean NOT NULL,
    subscribed_till date
);


ALTER TABLE ak2."user" OWNER TO ak2;

--
-- TOC entry 2886 (class 0 OID 0)
-- Dependencies: 203
-- Name: TABLE "user"; Type: COMMENT; Schema: ak2; Owner: ak2
--

COMMENT ON TABLE ak2."user" IS 'System users.';


--
-- TOC entry 207 (class 1259 OID 78634)
-- Name: video_id_seq; Type: SEQUENCE; Schema: ak2; Owner: ak2
--

CREATE SEQUENCE ak2.video_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ak2.video_id_seq OWNER TO ak2;

--
-- TOC entry 208 (class 1259 OID 78636)
-- Name: video; Type: TABLE; Schema: ak2; Owner: ak2
--

CREATE TABLE ak2.video (
    id bigint DEFAULT nextval('ak2.video_id_seq'::regclass) NOT NULL,
    section_id bigint NOT NULL,
    media_fp character varying(1000) NOT NULL,
    enabled boolean NOT NULL,
    order_key bigint DEFAULT round(date_part('epoch'::text, now())) NOT NULL
);


ALTER TABLE ak2.video OWNER TO ak2;


--
-- TOC entry 2887 (class 0 OID 0)
-- Dependencies: 210
-- Name: place_id_seq; Type: SEQUENCE SET; Schema: ak2; Owner: ak2
--

SELECT pg_catalog.setval('ak2.place_id_seq', 1, false);


--
-- TOC entry 2888 (class 0 OID 0)
-- Dependencies: 206
-- Name: section_id_seq; Type: SEQUENCE SET; Schema: ak2; Owner: ak2
--

SELECT pg_catalog.setval('ak2.section_id_seq', 18, true);


--
-- TOC entry 2889 (class 0 OID 0)
-- Dependencies: 204
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: ak2; Owner: ak2
--

SELECT pg_catalog.setval('ak2.user_id_seq', 3, true);


--
-- TOC entry 2890 (class 0 OID 0)
-- Dependencies: 207
-- Name: video_id_seq; Type: SEQUENCE SET; Schema: ak2; Owner: ak2
--

SELECT pg_catalog.setval('ak2.video_id_seq', 9, true);


--
-- TOC entry 2737 (class 2606 OID 78673)
-- Name: i18n i18n_unique; Type: CONSTRAINT; Schema: ak2; Owner: ak2
--

ALTER TABLE ONLY ak2.i18n
    ADD CONSTRAINT i18n_unique UNIQUE (video_id, section_id, lang, code);


--
-- TOC entry 2740 (class 2606 OID 78850)
-- Name: place place_pkey; Type: CONSTRAINT; Schema: ak2; Owner: ak2
--

ALTER TABLE ONLY ak2.place
    ADD CONSTRAINT place_pkey PRIMARY KEY (id);


--
-- TOC entry 2729 (class 2606 OID 78629)
-- Name: section section_pkey; Type: CONSTRAINT; Schema: ak2; Owner: ak2
--

ALTER TABLE ONLY ak2.section
    ADD CONSTRAINT section_pkey PRIMARY KEY (id);


--
-- TOC entry 2724 (class 2606 OID 78621)
-- Name: user user_email; Type: CONSTRAINT; Schema: ak2; Owner: ak2
--

ALTER TABLE ONLY ak2."user"
    ADD CONSTRAINT user_email UNIQUE (email);


--
-- TOC entry 2726 (class 2606 OID 78616)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: ak2; Owner: ak2
--

ALTER TABLE ONLY ak2."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 2733 (class 2606 OID 78643)
-- Name: video video_pkey; Type: CONSTRAINT; Schema: ak2; Owner: ak2
--

ALTER TABLE ONLY ak2.video
    ADD CONSTRAINT video_pkey PRIMARY KEY (id);


--
-- TOC entry 2734 (class 1259 OID 78671)
-- Name: fki_i18n_fkey_section; Type: INDEX; Schema: ak2; Owner: ak2
--

CREATE INDEX fki_i18n_fkey_section ON ak2.i18n USING btree (section_id);


--
-- TOC entry 2735 (class 1259 OID 78665)
-- Name: fki_i18n_fkey_video; Type: INDEX; Schema: ak2; Owner: ak2
--

CREATE INDEX fki_i18n_fkey_video ON ak2.i18n USING btree (video_id);


--
-- TOC entry 2730 (class 1259 OID 78650)
-- Name: fki_video_fkey_section; Type: INDEX; Schema: ak2; Owner: ak2
--

CREATE INDEX fki_video_fkey_section ON ak2.video USING btree (section_id);


--
-- TOC entry 2738 (class 1259 OID 78851)
-- Name: ix_place_enabled; Type: INDEX; Schema: ak2; Owner: ak2
--

CREATE INDEX ix_place_enabled ON ak2.place USING btree (enabled);


--
-- TOC entry 2727 (class 1259 OID 78633)
-- Name: ix_section_enabled; Type: INDEX; Schema: ak2; Owner: ak2
--

CREATE INDEX ix_section_enabled ON ak2.section USING btree (enabled);


--
-- TOC entry 2731 (class 1259 OID 78651)
-- Name: ix_video_enabled; Type: INDEX; Schema: ak2; Owner: ak2
--

CREATE INDEX ix_video_enabled ON ak2.video USING btree (enabled);


--
-- TOC entry 2743 (class 2606 OID 78682)
-- Name: i18n i18n_fkey_section; Type: FK CONSTRAINT; Schema: ak2; Owner: ak2
--

ALTER TABLE ONLY ak2.i18n
    ADD CONSTRAINT i18n_fkey_section FOREIGN KEY (section_id) REFERENCES ak2.section(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2742 (class 2606 OID 78677)
-- Name: i18n i18n_fkey_video; Type: FK CONSTRAINT; Schema: ak2; Owner: ak2
--

ALTER TABLE ONLY ak2.i18n
    ADD CONSTRAINT i18n_fkey_video FOREIGN KEY (video_id) REFERENCES ak2.video(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2741 (class 2606 OID 78645)
-- Name: video video_fkey_section; Type: FK CONSTRAINT; Schema: ak2; Owner: ak2
--

ALTER TABLE ONLY ak2.video
    ADD CONSTRAINT video_fkey_section FOREIGN KEY (section_id) REFERENCES ak2.section(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2884 (class 0 OID 0)
-- Dependencies: 206
-- Name: SEQUENCE section_id_seq; Type: ACL; Schema: ak2; Owner: ak2
--

REVOKE ALL ON SEQUENCE ak2.section_id_seq FROM ak2;
GRANT SELECT,USAGE ON SEQUENCE ak2.section_id_seq TO ak2;


--
-- TOC entry 2885 (class 0 OID 0)
-- Dependencies: 204
-- Name: SEQUENCE user_id_seq; Type: ACL; Schema: ak2; Owner: ak2
--

REVOKE ALL ON SEQUENCE ak2.user_id_seq FROM ak2;
GRANT SELECT,USAGE ON SEQUENCE ak2.user_id_seq TO ak2;


-- Completed on 2020-02-04 18:47:05

--
-- PostgreSQL database dump complete
--

