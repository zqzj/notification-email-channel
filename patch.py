import json
import subprocess

with open('./dataloop.json') as json_file:
    data = json.load(json_file)
    current_version = data['version'].split('.')
    current_version[-1] = str(int(current_version[-1]) + 1)
    data['version'] = '.'.join(current_version)
    data['codebase']['gitTag'] = f'v{data["version"]}'
    current_version = data['codebase']['gitTag']
    print(current_version)
    
with open("./dataloop.json", "w") as jsonFile:
    json.dump(data, jsonFile, indent=2)

cmd = ['git', 'commit', '-am', current_version]
p = subprocess.Popen(cmd)
p.communicate()
cmd = ['git', 'tag', '-a', current_version, '-m', current_version]
p = subprocess.Popen(cmd)
p.communicate()