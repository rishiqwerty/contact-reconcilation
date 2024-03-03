# Identity Reconcilation

#### Tech Used:
- Language: Python
- Framework: FastAPI

#### Local Setup
- Clone this repo
- Install python(preferebly version 3.11)
- Create new virtual env
```
    python -m venv env
```
- Activate the environment
- Install all the requirements mentioned in requirements.txt
```
    cd backend
    pip install -r requirements.txt
```
- 

APIs are hosted at render.com
- We have swagger UI provided with FAST API where we can interact with APIs. Goto below link to access Swagger UI  
    **Swagger UI API Link**: [https://contact-reconcilation.onrender.com/docs/](https://contact-reconcilation.onrender.com/docs/)
![Swagger UI](/README_images/image.png)
- To get list of all the contacts we can make GET request at /identity endpoint
![Alt GET Request](/README_images/GET.png)
- To add new contact with checks we can do POST request at /identity endpoint with phoneNumber and email.

![Alt POST request](/README_images/POST_req.png)

Response contains data of emails, phoneNumbers,secondaryids associated with primaryContactId
![Alt response](/README_images/POST_res.png)

**Note:
For testing in POSTMAN/curl [https://contact-reconcilation.onrender.com/identity/](https://contact-reconcilation.onrender.com/identity/) can be used.
