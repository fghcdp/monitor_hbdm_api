-- Table: public.domain

-- DROP TABLE public.domain;

CREATE TABLE public.domain
(
    contract_type character(255) COLLATE pg_catalog."default" NOT NULL,
    domain character(255) COLLATE pg_catalog."default",
    event character(255) COLLATE pg_catalog."default",
    contract_code character(255) COLLATE pg_catalog."default",
    local_ts bigint NOT NULL,
    data_ts numeric,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT domain_id PRIMARY KEY (contract_type, local_ts)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.domain
    OWNER to postgres;

GRANT SELECT ON TABLE public.domain TO hbdm_api;

GRANT ALL ON TABLE public.domain TO postgres;
-- Index: domain_ca

-- DROP INDEX public.domain_ca;

CREATE INDEX domain_ca
    ON public.domain USING btree
    (created_at ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: domain_ct

-- DROP INDEX public.domain_ct;

CREATE INDEX domain_ct
    ON public.domain USING btree
    (contract_type COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;