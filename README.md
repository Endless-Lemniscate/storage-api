# storage-api

Simple **aiohttp** app that implements API with following interaction with files on server storage: 
* Upload
* Download
* Delete

### Details
Each file is stored by name equivalent to its *md5 hash* at following path:

    /store/{key}/{hash_of_the_file}

where {key} is a directory named same as first two characters of hash of the file string, for example:

    /store/87/875d92937013e06abcbcd5758134063b

### How to run app
Server starting at localhost:8080 by executing app.py

### Documentation
All methods of interactions with files documented in swagger page, located at:
    
    http://localhost:8080/api/doc

Important values, such as host, port, path_to_swagger and storage_folder_name can be configured at:

    config.yaml