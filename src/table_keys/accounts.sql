CREATE TABLE public.accounts
(
    id bigserial,
    account character varying(255),
    currency character varying(255),
    country character varying(255),
    item character varying(255),
    type character varying(255),
    active boolean,
    comment character varying(255),
    uploaded_at timestamp without time zone,
    updated_at timestamp without time zone,
    PRIMARY KEY (id)
);