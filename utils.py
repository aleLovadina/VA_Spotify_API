#Imports
import json

### convert_path_to_JSON(path, ['password', 'username', 'api_key'])

def get_json_variables(path, var_name):
    with open(path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        json_file.close()
    if type(var_name) is list:
        return_data = {}
        for key in var_name:
            return_data[key] = data[key]
        return return_data
    else:            
        return {var_name: data[var_name]}
# path= os.path.abspath()
# print(os.path.join(path,"configurationState.JSON"))