CREATE TABLE public.investment_ytd
(
    id bigserial,
    date date,
    month character varying(255),
    amount real,
    comment character varying(255),
    source_period date,
    source_name character varying(255),
    db_update timestamp without time zone,
    PRIMARY KEY (id)
);