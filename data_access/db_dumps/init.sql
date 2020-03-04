--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1 (Debian 12.1-1.pgdg100+1)
-- Dumped by pg_dump version 12.2 (Ubuntu 12.2-2.pgdg18.04+1)

-- Started on 2020-03-04 11:33:21 CET

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 202 (class 1259 OID 16385)
-- Name: archives; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.archives (
    id integer NOT NULL,
    title text NOT NULL,
    article_text text NOT NULL,
    published_date text,
    newspaper text,
    url text NOT NULL
);


ALTER TABLE public.archives OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16391)
-- Name: archives_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.archives_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.archives_id_seq OWNER TO postgres;

--
-- TOC entry 2934 (class 0 OID 0)
-- Dependencies: 203
-- Name: archives_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.archives_id_seq OWNED BY public.archives.id;


--
-- TOC entry 204 (class 1259 OID 16393)
-- Name: matches; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.matches (
    id integer NOT NULL,
    id_archive integer,
    id_recent_article integer,
    score double precision
);


ALTER TABLE public.matches OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 16396)
-- Name: matches_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.matches_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.matches_id_seq OWNER TO postgres;

--
-- TOC entry 2935 (class 0 OID 0)
-- Dependencies: 205
-- Name: matches_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.matches_id_seq OWNED BY public.matches.id;


--
-- TOC entry 206 (class 1259 OID 16398)
-- Name: recent_articles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.recent_articles (
    id integer NOT NULL,
    title text NOT NULL,
    article_text text NOT NULL,
    published_date text,
    date_added timestamp without time zone DEFAULT CURRENT_DATE,
    newspaper text,
    url text NOT NULL
);


ALTER TABLE public.recent_articles OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 16405)
-- Name: recent_articles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.recent_articles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recent_articles_id_seq OWNER TO postgres;

--
-- TOC entry 2936 (class 0 OID 0)
-- Dependencies: 207
-- Name: recent_articles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.recent_articles_id_seq OWNED BY public.recent_articles.id;


--
-- TOC entry 2791 (class 2604 OID 16407)
-- Name: archives id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.archives ALTER COLUMN id SET DEFAULT nextval('public.archives_id_seq'::regclass);


--
-- TOC entry 2792 (class 2604 OID 16408)
-- Name: matches id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.matches ALTER COLUMN id SET DEFAULT nextval('public.matches_id_seq'::regclass);


--
-- TOC entry 2794 (class 2604 OID 16409)
-- Name: recent_articles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recent_articles ALTER COLUMN id SET DEFAULT nextval('public.recent_articles_id_seq'::regclass);


--
-- TOC entry 2796 (class 2606 OID 16411)
-- Name: archives archives_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.archives
    ADD CONSTRAINT archives_pkey PRIMARY KEY (id);


--
-- TOC entry 2798 (class 2606 OID 16413)
-- Name: matches matches_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.matches
    ADD CONSTRAINT matches_pkey PRIMARY KEY (id);


--
-- TOC entry 2800 (class 2606 OID 16415)
-- Name: recent_articles recent_articles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recent_articles
    ADD CONSTRAINT recent_articles_pkey PRIMARY KEY (id);


--
-- TOC entry 2801 (class 2606 OID 16416)
-- Name: matches matches_id_archive_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.matches
    ADD CONSTRAINT matches_id_archive_fkey FOREIGN KEY (id_archive) REFERENCES public.archives(id);


--
-- TOC entry 2802 (class 2606 OID 16421)
-- Name: matches matches_id_recent_article_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.matches
    ADD CONSTRAINT matches_id_recent_article_fkey FOREIGN KEY (id_recent_article) REFERENCES public.recent_articles(id);


-- Completed on 2020-03-04 11:33:21 CET

--
-- PostgreSQL database dump complete
--

