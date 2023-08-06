*** Settings ***
Library     FTSARequestsLibrary

Variables       ${EXEC_DIR}${/}resources${/}locators.py

*** Keywords ***
Abrir a seção REST/API
    CREATE SESSION      url=${project.get('prop','API_HOST')}       alias=${project.get('prop','API_ALIAS')}

Fechar a seção REST/API
    DELETE ALL SESSIONS