# ServdCraft

#### Web application for managing user access for your game servers

#### In Progress. These specs can and will change drastically

## [Heroku](https://tsoha-servdcraft.herokuapp.com/)

Idea is based on a need for a managing system for whitelisting users for Minecraft servers.
Users can register and add their in game usernames under their account. Users need to send a request to get an access on the server. User can have one or more in game accounts and all of them have separate permissions. 

## Usage 
* Requirements: Python 3.5


Clone this repository : 
```
git clone https://github.com/JoonaHa/ServdCraft
```
Create venv folder inside the cloned repository:  
```
python3 -m venv venv
```

Activate venv by running:
```
venv\bin\activate
```
Install dependencies
```
pip install -r requirements.txt
```
Launch:
```
python run.py
```

---
### Week 1
Crude concept database diagram for the basic logical structures. Other tables will be needed in the future for example tabels for login and requestStates.   

![](documentation/conceptDiagram.png) 

### Week 2
* [Heroku](https://tsoha-servdcraft.herokuapp.com/)
* [User stories](documentation/userstories.md)

### Week 3
* Test credentials **username:** test **password:** 1234







