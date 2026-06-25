*** Settings ***
Library     ScreenCapLibrary
Library     Process
Library     ${CURDIR}\\..\\src\\ImageHorizonLibrary    reference_folder=${CURDIR}\\ref_images    keyword_on_failure=Take New Screenshot    confidence=.99


*** Test Cases ***
Click An Aktueller Location
    Click With Offset    5    -10
    Click With Offset    0    15    button=right
    Click With Offset    0    15    button=left    clicks=2
    Run Keyword And Ignore Error    Click With Offset    0    15    button=right    interval=2.1

Click mit Location
    Click With Offset From Location    (600, 600)    10    20.5
    Click With Offset From Location    (600, 600)    10    20    clicks=3    button=right
    Click With Offset From Location    (600, 600)    10    20    clicks=2    interval=1
    Run Keyword And Ignore Error    Click With Offset From Location    600    600    10    20

Click mit Image Offset
    [Setup]    Launch Application    C:/Windows/System32/calc.exe
    Click With Offset From Image    reference_image=number_1    x_offset=0    y_offset=-10    timeout=5
    Click With Offset From Image    reference_image=number_1    x_offset=300    y_offset=-10    # click plus button
    Click With Offset From Image    reference_image=number_1    x_offset=100    y_offset=10    clicks=2    interval=1
    Click With Offset From Image    reference_image=equals    x_offset=-10    y_offset=0    clicks=3
    Does Exist    reference_image=result
    [Teardown]    Stop Calc

Click Location Test and Does Not Exist
    # getestet wie sonst auch in wait and click image
    [Setup]    Launch Application    C:/Windows/System32/calc.exe
    ${location}    Wait For    reference_image=number_1
    Click Location    location=${location}
    Does Not Exist    reference_image=equals
    [Teardown]    Stop Calc

Wait For Tests Und Scrollen
    [Setup]    Launch Application    C:/Windows/System32/calc.exe
    Wait For And Click Image    reference_image=equals
    Scroll Window
    [Teardown]    Stop Calc


*** Keywords ***
Take New Screenshot
    ScreenCapLibrary.Take Screenshot    save_to_disk=False    monitor=1

Stop Calc
    Run Process    taskkill /F /IM CalculatorApp.exe    shell=True    # robotcode: ignore
