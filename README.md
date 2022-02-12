# dapy_p12_epic_events

## Quality Assurance Branch

Coverage feature added.

## Installation

In a Command Line Interface:

| Comment                                    | Folder                | Instruction                                                             |
|--------------------------------------------|-----------------------|-------------------------------------------------------------------------|
| install the dependencies                   | root                  | ```pip install -r requirements.txt```                                   |

It will install coverage.py

## Test the coverage

| Comment                                           | Folder                       | Instruction                                          |
|---------------------------------------------------|------------------------------|------------------------------------------------------|
| first instruction                                 | folder containing manage.py  | ``` coverage run --source='.' manage.py test  ```    |
| checks the coverage, will show a table in the CLI | folder containing manage.py  | ``` coverage report ```                              |
