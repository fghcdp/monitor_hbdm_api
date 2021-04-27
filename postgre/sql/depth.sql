-- Table: public.depth

-- DROP TABLE public.depth;

CREATE TABLE public.depth
(
    id serial NOT NULL,
    mrid bigint NOT NULL,
    contract_type character(255) COLLATE pg_catalog."default" NOT NULL,
    ts bigint NOT NULL,
    event character(255) COLLATE pg_catalog."default",
    contract_code character(255) COLLATE pg_catalog."default" NOT NULL,
    data_ts bigint,
    bid20_p numeric,
    bid20_v numeric,
    ask20_p numeric,
    ask20_v numeric,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT depth_id PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.depth
    OWNER to postgres;

GRANT SELECT ON TABLE public.depth TO hbdm_api;

GRANT ALL ON TABLE public.depth TO postgres;
-- Index: depth_ca

-- DROP INDEX public.depth_ca;

CREATE INDEX depth_ca
    ON public.depth USING btree
    (created_at ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: depth_ct

-- DROP INDEX public.depth_ct;

CREATE INDEX depth_ct
    ON public.depth USING btree
    (contract_type COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;