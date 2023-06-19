CREATE TABLE public.investment
(
    id bigserial,
    date date,
    account character varying(255),
    amount real,
    comment character varying(255),
    source_period date,
    source_name character varying(255),
    db_update timestamp without time zone,
    PRIMARY KEY (id)
);