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
POST User
    [Tags]  ct02
    # Call / Action
    ${response}     GET                     ${HOST}/role
    ${role_ids}     GET VALUE FROM JSON     ${response.json()}     $.docs[:]._id
    ${body}         CREATE DICTIONARY       email=diegoquirino@gmail.com
    ...                                     password=Teste123#
    ...                                     firstName=Carlos Diego
    ...                                     lastName=Quirino Lima
    ...                                     role=${role_ids[0]}
    ...                                     _id=${ID}
    ${header}       CREATE DICTIONARY       Content-Type    application/json
    ${response}     POST On Session         ${ALIAS}        /user       json=${body}    headers=${header}

    # Validating response code
    ${status_code}          CONVERT TO STRING       ${response.status_code}
    LOG TO CONSOLE          ${status_code}
    SHOULD BE EQUAL         ${status_code}          201

    # Validating response content type
    ${content_type_value}   GET FROM DICTIONARY     ${response.headers}     Content-Type
    LOG TO CONSOLE          ${content_type_value}
    SHOULD CONTAIN          ${content_type_value}   application/json

    # Show JSON response body (converted to string)
    ${body}                 CONVERT TO STRING       ${response.json()}
    LOG TO CONSOLE          ${body}

    # Validating itens inside response JSON
    ${res_id}               GET VALUE FROM JSON     ${response.json()}     $._id
    LOG TO CONSOLE          ${res_id}
    SHOULD NOT BE EMPTY     ${res_id[0]}
    SHOULD BE EQUAL         ${res_id[0]}            ${ID}

*** Keywords ***
Setup Test Data
    Abrir a seção REST/API

Clean Test Data
    CREATE SESSION  TearDownSession     ${HOST}
    ${response}     DELETE On Session   TearDownSession       /user/${ID}
    LOG TO CONSOLE  ${response}
    Fechar a seção REST/API
