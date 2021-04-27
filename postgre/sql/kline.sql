-- Table: public.kline

-- DROP TABLE public.kline;

CREATE TABLE public.kline
(
    id serial NOT NULL,
    mrid bigint NOT NULL,
    contract_type character(255) COLLATE pg_catalog."default" NOT NULL,
    ts bigint NOT NULL,
    event character(255) COLLATE pg_catalog."default",
    contract_code character(255) COLLATE pg_catalog."default" NOT NULL,
    data_ts bigint,
    close numeric,
    amount numeric,
    trade_turnover numeric,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT kline_id PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.kline
    OWNER to postgres;

GRANT SELECT ON TABLE public.kline TO hbdm_api;

GRANT ALL ON TABLE public.kline TO postgres;
-- Index: kline_ca

-- DROP INDEX public.kline_ca;

CREATE INDEX kline_ca
    ON public.kline USING btree
    (created_at ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: kline_ct

-- DROP INDEX public.kline_ct;

CREATE INDEX kline_ct
    ON public.kline USING btree
    (contract_type COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;