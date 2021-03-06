
list_create_tables = [

    "CREATE TABLE client \
    (\
    idclient SERIAL PRIMARY KEY,\
    name VARCHAR(45) NOT NULL,\
    surname VARCHAR(45) NOT NULL,\
    sec_name VARCHAR(45) NOT NULL,\
    passport_series INT NOT NULL,\
    passport_id INT NOT NULL\
    );",

    "CREATE TABLE company\
    (\
    idcompany SERIAL PRIMARY KEY,\
    name VARCHAR(45) NOT NULL UNIQUE\
    );",

    "CREATE TABLE agent\
    (\
    idagent SERIAL PRIMARY KEY,\
    name VARCHAR(45) NOT NULL,\
    surname VARCHAR(45) NOT NULL,\
    sec_name VARCHAR(45) NOT NULL,\
    login VARCHAR(100) NOT NULL UNIQUE,\
    password VARCHAR(1000) NOT NULL,\
    qualification VARCHAR(100) NOT NULL,\
    admin BOOLEAN NOT NULL\
    );",

    "CREATE TABLE insurance_type\
    (\
    idinsurance_type SERIAL PRIMARY KEY,\
    title VARCHAR(45) NOT NULL UNIQUE,\
    short_title VARCHAR(15) NOT NULL UNIQUE,\
    capital INT NOT NULL\
    );",

    "CREATE TABLE unit\
    (\
    idunit SERIAL PRIMARY KEY,\
    name VARCHAR(45) NOT NULL UNIQUE,\
    small_name VARCHAR(4) NOT NULL UNIQUE\
    );",

    "CREATE TABLE contract\
    (\
    idcontract SERIAL PRIMARY KEY,\
    id_client INT UNIQUE,\
    id_company INT,\
    id_unit INT,\
    id_insurance_type INT,\
    id_agent INT,\
    FOREIGN KEY (id_client) REFERENCES client (idclient),\
    FOREIGN KEY (id_company) REFERENCES company (idcompany),\
    FOREIGN KEY (id_unit) REFERENCES unit (idunit),\
    FOREIGN KEY (id_insurance_type) REFERENCES insurance_type (idinsurance_type),\
    FOREIGN KEY (id_agent) REFERENCES agent (idagent),\
    insurance_amount FLOAT NOT NULL,\
    insurance_payment FLOAT NOT NULL,\
    date_start DATE NOT NULL,\
    date_stop DATE NOT NULL\
    );",

    "CREATE TABLE payment\
    (\
    idpayment SERIAL PRIMARY KEY,\
    id_contract INT UNIQUE,\
    id_unit INT,\
    FOREIGN KEY (id_contract) REFERENCES contract (idcontract),\
    FOREIGN KEY (id_unit) REFERENCES unit (idunit),\
    date DATE NOT NULL,\
    sum FLOAT NOT NULL\
    );",

]
