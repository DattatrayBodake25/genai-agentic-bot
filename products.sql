--
-- PostgreSQL database dump
--

\restrict eA5ZvJw4MX9wlWhVTQgGN7nLydMDTciRL2byRaeL4SVoWdov3LHeSlUvVrNJwuH

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

-- Started on 2025-09-28 21:34:30

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 218 (class 1259 OID 16544)
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying(100),
    price numeric,
    stock integer,
    category character varying(50),
    discount numeric
);


ALTER TABLE public.products OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16543)
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO postgres;

--
-- TOC entry 4896 (class 0 OID 0)
-- Dependencies: 217
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- TOC entry 4741 (class 2604 OID 16547)
-- Name: products id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- TOC entry 4890 (class 0 OID 16544)
-- Dependencies: 218
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (id, name, price, stock, category, discount) FROM stdin;
2	Phone	30000	25	Electronics	10
3	Headphones	2500	50	Accessories	15
4	Smartwatch	12000	30	Electronics	0
5	Backpack	1500	40	Fashion	5
6	Shoes	3500	60	Fashion	10
7	Tablet	20000	20	Electronics	5
8	Monitor	10000	15	Electronics	0
9	Keyboard	1500	70	Accessories	10
10	Mouse	800	100	Accessories	5
11	Camera	45000	12	Electronics	8
12	Printer	7000	18	Electronics	0
13	T-shirt	800	50	Fashion	15
14	Jeans	1800	40	Fashion	10
15	Speaker	4000	25	Electronics	5
16	Test Product	1000	10	Category	0
1	Laptop	99999	5	Electronics	5
17	Laptop Pro	1200	15	Electronics	0
\.


--
-- TOC entry 4897 (class 0 OID 0)
-- Dependencies: 217
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_seq', 17, true);


--
-- TOC entry 4743 (class 2606 OID 16551)
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


-- Completed on 2025-09-28 21:34:31

--
-- PostgreSQL database dump complete
--

\unrestrict eA5ZvJw4MX9wlWhVTQgGN7nLydMDTciRL2byRaeL4SVoWdov3LHeSlUvVrNJwuH

