import shutil
import json
import os
 
with open('./dataloop.json') as json_file:
    data = json.load(json_file)
    panel_name = data['components']['panels'][0]['name']

index_path = f'./panels/{panel_name}/index.html'
lines = []
with open(index_path, 'r') as html_file:
    for line in html_file.readlines():
        if "/assets/" in line:
            line = line.replace('/assets/', f'../{panel_name}/assets/')
        lines.append(line)

with open(f'./panels/{panel_name}/index.html', 'w') as updated_html_file:
    updated_html_file.writelines(lines)
