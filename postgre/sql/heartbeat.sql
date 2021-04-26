-- Table: public.heartbeat

-- DROP TABLE public.heartbeat;

CREATE TABLE public.heartbeat
(
    contract_type character(255) COLLATE pg_catalog."default" NOT NULL,
    ts bigint NOT NULL,
    event character(255) COLLATE pg_catalog."default",
    heartbeat bigint,
    recovery_time bigint,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT heartbeat_id PRIMARY KEY (contract_type, ts)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.heartbeat
    OWNER to postgres;

GRANT SELECT ON TABLE public.heartbeat TO hbdm_api;

GRANT ALL ON TABLE public.heartbeat TO postgres;
-- Index: heartbeat_ca

-- DROP INDEX public.heartbeat_ca;

CREATE INDEX heartbeat_ca
    ON public.heartbeat USING btree
    (created_at ASC NULLS LAST)
    TABLESPACE pg_default;