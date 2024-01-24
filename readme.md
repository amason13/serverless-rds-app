# Sample Serverless Python Project

## Project Setup
In the terminal:
1. Clone the repository.
    - git clone https://github.com/amason13/serverless_rds_app.git
2. navigate to the project
3. create a python virtual environment and set it to default for project
    - pyenv virtualenv my_env_name
    - pyenv local my_env_name
4. Installing requirements
    - pip install -e .
5. Optional - add kernel to jupter notebook
	- ipython kernel install --name "my_env_name" --user

## SAM Setup
In the terminal:
1. Navigate to project folder
2. Build sam app
    - sam build
3. Deploy the app
    - sam deploy --guided
