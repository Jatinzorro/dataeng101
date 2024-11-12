-- This script creates star schema architecture for Sales Table with some dimension tables


CREATE TABLE IF NOT EXISTS public."softcartDimDate"
(
    dateid integer NOT NULL,
    year bigint,
    month integer,
    monthname character varying,
    day integer,
    weekday integer,
    weekdayname character varying,
    date date,
    PRIMARY KEY (dateid)
);

CREATE TABLE IF NOT EXISTS public."softcartDimCategory"
(
    catagoryid integer NOT NULL,
    catagory character varying NOT NULL,
    PRIMARY KEY (catagoryid)
);

CREATE TABLE IF NOT EXISTS public."softcartDimItem"
(
    itemid interval NOT NULL,
    item character varying,
    PRIMARY KEY (itemid)
);

CREATE TABLE IF NOT EXISTS public."softcartDimCountry"
(
    countryid integer NOT NULL,
    country character varying,
    PRIMARY KEY (countryid)
);

CREATE TABLE IF NOT EXISTS public."softcartFactSales"
(
    orderid integer,
    dateid integer,
    categoryid integer,
    countryid integer,
    itemid bigint,
    amount double precision,
    PRIMARY KEY (orderid)
);

ALTER TABLE IF EXISTS public."softcartFactSales"
    ADD CONSTRAINT date FOREIGN KEY (dateid)
    REFERENCES public."softcartDimDate" (dateid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."softcartFactSales"
    ADD CONSTRAINT categoryid FOREIGN KEY (categoryid)
    REFERENCES public."softcartDimCategory" (catagoryid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."softcartFactSales"
    ADD CONSTRAINT countryid FOREIGN KEY (countryid)
    REFERENCES public."softcartDimCountry" (countryid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."softcartFactSales"
    ADD CONSTRAINT itemid FOREIGN KEY (itemid)
    REFERENCES public."softcartDimItem" (itemid) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;