--
-- PostgreSQL database dump
--

-- Dumped from database version 11.7
-- Dumped by pg_dump version 11.7

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

SET default_with_oids = false;

--
-- Name: customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customer (
    "customerID" numeric(8,0) NOT NULL,
    "firstName" character varying NOT NULL,
    "lastName" character varying,
    "userID" integer NOT NULL
);


ALTER TABLE public.customer OWNER TO postgres;

--
-- Name: employee; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employee (
    "employeeID" integer NOT NULL,
    "firstName" character varying NOT NULL,
    "lastName" character varying,
    "SSN" integer NOT NULL,
    salary money,
    "payType" character varying,
    "jobType" character varying,
    "userID" integer,
    bonus money
);


ALTER TABLE public.employee OWNER TO postgres;

--
-- Name: employee_expense; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.employee_expense AS
 SELECT (employeecost.salary + employeecost.bonus)
   FROM public.employee employeecost;


ALTER TABLE public.employee_expense OWNER TO postgres;

--
-- Name: transaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transaction (
    "employeeID" integer NOT NULL,
    "customerID" integer NOT NULL,
    "orderNumber" character varying(20) NOT NULL
);


ALTER TABLE public.transaction OWNER TO postgres;

--
-- Name: employee_sales; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.employee_sales AS
 SELECT count(transaction."orderNumber") AS count,
    transaction."employeeID"
   FROM public.transaction
  GROUP BY transaction."employeeID";


ALTER TABLE public.employee_sales OWNER TO postgres;

--
-- Name: engineer_view; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.engineer_view AS
 SELECT employee."firstName",
    employee."lastName",
    employee."employeeID",
    employee."jobType"
   FROM public.employee;


ALTER TABLE public.engineer_view OWNER TO postgres;

--
-- Name: model; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.model (
    "modelNumber" numeric(10,0) NOT NULL,
    "salePrice" money
);


ALTER TABLE public.model OWNER TO postgres;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    "orderNumber" character varying(20) NOT NULL,
    "billCost" money,
    quantity integer,
    "modelNumber" numeric(10,0)
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: frequency_report; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.frequency_report AS
 SELECT model."modelNumber",
    sum(orders.quantity) AS item_count
   FROM (public.orders
     JOIN public.model USING ("modelNumber"))
  GROUP BY model."modelNumber";


ALTER TABLE public.frequency_report OWNER TO postgres;

--
-- Name: inventory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.inventory (
    "inventoryID" character varying NOT NULL,
    cost money,
    "leadTime" integer,
    category character varying,
    "itemCount" integer,
    "modelNumber" numeric(10,0)
);


ALTER TABLE public.inventory OWNER TO postgres;

--
-- Name: login; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.login (
    "userID" integer NOT NULL,
    priviledge character varying(10),
    "loginTime" timestamp with time zone,
    "logoutTime" timestamp with time zone
);


ALTER TABLE public.login OWNER TO postgres;

--
-- Name: model_expense; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.model_expense AS
 SELECT sum(model."salePrice") AS sum
   FROM public.model;


ALTER TABLE public.model_expense OWNER TO postgres;

--
-- Name: order_report; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.order_report AS
 SELECT model."modelNumber",
    sum(orders.quantity) AS inventory_count
   FROM ((public.model
     JOIN public.orders ON ((model."modelNumber" = orders."modelNumber")))
     JOIN public.inventory ON ((inventory."modelNumber" = model."modelNumber")))
  GROUP BY model."modelNumber";


ALTER TABLE public.order_report OWNER TO postgres;

--
-- Name: revenue_report; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.revenue_report AS
 SELECT transaction."customerID",
    transaction."employeeID",
    sum(orders."billCost") AS sales_revenue
   FROM (public.orders
     JOIN public.transaction USING ("orderNumber"))
  GROUP BY transaction."customerID", transaction."employeeID";


ALTER TABLE public.revenue_report OWNER TO postgres;

--
-- Data for Name: customer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customer ("customerID", "firstName", "lastName", "userID") FROM stdin;
1263	Mark	Chavez	3455
4557	Ismael	Contreras	4879
8989	Louis	Lim	9875
8585	Bryan	Rodriguez	3555
8908	Jose	Gonzalez	3405
\.


--
-- Data for Name: employee; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employee ("employeeID", "firstName", "lastName", "SSN", salary, "payType", "jobType", "userID", bonus) FROM stdin;
5655	Drew	Lopez	3456	$3,456.00	cash	engineer	6789	$10.00
9984	Yeslin	Martinez	5643	$7,884.00	cash	engineer	6543	$20.00
2344	Arieni 	Cabanas	9843	$1,324.00	cash	HR	6944	$20.00
2989	Darryl	Foong	3342	$9,883.00	cash	HR	6421	$10.00
6643	Victor	Roman	7654	$3,833.00	cash	sales	6478	$10.00
\.


--
-- Data for Name: inventory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.inventory ("inventoryID", cost, "leadTime", category, "itemCount", "modelNumber") FROM stdin;
345	$30.00	1	cleaning supplies	10	3514
334	$30.00	2	cleaning supplies	15	3556
312	$30.00	3	cleaning supplies	20	3095
365	$30.00	4	cleaning supplies	25	3035
385	$30.00	5	cleaning supplies	30	3054
378	$40.00	6	bedroom materials	40	3314
311	$40.00	7	bedroom materials	45	3379
390	$40.00	8	bedroom materials	50	4214
356	$40.00	9	bedroom materials	55	4267
344	$40.00	2	bedroom materials	60	4255
\.


