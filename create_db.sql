--
-- Name: Donors; Type: TABLE;
--

DROP TABLE IF EXISTS Donors;

CREATE TABLE Donors(
   donor_id INT PRIMARY KEY     NOT NULL,
   name           VARCHAR(50)   NOT NULL,
   blood_type     VARCHAR(50)   NOT NULL,
   blood_id       INT           NOT NULL,
   contact_info   VARCHAR(50)
);

--
-- Name: Drives; Type: TABLE;
--

DROP TABLE IF EXISTS Drives;

CREATE TABLE Drives(
   drive_id INT PRIMARY KEY     NOT NULL,
   name         VARCHAR(50)     NOT NULL,
   location     VARCHAR(50)     NOT NULL,
   date         DATE            NOT NULL
);

--
-- Name: Labs; Type: TABLE;
--

DROP TABLE IF EXISTS Labs;

CREATE TABLE Labs(
   lab_id INT PRIMARY KEY     NOT NULL,
   name         VARCHAR(50)    NOT NULL,
   location     VARCHAR(50)   NOT NULL,
   tests_passed BOOLEAN       NOT NULL
);

--
-- Name: Hospitals; Type: TABLE;
--

DROP TABLE IF EXISTS Hospitals;

CREATE TABLE Hospitals(
   hospital_id INT PRIMARY KEY     NOT NULL,
   name         VARCHAR(50)    NOT NULL,
   location     VARCHAR(50)   NOT NULL
);

--
-- Name: Banks; Type: TABLE;
--

DROP TABLE IF EXISTS Banks;

CREATE TABLE Banks(
   bank_id INT PRIMARY KEY     NOT NULL,
   name         VARCHAR(50)    NOT NULL,
   location     VARCHAR(50)   NOT NULL
);

--
-- Name: Recipients; Type: TABLE;
--

DROP TABLE IF EXISTS Recipients;

CREATE TABLE Recipients(
   recipient_id INT PRIMARY KEY     NOT NULL,
   name           VARCHAR(50)   NOT NULL,
   recipient_blood_type     VARCHAR(50)   NOT NULL,
   contact_info   VARCHAR(50)
);

--
-- Name: donate; Type: TABLE;
--

DROP TABLE IF EXISTS donate;

CREATE TABLE donate(
  donation_id INT PRIMARY KEY     NOT NULL,
  donor_id    INT                 NOT NULL,
  blood_id    INT                 NOT NULL,
  drive_id    INT                 NOT NULL,
  FOREIGN KEY(donor_id) REFERENCES Donors(donor_id),
  FOREIGN KEY(drive_id) REFERENCES Drives(drive_id)
);

--
-- Name: test; Type: TABLE;
--

DROP TABLE IF EXISTS test;

CREATE TABLE test(
  test_id     INT PRIMARY KEY     NOT NULL,
  drive_id    INT                 NOT NULL,
  lab_id      INT                 NOT NULL,
  blood_id    INT                 NOT NULL,
  FOREIGN KEY(lab_id) REFERENCES Labs(lab_id),
  FOREIGN KEY(drive_id) REFERENCES Drives(drive_id)
);


--
-- Name: store; Type: TABLE;
--

DROP TABLE IF EXISTS store;

CREATE TABLE store(
  storage_id  INT PRIMARY KEY     NOT NULL,
  bank_id     INT                 NOT NULL,
  lab_id      INT                 NOT NULL,
  blood_id    INT                 NOT NULL,
  FOREIGN KEY(lab_id) REFERENCES Labs(lab_id),
  FOREIGN KEY(bank_id) REFERENCES Banks(bank_id)
);

--
-- Name: distribute; Type: TABLE;
--

DROP TABLE IF EXISTS distribute;

CREATE TABLE distribute(
  distribution_id  INT PRIMARY KEY     NOT NULL,
  bank_id     INT                 NOT NULL,
  hospital_id INT                 NOT NULL,
  blood_id    INT                 NOT NULL,
  FOREIGN KEY(hospital_id) REFERENCES Hospitals(hospital_id),
  FOREIGN KEY(bank_id) REFERENCES Banks(bank_id)
);


--
-- Name: transfusion; Type: TABLE;
--

DROP TABLE IF EXISTS transfusion;

CREATE TABLE transfusion(
  distribution_id  INT PRIMARY KEY     NOT NULL,
  recipient_id     INT                 NOT NULL,
  hospital_id INT                 NOT NULL,
  blood_id    INT                 NOT NULL,
  FOREIGN KEY(hospital_id) REFERENCES Hospitals(hospital_id),
  FOREIGN KEY(recipient_id) REFERENCES Recipients(recipient_id)
);
