import json
import os
import shutil
import subprocess

defaultData = {
    "BuildNumber": 0,
    "JSONVersion": 3,
    "AngularProjectFolder": "PlayTimeClient",
    "BuildDataPath": "/src/app/Models/buildData.ts",
    "AngularDistName": "play-time",
    "HostToUrl": "https://oldmartijntje.nl",
    "BuilderMakeBranch": False,
    "MainBranch": "main"
}

exitMessage = "Press Enter key to exit..."
current_working_directory = os.getcwd()

splitted = current_working_directory.split('\\')

def create_or_read_builder_data():
    filename = "scripts/BuilderData.json"

    if os.path.isfile(filename):
        # If the file exists, read the JSON data from it
        with open(filename, 'r') as file:
            builder_data = json.load(file)
            # Increment the 'buildNumber' field by 1
            builder_data["BuildNumber"] += 1
    else:
        # If the file doesn't exist, initialize it with default data
        builder_data = defaultData

    with open(filename, 'w') as file:
        json.dump(builder_data, file, indent=4)

    return builder_data

builder_data = create_or_read_builder_data()

while os.path.isdir("PlayTimeClient") == False and len(splitted) > 2:
    os.chdir("..")
    current_working_directory = os.getcwd()

    splitted = current_working_directory.split('\\')

if (len(splitted) == 2 and splitted[1] == ''):
    print("ERROR: PlayTimeClient folder not found")
    input(exitMessage)
    exit()

try:

    # Change the current working directory to the PlayTimeClient folder
    os.chdir('PlayTimeClient')

    npm_build_command = 'npm install'
    subprocess.run(npm_build_command, shell=True, check=True)

    # Build the Angular project
    ng_build_command = 'ng build --configuration "production" --base-href "https://oldmartijntje.nl"'
    subprocess.run(ng_build_command, shell=True, check=True)

    source_index_html = 'dist/play-time/index.html'
    destination_404_html = 'dist/play-time/404.html'
    shutil.copyfile(source_index_html, destination_404_html)
    
    gh_pages_command = "npx angular-cli-ghpages --dir=dist/play-time"
    subprocess.run(gh_pages_command, shell=True, check=True)
    
except Exception as e:
    print(f'An error occurred while building the project: {e}')
    input(exitMessage)
    exit()
input(exitMessage)
exit()