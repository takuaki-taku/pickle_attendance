--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Homebrew)
-- Dumped by pg_dump version 14.13 (Homebrew)

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: event_manager_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO event_manager_user;

--
-- Name: event; Type: TABLE; Schema: public; Owner: event_manager_user
--

CREATE TABLE public.event (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    start timestamp without time zone NOT NULL,
    "end" timestamp without time zone NOT NULL,
    location character varying(255),
    color character varying(20),
    created_by integer NOT NULL
);


ALTER TABLE public.event OWNER TO event_manager_user;

--
-- Name: event_id_seq; Type: SEQUENCE; Schema: public; Owner: event_manager_user
--

CREATE SEQUENCE public.event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.event_id_seq OWNER TO event_manager_user;

--
-- Name: event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: event_manager_user
--

ALTER SEQUENCE public.event_id_seq OWNED BY public.event.id;


--
-- Name: participant; Type: TABLE; Schema: public; Owner: event_manager_user
--

CREATE TABLE public.participant (
    id integer NOT NULL,
    event_id integer NOT NULL,
    user_id integer NOT NULL,
    status character varying(20)
);


ALTER TABLE public.participant OWNER TO event_manager_user;

--
-- Name: participant_id_seq; Type: SEQUENCE; Schema: public; Owner: event_manager_user
--

CREATE SEQUENCE public.participant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.participant_id_seq OWNER TO event_manager_user;

--
-- Name: participant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: event_manager_user
--

ALTER SEQUENCE public.participant_id_seq OWNED BY public.participant.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: event_manager_user
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    password_hash character varying(256),
    is_admin boolean
);


ALTER TABLE public."user" OWNER TO event_manager_user;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: event_manager_user
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO event_manager_user;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: event_manager_user
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: event id; Type: DEFAULT; Schema: public; Owner: event_manager_user
--

ALTER TABLE ONLY public.event ALTER COLUMN id SET DEFAULT nextval('public.event_id_seq'::regclass);


--
-- Name: participant id; Type: DEFAULT; Schema: public; Owner: event_manager_user
--

ALTER TABLE ONLY public.participant ALTER COLUMN id SET DEFAULT nextval('public.participant_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: event_manager_user
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: event_manager_user
--

COPY public.alembic_version (version_num) FROM stdin;
ee012dbfb912
\.


--
-- Data for Name: event; Type: TABLE DATA; Schema: public; Owner: event_manager_user
--

COPY public.event (id, title, start, "end", location, color, created_by) FROM stdin;
1	LYNX 4 courts	2024-11-06 09:00:00	2024-11-06 12:00:00	LYNX Tennis Academy	#3788d8	1
2	LYNX 4 courts	2024-11-13 09:00:00	2024-11-13 12:00:00	LYNX Tennis Academy	#3788d8	1
3	LYNX 4 courts	2024-11-20 09:00:00	2024-11-20 12:00:00	LYNX Tennis Academy	#3788d8	1
4	LYNX 4 courts	2024-11-27 09:00:00	2024-11-27 12:00:00	LYNX Tennis Academy	#3788d8	1
5	Yawata 2F 2 courts	2024-11-02 18:00:00	2024-11-02 21:00:00	八幡市民体育館	#dc3545	1
6	Yawata Arena 4 courts	2024-11-09 15:00:00	2024-11-09 18:00:00	八幡市民体育館	#dc3545	1
7	Yawata 2F 2 courts	2024-11-16 18:00:00	2024-11-16 21:00:00	八幡市民体育館	#dc3545	1
8	Seseragi 1court	2024-11-16 13:00:00	2024-11-16 17:00:00	せせらぎ体育館	#ffc107	1
9	Yawata 2F 2 courts	2024-11-23 09:00:00	2024-11-23 12:00:00	八幡市民体育館	#dc3545	1
10	Seseragi 1court	2024-11-23 13:00:00	2024-11-23 17:00:00	せせらぎ体育館	#ffc107	1
11	Yawata 2F 1 court	2024-11-01 18:00:00	2024-11-01 21:00:00	八幡市民体育館	#dc3545	1
12	Yawata 2F 2 courts	2024-11-08 18:00:00	2024-11-08 21:00:00	八幡市民体育館	#dc3545	1
13	Yawata 2F 1 court	2024-11-15 18:00:00	2024-11-15 21:00:00	八幡市民体育館	#dc3545	1
14	Yawata Arena 4 court	2024-11-22 18:00:00	2024-11-22 21:00:00	八幡市民体育館	#dc3545	1
15	Yawata 2F 1 court	2024-11-29 18:00:00	2024-11-29 21:00:00	八幡市民体育館	#dc3545	1
16	Kyotanabe 3 courts	2024-11-05 04:00:00	2024-11-05 07:00:00	京田辺中央体育館	#6f42c1	1
17	Kyotanabe 3 courts	2024-11-12 04:00:00	2024-11-12 07:00:00	京田辺中央体育館	#6f42c1	1
18	Kyotanabe 3 courts	2024-11-19 04:00:00	2024-11-19 07:00:00	京田辺中央体育館	#6f42c1	1
19	Kyotanabe 3 courts	2024-11-26 04:00:00	2024-11-26 07:00:00	京田辺中央体育館	#6f42c1	1
20	Kusauchi 3 courts	2024-11-30 00:00:00	2024-11-30 03:00:00	草内小学校	#28a745	1
\.


--
-- Data for Name: participant; Type: TABLE DATA; Schema: public; Owner: event_manager_user
--

COPY public.participant (id, event_id, user_id, status) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: event_manager_user
--

COPY public."user" (id, username, password_hash, is_admin) FROM stdin;
2	sample	scrypt:32768:8:1$hp3p6p19VgawxS09$e55dd7b9931d2e8dee02e00f9e333f5c07007e449f5802705844c03603e265dd20c2db97a9942b465f1a885ea5dd1d4a00e6350abef82d3034d027f787a29651	f
1	東	scrypt:32768:8:1$ay1KVgZmgxGcxYXo$a9e506d9ea0f7a9b95c55c230ef8965fc20a21024a5c300ce5898554c3c0370bb03445456c75e18782ab61b2446a69bf4060390861163080ff83e10e35051f37	t
\.


--
-- Name: event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: event_manager_user
--

SELECT pg_catalog.setval('public.event_id_seq', 20, true);


--
-- Name: participant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: event_manager_user
--

SELECT pg_catalog.setval('public.participant_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: event_manager_user
--

SELECT pg_catalog.setval('public.user_id_seq', 2, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: event_manager_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: event event_pkey; Type: CONSTRAINT; Schema: public; Owner: event_manager_user
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_pkey PRIMARY KEY (id);


--
-- Name: participant participant_pkey; Type: CONSTRAINT; Schema: public; Owner: event_manager_user
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: event_manager_user
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: event_manager_user
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: event event_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: event_manager_user
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_created_by_fkey FOREIGN KEY (created_by) REFERENCES public."user"(id);


--
-- Name: participant participant_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: event_manager_user
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.event(id);


--
-- Name: participant participant_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: event_manager_user
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

