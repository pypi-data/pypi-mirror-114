*** Settings ***
Library     FTSASeleniumLibrary
Library     String
Library     OperatingSystem
Library     Collections

Variables   ${EXEC_DIR}${/}resources${/}locators.py

*** Variables ***
${HOST}             ${EMPTY}
${PORT}             ${EMPTY}
${NETWORK_NAME}     ${EMPTY}
${SELENIUM_NAME}    ${EMPTY}
${PERFIL}           ${EMPTY}

*** Keywords ***
Inicializo o servidor remoto
    ${server}               INIT REMOTE SERVER
    ${HOST} =               GET FROM DICTIONARY    ${server}    host
    SET SUITE VARIABLE      ${HOST}
    ${PORT} =               GET FROM DICTIONARY    ${server}    port
    SET SUITE VARIABLE      ${PORT}
    ${NETWORK_NAME} =       GET FROM DICTIONARY    ${server}    network_name
    SET SUITE VARIABLE      ${NETWORK_NAME}
    ${SELENIUM_NAME} =      GET FROM DICTIONARY    ${server}    selenium_name
    SET SUITE VARIABLE      ${SELENIUM_NAME}
    LOG TO CONSOLE          '${SELENIUM_NAME}' execution container initialized at http://${HOST}:${PORT}/wd/hub inside '${NETWORK_NAME}' network.

Finalizo o servidor remoto
    END REMOTE SERVER
    LOG TO CONSOLE          Synchronizing execution data...

Abro o navegador
    INIT RECORD TEST VIDEO  test_name=${TEST NAME}
    LOG TO CONSOLE          Recording test case "${TEST NAME}".
    OPEN BROWSER            remote_url=http://${HOST}:${PORT}/wd/hub

Fecho o navegador
    CLOSE ALL BROWSERS
    END RECORD TEST VIDEO

Sou um "${nome_perfil}"
    ${nome_perfil}          CONVERT TO LOWER CASE   ${nome_perfil}
    SET SUITE VARIABLE      ${PERFIL}               ${nome_perfil}

Informo os dados de autenticação do usuário
    ${cpf}     Catenate   SEPARATOR=_   ${PERFIL}  cpf
    ${senha}   Catenate   SEPARATOR=_   ${PERFIL}  senha
    LOGIN USER  ${project.get('prop', '${cpf}')}  ${project.get('prop', '${senha}')}

Informo dados inválidos nos campos de autenticação
    [Arguments]    ${cpf}    ${senha}
    LOGIN USER     ${cpf}    ${senha}

Verifico que a autenticação foi realizada com sucesso
    PAGE SHOULD CONTAIN  Log In Successful

Verifico que a autenticação não foi realizada
    PAGE SHOULD CONTAIN  Usuário ou senha inválidos

Verifico que a o botão entrar não está habilitado
    ELEMENT SHOULD BE DISABLED   ${botao_entrar}
