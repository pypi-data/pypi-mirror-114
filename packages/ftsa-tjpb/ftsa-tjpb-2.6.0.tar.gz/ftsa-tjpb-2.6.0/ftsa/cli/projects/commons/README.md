# {NOME_DO_PROJETO}

## Introduction

This test project based on [FTSA-TJPB _Framework_](http://gitlab-novo.tjpb.jus.br/testes/ftsa) minimizes automation efforts by providing _useful keywords_ and _libraries_ as an extension of pre-delivered [RobotFramework](https://robotframework.org/).

**This project supports _FTSA 2.5.1_, WITH python 3.8+ and Docker Engine 20+**

## Keyword Documentation

Here is a list of the available keywords:

- [Mobile **FTSAAppiumLibrary** keywords](http://gitlab-novo.tjpb.jus.br/testes/ftsa/core/tree/master/docs/FTSAAppiumLibrary.html)
- [Web **FTSASeleniumLibrary** keywords](http://gitlab-novo.tjpb.jus.br/testes/ftsa/core/tree/master/docs/FTSASeleniumLibrary.html)
- [Services and REST **FTSARequestsLibrary** keywords](http://gitlab-novo.tjpb.jus.br/testes/ftsa/core/tree/master/docs/FTSARequestsLibrary.html)
- [SSH **FTSASSHLibrary** keywords](http://gitlab-novo.tjpb.jus.br/testes/ftsa/core/tree/master/docs/FTSASSHLibrary.html)
- [Database **FTSADatabaseLibrary** keywords](http://gitlab-novo.tjpb.jus.br/testes/ftsa/core/tree/master/docs/FTSADatabaseLibrary.html)
- Template Files **FTSAFilesLibrary** (not implemented)

## Getting Started

### Implement your own scripts

FTSA project structured into 3 main packages:

- **data**: here you make available all mass of data (files *.csv, *.xml, *.txt, *.sql, etc.) that will provide to your test cases the values to be used in tests (usually for covering purposes).
- **features**: here you will provide _BDD (given, when, then) like sentences_ that provides pre-conditions, steps and assertions for your test cases. For example:
- **page_objects**: here you will implement with _robot framework or FTSA keywords_ the sentences you made into BDD features.
  - Use [locators.py](resources/locators.py) file to avoid repeating _xpath, id or css_ locators names and values throughout the page objects.
  - Use [project.properties](resources/project.properties) file to general and configuration project properties (like URLs, test username and passwords, endpoints, etc.).

Obs: This project provides files exemplifying basic implementation content into each mentioned packages.

## Run

Once you have implemented your test cases, execute then. You can choose between:

### Local Run Test

1. Your host machine must be able and configured with _FTSA 2.5.1_, WITH python 3.8+ and Docker Engine 20+. In case you are using database mass of data (or either need to apply database changes during your scripts), you must configure Oracle 11+, MySQL 8+ or PostgreSQL 10+ clients in order to run correctly tests. Bellow you can see a linux Fedora dist list of command that enable configuration you need (execute in presented order):

```
dnf upgrade -y && dnf update -y
dnf install -y python39 pip docker wget
dnf module install -y nodejs:12
dnf install -y libpq-devel
wget https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python3-8.0.25-1.fc34.x86_64.rpm
dnf localinstall -y mysql-connector-python3-8.0.25-1.fc34.x86_64.rpm
wget https://dev.mysql.com/get/Downloads/Connector-ODBC/8.0/mysql-connector-odbc-8.0.25-1.fc34.x86_64.rpm
dnf localinstall -y mysql-connector-odbc-8.0.25-1.fc34.x86_64.rpm
wget https://dev.mysql.com/get/Downloads/Connector-ODBC/8.0/mysql-connector-odbc-setup-8.0.25-1.fc34.x86_64.rpm
dnf localinstall -y mysql-connector-odbc-setup-8.0.25-1.fc34.x86_64.rpm
dnf install -y libaio libnsl
wget https://download.oracle.com/otn_software/linux/instantclient/19600/oracle-instantclient19.6-basic-19.6.0.0.0-1.x86_64.rpm
dnf localinstall -y oracle-instantclient19.6-basic-19.6.0.0.0-1.x86_64.rpm
pip install docker setuptools wheel twine
```

2. Run local command to perform tests:

```
ftsa report --nodocker -i <tagname> -e <tagname>
```

- ***Obs:*** -i (--includes) and -e (--excludes) tag parameters are optionals. If you don't include them, all test cases defined will be executed.
- ***For non-linux hosts, remember to satisfy pre-required python, docker and database (Oracle, MySQL or PostgreSQL clients) installations to your system and versions.***

### Docker External Test

#### Dockerfile approach

To execute this project using [Dockerfile](Dockerfile) released within, perform the single command:

```
ftsa docker-report -i <tagname> -e <tagname>
```

- ***Obs:*** -i (--includes) and -e (--excludes) tag parameters are optionals. If you don't include them, all test cases defined will be executed.

#### FTSA Image approach

To execute this project using pre-compilled [FTSA Docker Image](https://hub.docker.com/repository/docker/testetjpb/ftsa-tjpb-image), choose the version 2.5.1 and perform this single command:

```
ftsa docker-report --pull -i <tagname> -e <tagname>
```

- ***Obs:*** -i (--includes) and -e (--excludes) tag parameters are optionals. If you don't include them, all test cases defined will be executed.

## Example Services Project

To execute Services Project example, you need to make up and running [Rest-Hapi Project](https://resthapi.com/docs/quick-start.html). 

***PAY ATTENTION FOR THE FOLLOWING PRE-REQUIREMENTS (TO RUN EXAMPLE PROJECT):***

- You need [Node.js ^12.14.1 installed](https://nodejs.org/en/), and;
- You'll need [MongoDB installed and running](https://docs.mongodb.com/manual/installation/).

In this way, server will be initialized in `http://localhost:8080` and you can start a new services project `ftsa init <project name> -s` and run `ftsa report --nodocker` to see the results locally.

## Contact and support

*Carlos Diego Quirino Lima*
- **Email:** diego.quirino@tjpb.jus.br

*Felipe Dias*
- **Email:** felipe.dias@tjpb.jus.br

*Rogerio Trevian Nibon*
- **Email:** rogerio.nibon@tjpb.jus.br
