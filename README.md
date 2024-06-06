# Quilibrium Tooling
⚒️ Tooling for quilibrium.com
This repo contains various toolings and small scripts we have used internally for testing out the best configurations for $QUIL and scaling mining operations. We will add throughout the times new scripts to this Repo.
# Key, Config & Store Exporter
This script runs through every machine via SSH (IP & Password needed, Script is assuming that root is the username) and downloads the config.yml, keys.yml and the content of the /store/ folder.
Before starting the script you will need to do the following:
1. Create a folder called *keys* on the same level as the script
2. Within the *keys* folder create a new subfolder for the provider you want to export, as many users have different nodes hosted by different providers
3. After that fill the list of machines with your actual machines, you will need for each machine to put in the IP and the respective password for the root user. **Important:** You can add as many machines as you want, you just need to separate them by commas.
4. Before actually running your script, go to line 12 (prior to adding the machines) and change the value of ***base_download_directory*** to contain your provider, e.g. **base_download_directory = "keys/myprovider"**
5. Install the dependencies with pip / pip3 - only paramiko for now: pip install paramiko
6. Then you can start your script with python3 key_export.py or python key_export.py
