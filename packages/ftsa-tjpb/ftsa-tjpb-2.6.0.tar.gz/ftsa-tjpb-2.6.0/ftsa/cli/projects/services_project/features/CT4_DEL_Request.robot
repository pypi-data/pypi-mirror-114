*** Settings ***
Library         FTSARequestsLibrary
Library         JSONLibrary
Library         Collections

Resource        ${EXEC_DIR}${/}page_objects${/}OpenCloseSessionPage.robot

Test Setup      Setup Test Data
Test Teardown   Clean Test Data

Variables       ${EXEC_DIR}${/}resources${/}locators.py

*** Variables ***
${HOST}         ${project.get('prop','API_HOST')}
${ALIAS}        ${project.get('prop','API_ALIAS')}
${ID}           000000007cc459533cc6aeea
# ID from       ./resources/objectId.html

*** Test Cases ***
DEL User
    [Tags]  ct04
    # Call / Action
    ${response}     DELETE On Session    ${ALIAS}       /user/${ID}

    # Validating response code
    ${status_code}          CONVERT TO STRING       ${response.status_code}
    LOG TO CONSOLE          ${status_code}
    SHOULD BE EQUAL         ${status_code}          204

    # Validating response content is empty
    ${body}                 CONVERT TO STRING       ${response.content}
    LOG TO CONSOLE          ${body}
    SHOULD BE EMPTY         ${body}

*** Keywords ***
Setup Test Data
   ${response}     GET                     ${HOST}/role
    ${role_ids}     GET VALUE FROM JSON     ${response.json()}     $.docs[:]._id
    ${body}         CREATE DICTIONARY       email=diegoquirino@gmail.com
    ...                                     password=Teste123#
    ...                                     firstName=Carlos Diego
    ...                                     lastName=Quirino Lima
    ...                                     role=${role_ids[0]}
    ...                                     _id=${ID}
    ${header}       CREATE DICTIONARY       Content-Type    application/json
    CREATE SESSION  SetupSession            ${HOST}
    ${response}     POST On Session         SetupSession    /user       json=${body}    headers=${header}
    LOG TO CONSOLE  ${response}
    Abrir a seção REST/API

Clean Test Data
    Fechar a seção REST/API
