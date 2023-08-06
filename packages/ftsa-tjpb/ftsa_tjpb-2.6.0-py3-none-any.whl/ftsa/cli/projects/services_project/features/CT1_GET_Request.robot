*** Settings ***
Library         FTSARequestsLibrary
Library         JSONLibrary
Library         Collections

Resource        ${EXEC_DIR}${/}page_objects${/}OpenCloseSessionPage.robot

Test Setup      Abrir a seção REST/API
Test Teardown   Fechar a seção REST/API

Variables       ${EXEC_DIR}${/}resources${/}locators.py

*** Variables ***
${HOST}         ${project.get('prop','API_HOST')}
${ALIAS}        ${project.get('prop','API_ALIAS')}
${ID}           ${empty}

*** Test Cases ***
GET Users
    [Tags]  ct01
    # Call / Action
    ${response}             GET On Session          ${ALIAS}   /user

    # Validating response code
    ${status_code}          CONVERT TO STRING       ${response.status_code}
    LOG TO CONSOLE          ${status_code}
    SHOULD BE EQUAL         ${status_code}          200

    # Validating response content type
    ${content_type_value}   GET FROM DICTIONARY     ${response.headers}     Content-Type
    LOG TO CONSOLE          ${content_type_value}
    SHOULD CONTAIN          ${content_type_value}   application/json

    # Show JSON response body (converted to string)
    ${body}                 CONVERT TO STRING       ${response.json()}
    LOG TO CONSOLE          ${body}

    # Multiple data validation
    ${res_emails}           GET VALUE FROM JSON     ${response.json()}     $.docs[:].email
    LOG TO CONSOLE          ${res_emails}
    SHOULD CONTAIN ANY      ${res_emails[0]}        test@account.com  test@admin.com  test@superadmin.com

    ${res_ids}              GET VALUE FROM JSON     ${response.json()}     $.docs[:]._id
    LOG TO CONSOLE          ${res_ids}
    SHOULD NOT BE EMPTY     ${res_ids[0]}
    ${ID} =                 SET VARIABLE            ${res_ids[0]}
    SET SUITE VARIABLE      ${ID}

GET User (${ID})
    [Tags]  ct01
    # Call / Action
    ${response}             GET On Session          ${ALIAS}   /user/${ID}

    # Validating response code
    ${status_code}          CONVERT TO STRING       ${response.status_code}
    LOG TO CONSOLE          ${status_code}
    SHOULD BE EQUAL         ${status_code}          200

    # Validating response content type
    ${content_type_value}   GET FROM DICTIONARY     ${response.headers}     Content-Type
    LOG TO CONSOLE          ${content_type_value}
    SHOULD CONTAIN          ${content_type_value}   application/json

    # Show JSON response body (converted to string)
    ${body}                 CONVERT TO STRING       ${response.json()}
    LOG TO CONSOLE          ${body}

    # Unique data validation
    ${test_id}              GET VALUE FROM JSON     ${response.json()}    $.._id
    LOG TO CONSOLE          ${test_id}
    SHOULD BE EQUAL AS STRINGS    ${test_id[0]}     ${ID}


