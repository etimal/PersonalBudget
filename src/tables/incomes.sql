CREATE TABLE public.incomes
(
    id bigserial,
    date date,
    account character varying(255),
    description character varying(255),
    status character varying(255),
    amount real,
    source_period character varying(255),
    source_name character varying(255),
    db_update timestamp without time zone,
    PRIMARY KEY (id)
);