CREATE TABLE public.credit_accounts
(
    id bigserial,
    start_date date,
    final_date date,
    account character varying(255),
    currency character varying(255),
    debt real,
    payment real,
    payment_date date,
    comment character varying(255),
    source_period character varying(255),
    source_name character varying(255),
    db_update timestamp without time zone,
    PRIMARY KEY (id)
);