*** Settings ***
Library     FTSASeleniumLibrary
Library     String
Library     OperatingSystem
#Library     SikuliLibrary   mode=NEW

Variables   ${EXECDIR}${/}resources${/}locators.py

*** Variables ***
${PERFIL}
${IMAGE_DIR}  ${EXECDIR}${/}data${/}img

*** Keywords ***
Inicializando o servidor de imagens
    #SikuliLibrary.START SIKULI PROCESS
    #SikuliLibrary.ADD IMAGE PATH    ${IMAGE_DIR}
    LOG TO CONSOLE      Inicializando servidor de Images no diretório ${IMAGE_DIR}

Abro o navegador
    OPEN BROWSER

Sou um "${nome_perfil}"
    ${nome_perfil}   CONVERT TO LOWER CASE   ${nome_perfil}
    SET SUITE VARIABLE   ${PERFIL}   ${nome_perfil}
    #SikuliLibrary.HIGHLIGHT     botao_login_novamente.png   secs=1
    #SikuliLibrary.CLICK         botao_login_novamente.png

Informo os dados de autenticação do usuário
    ${cpf}     Catenate   SEPARATOR=_   ${PERFIL}  cpf
    ${senha}   Catenate   SEPARATOR=_   ${PERFIL}  senha
    LOGIN USER  ${project.get('prop', '${cpf}')}  ${project.get('prop', '${senha}')}

Informo dados inválidos nos campos de autenticação
    [Arguments]     ${cpf}    ${senha}
    LOGIN USER      ${cpf}    ${senha}

Verifico que a autenticação foi realizada com sucesso
    PAGE SHOULD CONTAIN  Log In Successful

Verifico que a autenticação não foi realizada
    PAGE SHOULD CONTAIN  Usuário ou senha inválidos

Verifico que a o botão entrar não está habilitado
    ELEMENT SHOULD BE DISABLED   ${botao_entrar}

Fecho o navegador
    CLOSE ALL BROWSERS

Fechando o servidor de imagens
    #SikuliLibrary.STOP REMOTE SERVER
    LOG TO CONSOLE    Finalizando servidor de Images no diretório ${IMAGE_DIR}