from google.cloud import storage
import os
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../machine-learning-testenv-92abff945a2c.json"

# Instantiates a client
storage_client = storage.Client()
# Creates the new bucket
bucket = storage_client.get_bucket('product-image-catalogs')

blob = bucket.blob('SFS/sort_dict/cluster_sort_dict_SFS/cluster_sort_dict_SFS_foldernames.json')
file = blob.download_as_string()
json_file = json.loads(file)

#blob.upload_from_string(json.dumps(file))

print("end")
