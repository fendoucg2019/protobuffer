import yaml
def get_yaml_data(key):
    with open('../config/values.yaml', 'r') as f:
        data = yaml.safe_load(f)
    return data.get(key)

socket_data = get_yaml_data('socketinfo')
user_data = get_yaml_data('User')

# print('Socket IP:', socket_data['ip'])
# print('User strid:', user_data['strid'])