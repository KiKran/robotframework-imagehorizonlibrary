*** Settings ***
Library     ScreenCapLibrary
Library     Process
Library     ${CURDIR}\\..\\src\\ImageHorizonLibrary    reference_folder=${CURDIR}\\ref_images    keyword_on_failure=Take New Screenshot    confidence=.99    timeout=${1*${mult}}


*** Variables ***
${mult}     0.5


*** Test Cases ***
Default Timeout
    Run Keyword And Ignore Error    Wait For    reference_image=equals
    Run Keyword And Ignore Error    Wait For    reference_image=equals    timeout=.5
    Run Keyword And Ignore Error    Wait For And Click Image    reference_image=equals    timeout=.5

Set Default Timeout
    Set Timeout    new_timeout=0.5
    Run Keyword And Ignore Error    Wait For    reference_image=equals
    Run Keyword And Ignore Error    Wait For    reference_image=equals    timeout=.2


*** Keywords ***
Take New Screenshot
    ScreenCapLibrary.Take Screenshot    save_to_disk=False    monitor=1
