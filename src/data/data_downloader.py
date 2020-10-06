import os.path as path
import wget
import zipfile

## Data will be downloaded in the folder data/raw/
data_download_path =  path.abspath(path.join("../../data/raw"))
## We are downloading the mysql.zip file and storing it in folder data/raw
wget.download("https://github.com/SankBad/configuration_datasets/raw/master/configfiles/mysql/mysql.zip", data_download_path)
## We are unzipping the file inside the data/raw
with zipfile.ZipFile("../../data/raw/mysql.zip", 'r') as zip_ref:
    zip_ref.extractall(data_download_path)

