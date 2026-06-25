*** Settings ***
Library     ScreenCapLibrary
Library     Process
Library    OperatingSystem
Library     ${CURDIR}\\..\\src\\ImageHorizonLibrary    reference_folder=${CURDIR}\\..\\results    keyword_on_failure=Take New Screenshot    confidence=.99


*** Variables ***
${test_location_1}      (515, 155)
${test_width_1}         200
${test_height_1}        30
${test_location_2}      (515, 155)


*** Test Cases ***
OCR from Screenshot Test
    Delete Last Screenshot
    ${path}    ScreenCapLibrary.Take Screenshot    name=testing_screenshot    monitor=1
    Get Text From Image    testing_screenshot_1    confidence=5    lang='eng'


*** Keywords ***
Take New Screenshot
    ScreenCapLibrary.Take Screenshot    save_to_disk=False    monitor=1

Delete Last Screenshot
    Remove File    ${CURDIR}${/}..${/}results${/}testing_screenshot_*.png

Stop Calc
    Run Process    taskkill /F /IM CalculatorApp.exe    shell=True    # robotcode: ignore
