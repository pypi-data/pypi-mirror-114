# Import test tool
Import test cases from .xlsx file

## Installation
* `$ pip install teko-import-test`

## Precondition
* Python >= 3.7.1, < 4.0

* File to import is .xlsx

* File must has the column with cell at first row is "NAME".
This tool will take test case's names from that column to import

* Optional: If you want to add objective and precondition for the test case, just add 2 columns "OBJECTIVE" and "PRECONDITION"

* You must set environment variables before import. Example in `.\set_env.bat`

    * FILE_GENERATED - path to the file to be generated
    
    * FILE_IMPORT - path to the file to import
    
    * CLASS_TEMPLATE - template of the class test.
    Template of class must be .txt and contains "$body$". Example in `.\template\class_template.txt`
    
    * TEST_CASE_TEMPLATE -  template of the each test case. 
    Template of class must be .txt and contains "$test_case_name$" and ""$test_number$".
    $test_case_objective$ and $test_case_precondition$ is optional
    Example in `.\template\test_case_template.txt`

## Import
* `$ teko-import-test`
