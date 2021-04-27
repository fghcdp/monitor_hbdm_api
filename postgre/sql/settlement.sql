-- Table: public.settlement

-- DROP TABLE public.settlement;

CREATE TABLE public.settlement
(
    contract_type character(255) COLLATE pg_catalog."default" NOT NULL,
    ts bigint NOT NULL,
    event character(255) COLLATE pg_catalog."default",
    contract_code character(255) COLLATE pg_catalog."default" NOT NULL,
    contract_status bigint,
    settlement_date bigint,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT settlement_id PRIMARY KEY (contract_type, ts, contract_code)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.settlement
    OWNER to postgres;

GRANT SELECT ON TABLE public.settlement TO hbdm_api;

GRANT ALL ON TABLE public.settlement TO postgres;
-- Index: settlement_ca

-- DROP INDEX public.settlement_ca;

CREATE INDEX settlement_ca
    ON public.settlement USING btree
    (created_at ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: settlement_ct

-- DROP INDEX public.settlement_ct;

CREATE INDEX settlement_ct
    ON public.settlement USING btree
    (contract_type COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;