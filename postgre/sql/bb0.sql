-- Table: public.bbo

-- DROP TABLE public.bbo;

CREATE TABLE public.bbo
(
    id integer NOT NULL DEFAULT nextval('bbo_id_seq'::regclass),
    mrid bigint NOT NULL,
    contract_type character(255) COLLATE pg_catalog."default" NOT NULL,
    ts bigint NOT NULL,
    contract_code character(255) COLLATE pg_catalog."default" NOT NULL,
    data_ts bigint,
    bid1_p numeric,
    bid1_v numeric,
    ask1_p numeric,
    ask1_v numeric,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT bbo_id PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.bbo
    OWNER to postgres;

GRANT SELECT ON TABLE public.bbo TO hbdm_api;

GRANT ALL ON TABLE public.bbo TO postgres;
-- Index: bbo_ca

-- DROP INDEX public.bbo_ca;

CREATE INDEX bbo_ca
    ON public.bbo USING btree
    (created_at ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: bbo_ct

-- DROP INDEX public.bbo_ct;

CREATE INDEX bbo_ct
    ON public.bbo USING btree
    (contract_type COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;