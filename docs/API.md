### send_livepatch _POST_
Get the livepatch object by sending the UUID
#### url: /elivepatch/api/v1.0/send_livepatch
- KernelVersion type=string required=False
- UUID type=string required=False

### GetFiles _POST_
Send the information for building the livepatch object
#### url: /elivepatch/api/v1.0/get_files
- KernelVersion type=string required=False
Kernel verson needed for know which kernel we are working
- UUID type=string required=False
Assigning a Universally Unique Identifier
- patch type=werkzeug.datastructures.FileStorage required=True
Previous applied patch to kernel
- main_patch type=werkzeug.datastructures.FileStorage required=True
Patch that will be converted in the live patch object
- config type=werkzeug.datastructures.FileStorage required=True
Configuraton file of the kernel

#### example
Success
```
{
  "KernelVersion": "5.1.9",
  "UUID': '57773c4c-65e2-4ed1-9daa-345737a9b05f"
}
```

Fail
```
{
  "message": "These are not the patches you are looking for"
}
```

### Root _GET_
Root of the endpoint
#### url: /elivepatch/api/
#### example
curl -H "Accept: application/ld+json" -X GET http://localhost:5000/elivepatch/api/ | jd
success
```
{
  "agent": [
    {
      "module": "elivepatch",
      "version": "0.01"
    }
  ]
}
```

### Agent _GET_
Retrive agent informations
#### url: /elivepatch/api/v1.0/agent
#### example
curl -H "Accept: application/ld+json" -X GET http://localhost:5000/elivepatch/api/v1.0/agent | jd
success
```
{
  "agent": [
    {
      "module": "elivepatch",
      "version": "0.01"
    }
  ]
}
```
