CREATE TABLE public.accounts_balance
(
    id bigserial,
    account character varying(255),
    last_balance real,
    period date,
    assignment character varying(255),
    incomes real,
    transfers real,
    amount real,
    expenses real,
    total_period real,
    total_account real,
    new_balance real,
    check_date date,
    source_period date,
    source_name character varying(255),
    db_update timestamp without time zone,
    PRIMARY KEY (id)
);