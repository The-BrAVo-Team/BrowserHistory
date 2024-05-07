# DEVELOPMENT PROCEDURES #

- ### Starting programming: ###
    - You should start by Initializing your venv and setting it to use the venv
    - The commands to do this are as follows:
        - python -m venv venv
        - Windows: source venv/Sripts/activate
        - Mac/Linux: source venv/bin/activate
        - pip install -r requirements.txt

- ### Add any dependencies to requirements.txt ###
    - Do this by running 'pip freeze -r requirements.txt -l' and it will automatically dump the dependencies present in the VENV

- ### Store Secrets in .env file ###
    - This should be self explanatory

- ### Work in a branch ###
    - Do this to avoid any future issues and merge conflicts.