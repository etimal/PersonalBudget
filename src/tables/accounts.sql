CREATE TABLE public.accounts
(
    id bigserial,
    account_id integer,
    account character varying(255),
    currency character varying(255),
    country character varying(255),
    item character varying(255),
    type character varying(255),
    comment character varying(255),
    source_period character varying(255),
    source_name character varying(255),
    db_update date,
    PRIMARY KEY (id)
);