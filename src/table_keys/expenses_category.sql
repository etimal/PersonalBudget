CREATE TABLE public.expenses_category
(
    id bigserial,
    category character varying(255),
    type character varying(255),
    "group" character varying(255),
    comment character varying(255),
    uploaded_at timestamp without time zone,
    updated_at timestamp without time zone,
    PRIMARY KEY (id)
);