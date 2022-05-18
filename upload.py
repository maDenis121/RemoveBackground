import os
import yaml
from azure.storage.blob import ContainerClient

def upload_file(fileName, fileData):
    config = load_config()
    container_client = ContainerClient.from_connection_string(config["azure_storage_connectionstring"], config["images_container_name"])

    blob_client = container_client.get_blob_client(fileName)
    blob_client.upload_blob(fileData)
    print(f'{fileName} upload to blob storage')

def download_file(fileName):
    config = load_config()
    container_client = ContainerClient.from_connection_string(config["azure_storage_connectionstring"], config["images_container_name"])
    
    print('Downloading ' + fileName)
    fileData = container_client.get_blob_client(fileName).download_blob().readall()
    return fileData

# ------------------------------------------------------------

def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)

def get_files(dir):
    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.is_file() and not entry.name.startswith('.'):
                yield entry

def save_file(filename, bytes, path):
    full_path = path + "/" + filename
    with open(full_path, "wb") as file:
        file.write(bytes)

def upload(files, connection_string, container_name):
    container_client = ContainerClient.from_connection_string(connection_string, container_name)
    print("Uploading files to blob storage...")

    for file in files:
        blob_client = container_client.get_blob_client(file.name)
        with open(file.path, "rb") as data:
            blob_client.upload_blob(data)
            print(f'{file.name} upload to blob storage')


def list_blobs(connection_string, container_name):
    container_client = ContainerClient.from_connection_string(connection_string, container_name)
    print("Listing container content...")

    blobs = container_client.list_blobs()
    for blob in blobs:
        print('\tBlob Name: ' + blob.name)

def download_blobs(connection_string, container_name, download_folder):
    container_client = ContainerClient.from_connection_string(connection_string, container_name)
    print("Downloading container content...")

    blobs = container_client.list_blobs()
    for blob in blobs:
        print('Downloading ' + blob.name)
        bytes = container_client.get_blob_client(blob.name).download_blob().readall()
        save_file(blob.name, bytes, download_folder)


# config = load_config()
# images = get_files(config["source_folder"]+ "/imatges")
# print(*images)
# upload(images, config["azure_storage_connectionstring"], config["images_container_name"])
# list_blobs(config["azure_storage_connectionstring"], config["images_container_name"])
# download_blobs(config["azure_storage_connectionstring"], config["images_container_name"], config["download_folder"])