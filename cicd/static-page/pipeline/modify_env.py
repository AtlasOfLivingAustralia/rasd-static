import yaml
import sys
import os

if __name__ == '__main__':
    args = sys.argv

    if len(args) != 2:
        print('Usage: python modify_env.py <env>')
        sys.exit(1)

    with open(args[1], 'r') as file:
        env = yaml.safe_load(file)
        print(env)
    hosted_zone = os.getenv('HOSTED_ZONE')
    sub_domain = os.getenv('SUB_DOMAIN')

    url = f"{sub_domain}.{hosted_zone}"
    html_url = f"https://{url}"
    env['book']['navbar']['href'] = html_url
    env['book']['page-footer']['center'][0]['text'] = url
    env['book']['page-footer']['center'][0]['href'] = html_url
    # branch_name = env['pCleanBranch']


    with open(args[1], 'w') as file:
        yaml.dump(env, file, sort_keys=False)