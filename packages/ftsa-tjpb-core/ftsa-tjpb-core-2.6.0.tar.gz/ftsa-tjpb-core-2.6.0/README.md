# FTSA-TJPB-CORE


## Introduction

_CORE Libraries_ from **FTSA (_Framework_ de Testes de Sistema Automatizados - TJPB)** provides keywords extents to be used within [Robot Framework's](https://robotframework.org/) environment to test UI (web and mobile), Rest/Services/SSH and Databases, to supply tests context in TJPB.

This library supports python 3.8+ AND Docker Engine 20+

## Keyword Documentation

Here is a list of the available keywords:

- [Mobile **FTSAAppiumLibrary** keywords](docs/FTSAAppiumLibrary.html)
- [Web **FTSASeleniumLibrary** keywords](docs/FTSASeleniumLibrary.html)
- [Services and REST **FTSARequestsLibrary** keywords](docs/FTSARequestsLibrary.html)
- [SSH **FTSASSHLibrary** keywords](docs/FTSASSHLibrary.html)
- [Database **FTSADatabaseLibrary** keywords](docs/FTSADatabaseLibrary.html)
- Template Files **FTSAFilesLibrary** (not implemented)

## Getting Started

### Step 1: Install FTSA-TJPB command client

Make sure you have installed [FTSA-TJPB command client](http://gitlab-novo.tjpb.jus.br/testes/ftsa/cli) through a console/terminal:

```
pip install -y ftsa-tjpb
```

### Step 2: Install FTSA-TJPB-CORE libraries

To install FTSA-TJPB-CORE libraries, perform in your console/terminal the following command:

```
ftsa install
```

### Step 3: Initialize a project from template

To use a template that will enable project with architectural FTSA patterns pre-definitions, use `init` command:

```
ftsa init <project_name> 
```

- ***Obs:*** if you are working with Rest/API/Services test project, use `ftsa init <project_name> -s` (or `--services` option)

## Writing Tests

Once you have installed FTSA-TJPB-CORE libraries, into the **Settings section** from any *.robot* script you can import any of Libraries to test UI (web and mobile), Rest/Services/SSH and Databases with keyword available.

```robot
*** Settings ***
Documentation   TJPB Core Example

Library     FTSASeleniumLibrary
Library     FTSAAppiumLibrary
Library     FTSARequestsLibrary
Library     FTSASSHLibrary
Library     FTSADatabaseLibrary

*** Variables ***
# Implement your variables 

*** Test Cases ***
# Implement your test cases 
Test that something happens when an action is performed
    Given I have some precondition
    When I perform some action
    Then A determined result is expected
    
*** Keywords ***
I have some precondition
    # Call any of keywords available from the documentation of the imported libraries
    
I perform some action
    # Call any of keywords available from the documentation of the imported libraries
    
A determined result is expected
    # Call any of keywords available from the documentation of the imported libraries
    
```

***Obs:*** for simplicity, *keywords* are shown into the same *feature* file, in the example above. You must implement *keywords* ONLY into `page_object` package, like required for the FTSA architetural patterns and structure (see an example by running `ftsa init <project_name>`).

## Contact and support

*Carlos Diego Quirino Lima*
- **Email:** diego.quirino@tjpb.jus.br

*Felipe Dias*
- **Email:** felipe.dias@tjpb.jus.br

*Rogerio Trevian Nibon*
- **Email:** rogerio.nibon@tjpb.jus.br