--
-- Data for Name: login; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.login ("userID", priviledge, "loginTime", "logoutTime") FROM stdin;
3455	customer	2020-04-15 12:10:10-05	2020-04-15 12:20:10-05
4879	customer	2020-04-15 12:35:10-05	2020-04-15 12:55:10-05
9875	customer	2020-04-15 14:10:10-05	2020-04-15 14:20:10-05
3555	customer	2020-04-15 16:22:10-05	2020-04-15 16:44:10-05
3405	customer	2020-04-15 18:10:10-05	2020-04-15 19:20:10-05
6789	engineer	2020-04-20 12:09:10-05	2020-04-20 16:20:10-05
6543	engineer	2020-04-20 12:30:10-05	2020-04-20 19:55:10-05
6944	HR	2020-04-20 12:00:10-05	2020-04-20 20:20:10-05
6421	HR	2020-04-20 12:10:10-05	2020-04-20 20:50:10-05
6478	sales	2020-04-15 12:15:10-05	2020-04-15 22:20:10-05
\.


--
-- Data for Name: model; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.model ("modelNumber", "salePrice") FROM stdin;
3514	$25.00
3556	$25.00
3095	$20.00
3035	$20.00
3054	$20.00
3314	$30.00
3379	$30.00
4214	$40.00
4267	$40.00
4255	$40.00
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders ("orderNumber", "billCost", quantity, "modelNumber") FROM stdin;
ES345	$20.00	10	3514
ES389	$25.00	15	3556
ES309	$30.00	20	3095
ES378	$35.00	25	3035
ES355	$40.00	30	3054
ES334	$45.00	35	3314
ES387	$50.00	40	3379
FS465	$55.00	45	4214
FS456	$60.00	50	4267
FS498	$65.00	55	4255
\.


--
-- Data for Name: transaction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transaction ("employeeID", "customerID", "orderNumber") FROM stdin;
5655	1263	ES345
6643	4557	ES389
6643	8989	ES309
2344	8585	ES378
2344	8908	ES355
\.


--
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY ("customerID");


--
-- Name: employee employee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY ("employeeID");


--
-- Name: inventory inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY ("inventoryID");


--
-- Name: login login_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login
    ADD CONSTRAINT login_pkey PRIMARY KEY ("userID");


--
-- Name: model modelNumber; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model
    ADD CONSTRAINT "modelNumber" UNIQUE ("modelNumber");


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY ("orderNumber");


--
-- Name: transaction customerID; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT "customerID" FOREIGN KEY ("customerID") REFERENCES public.customer("customerID") NOT VALID;


--
-- Name: transaction employeeID; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT "employeeID" FOREIGN KEY ("employeeID") REFERENCES public.employee("employeeID") NOT VALID;


--
-- Name: inventory modelNumber; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT "modelNumber" FOREIGN KEY ("modelNumber") REFERENCES public.model("modelNumber") NOT VALID;


--
-- Name: orders modelNumber; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT "modelNumber" FOREIGN KEY ("modelNumber") REFERENCES public.model("modelNumber") NOT VALID;


--
-- Name: transaction orderNumber; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT "orderNumber" FOREIGN KEY ("orderNumber") REFERENCES public.orders("orderNumber") NOT VALID;


--
-- Name: customer userID; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT "userID" FOREIGN KEY ("userID") REFERENCES public.login("userID") NOT VALID;


--
-- Name: employee userID; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT "userID" FOREIGN KEY ("userID") REFERENCES public.login("userID") NOT VALID;


--
-- Name: TABLE customer; Type: ACL; Schema: public; Owner: postgres
--

--GRANT SELECT ON TABLE public.customer TO test;
GRANT ALL ON TABLE public.customer TO admin WITH GRANT OPTION;
GRANT SELECT,UPDATE ON TABLE public.customer TO sales;


--
-- Name: TABLE employee; Type: ACL; Schema: public; Owner: postgres
--

--GRANT SELECT ON TABLE public.employee TO test;
GRANT ALL ON TABLE public.employee TO admin WITH GRANT OPTION;
GRANT SELECT,UPDATE ON TABLE public.employee TO hr;


--
-- Name: TABLE employee_expense; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.employee_expense TO admin;


--
-- Name: TABLE transaction; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.transaction TO admin WITH GRANT OPTION;


--
-- Name: TABLE employee_sales; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.employee_sales TO hr;


--
-- Name: TABLE engineer_view; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.engineer_view TO engineer;


--
-- Name: TABLE model; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.model TO admin WITH GRANT OPTION;
GRANT SELECT,UPDATE ON TABLE public.model TO engineer;


--
-- Name: TABLE orders; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.orders TO admin WITH GRANT OPTION;
GRANT SELECT,INSERT ON TABLE public.orders TO sales;


--
-- Name: TABLE frequency_report; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.frequency_report TO admin;


--
-- Name: TABLE inventory; Type: ACL; Schema: public; Owner: postgres
--

--GRANT SELECT ON TABLE public.inventory TO test;
GRANT ALL ON TABLE public.inventory TO admin WITH GRANT OPTION;
GRANT SELECT,UPDATE ON TABLE public.inventory TO engineer;


--
-- Name: TABLE model_expense; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.model_expense TO admin;


--
-- Name: TABLE order_report; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.order_report TO admin;


--
-- Name: TABLE revenue_report; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.revenue_report TO admin;


--
-- PostgreSQL database dump complete
--

