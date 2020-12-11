# storage-api

A simple **aiohttp** app that implements API with following interaction with files in server storage: 
* Upload
* Download
* Delete

### Details
Each file is stored by name equivalent to its *md5 hash* at following path:

    /store/{key}/{hash_of_the_file}

where {key} is a directory named as two characters of hash of the file, for example:

    /store/87/875d92937013e06abcbcd5758134063b

### How to run app
Server starting at localhost:8080 by executing app.py

### Documentation
All ways of interactions with files documented in swagger page, located at:
    
    http://localhost:8080/api/doc