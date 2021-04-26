-- Table: public.funding_rate

-- DROP TABLE public.funding_rate;

CREATE TABLE public.funding_rate
(
    contract_type character(255) COLLATE pg_catalog."default" NOT NULL,
    ts bigint NOT NULL,
    contract_code character(255) COLLATE pg_catalog."default" NOT NULL,
    fee_asset character(255) COLLATE pg_catalog."default",
    funding_time numeric,
    funding_rate numeric,
    estimated_rate numeric,
    settlement_time numeric,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT funding_rate_id PRIMARY KEY (contract_type, ts, contract_code)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.funding_rate
    OWNER to postgres;

GRANT SELECT ON TABLE public.funding_rate TO hbdm_api;

GRANT ALL ON TABLE public.funding_rate TO postgres;
-- Index: funding_rate_ca

-- DROP INDEX public.funding_rate_ca;

CREATE INDEX funding_rate_ca
    ON public.funding_rate USING btree
    (created_at ASC NULLS LAST)
    TABLESPACE pg_default;