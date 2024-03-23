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
    - enter your desired parameters

## Let's look at the resources created
1. Navigate to your newly created 'create_db_tables' lambda function and run it to create the tables in your database
2. Navigate to your api gateway to test your newly created APIs

## Notes
- Hopefully you can use this as a basis to create your own serverless app with rds backend
- Build out your API, add security features etc. to interface with the front end of your app.