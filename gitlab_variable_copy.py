import requests
import os
from dotenv import load_dotenv

load_dotenv()

gitlab_api_url= os.environ["gitlab_api_url"]
api_url_T = os.environ["api_url_T"]
user_id = os.environ["user_id"]

while(True):   
    project_id = input("\nEnter the ON-PREM Project ID (or 'exit' to quit) :")         
    if project_id == 'exit':
        print('\nThank you for copying variables from ON-PREM to SaaS cloud.')
        break
    else:   
        gitlab_api_url = os.environ.get('gitlab_api_url')
        private_token_S = input("Enter the ON-PREM Private Token :")    
        api_url_T = os.environ.get('api_url_T')
        project_id_T = input("\nEnter the SaaS Cloud Project ID :")           
        private_token_T = input("Enter the SaaS Cloud Private Token :") 
        
        # Masked sensitive information with stars.
        def mask_sensitive_info(info):
            return '*' * len(info)
        masked_source_token = mask_sensitive_info(private_token_S)
        masked_dest_token = mask_sensitive_info(private_token_T)

        # Copy variables from  ON-PREM Gitlab.
        def get_gitlab_variables(gitlab_api_url, project_id, private_token_S):
            headers = {'PRIVATE-TOKEN': private_token_S} 
            response = requests.get(f'{gitlab_api_url}/projects/{project_id}/variables', headers=headers)   
            if response.status_code == 200:
                return response.json()            
        source_variables = get_gitlab_variables(gitlab_api_url, project_id, private_token_S)

        destination_variables = []
        for variable in source_variables:
            destination_variable = variable.copy()  
            destination_variable['protected'] = variable.get('protected', False)  
            destination_variable['masked'] = variable.get('masked', False)  
            destination_variables.append(destination_variable)

        # Create variables on Gitlab SaaS Cloud.
        def create_gitlab_variable(api_url_T, project_id_T, private_token_T, key, value, protected=False, masked=False, variable_type='variable'):
            headers = { 'PRIVATE-TOKEN': private_token_T ,'Content-Type': 'application/x-www-form-urlencoded'}
            data = {'key': key,'value': value,'variable_type': variable_type, 'protected': protected, 'masked': masked}
            response = requests.post(f'{api_url_T}/projects/{project_id_T}/variables', headers=headers, data=data, verify='C:\\Users\\blsrlyn\\ca-bundle.crt')
        variables_to_post = get_gitlab_variables(gitlab_api_url, project_id, private_token_S)       
        
        if variables_to_post:
            variables_to_post.extend(destination_variables)
            for variable in variables_to_post:
                create_gitlab_variable(
                    api_url_T,
                    project_id_T,
                    private_token_T,
                    variable['key'],
                    variable['value'],
                    variable.get('protected', False),  
                    variable.get('masked', False),    
                    variable_type=variable.get('variable_type', 'variable')
                    )            