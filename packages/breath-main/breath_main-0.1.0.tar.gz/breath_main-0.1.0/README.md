# BReATH - Brazilian Research of Atmosphere Towards Health

BReATH project aims to create a interface to visualize and get insights relating asthma and weather data.

It depends on our other modules:
- [breath_api_interface](https://github.com/BReATH-Brazilian-Research/breath_api_interface) to connect all our modules. [Gitlab mirror](https://gitlab.com/breath_unicamp/breath_api_interface).
- [breath_data](https://github.com/BReATH-Brazilian-Research/breath_data) for data operations. [Gitlab mirror](https://gitlab.com/breath_unicamp/breath_api_interface)
- [breath_ml](https://github.com/BReATH-Brazilian-Research/breath_ml) for machine learning operations. 

<br>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Tensorflow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=TensorFlow&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white) ![Numpy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white) ![MatPlotLib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge)

## How to execute:

- Install `breath_main`: 
  - Windows: `python -m pip install breath_main`
  - Linux: `pip3 install breath_main`
- Install `tensorflow`:
  - Windows: `python -m pip install tensorflow`
  - Linux: `pip3 install tensorflow`
- Run breath_main:
  - Windows: `python -m breath_main`
  - Linux: `python3 -m breath_main`
- Select operation in the menu (enter the desired option)

## Features:

We have some features implemented:

- Search for some brazilian city in the data bank, returning its position, state and population; and making it available to perform other operations. Implements [#37](https://gitlab.com/breath_unicamp/breath-brazilian-research-of-atmosphere-towards-health/-/issues/37)
- Plot a city's history of cases of fever, cough, or sore throat. Implements [#27](https://gitlab.com/breath_unicamp/breath-brazilian-research-of-atmosphere-towards-health/-/issues/27)
- Show a city's cases in some specific date. Implements [#28](https://gitlab.com/breath_unicamp/breath-brazilian-research-of-atmosphere-towards-health/-/issues/28)
- View current weather data in the city. Implements [#21](https://gitlab.com/breath_unicamp/breath-brazilian-research-of-atmosphere-towards-health/-/issues/21), [#13](https://gitlab.com/breath_unicamp/breath-brazilian-research-of-atmosphere-towards-health/-/issues/13), [#39](https://gitlab.com/breath_unicamp/breath-brazilian-research-of-atmosphere-towards-health/-/issues/39).
- Predicts the occurrence of current cases of fever, flu or cough in the city. Implements [#33](https://gitlab.com/breath_unicamp/breath-brazilian-research-of-atmosphere-towards-health/-/issues/33). NOTE: The model is still under development, and at the moment it does not make very correct predictions.
- Register new user symptoms. Implements [#30](https://gitlab.com/breath_unicamp/breath-brazilian-research-of-atmosphere-towards-health/-/issues/30).

# Authors

- [233840, Elton Cardoso do Nascimento](https://github.com/EltonCN)
- [218733, João Pedro de Moraes Bonucci](https://github.com/Joao-Pedro-MB)
- [240106, Lucas Otávio Nascimento de Araújo](https://github.com/Lucas-Otavio)
- [244712, Thiago Danilo Silva de Lacerda](https://github.com/ThiagoDSL)

# Software architecture

Our software system is architected using C4 and UML diagrams. This repository contains the main application and service management, with other services separated across multiple repositories, containing our different Python modules. It was divided in this way to help manage the different activities of the disciplines linked to this project.

![](images/PythonModules.png) 


## Context
![](images/Context.png) 

This project context consists of 3 stakeholders, the Patient, the Health Manager, and the Physicist/Medic, which have access to 2 different sets of features: the Map visualization and the patient portal. 
The first set consists of an interface with geolocalized information about climate, respiratory diseases, air quality, and history of respiratory diseases through time by city. This service also estimates the number of cases for the following days through the air quality and climate information.
The second set of features show a widget that condensates the information of the climate and air quality. It also shows the consequences of those for the patient's symptoms and offers some tips on how to avoid or mitigate them.
A Session Manager will link the frontend services to the background services of Data workflow, Prediction, and Data requests from exterior sources. In addition, it is responsible for writing and retrieving data from relational and graph databases.

## Container and components

_Container diagram_
![](images/Container.png) 

Our container level describes our **service-oriented architecture**. Each service performs a set of operations, and is isolated in a different Python process. 

Within the containers section we also have the component and code level description. We describe only the main and the already designed components of the architecture, as some are related to features not yet started.


### Session Manager:
This container orchestrates service requests, and handles the login session.

![](images\Diagram_SessionManager.PNG)

#### RequestSessionManager:
Handles the lifecycle of a request, from receiving it to sending its response.
We used the [Chain of Responsibility](https://refactoring.guru/pt-br/design-patterns/chain-of-responsibility) design pattern to create it, as can be seen on its code diagram. Because we use Python, which supports multiple inheritance, we use an abstract class, as there is no difference between it and an interface.

__Code diagram__
![](images/Code.png)

### BReATH Map and Patient Portal:
These containers have a Layering Structure that intends to be an MVC. Divided into View, the top layer, Model, the middle layer, and a ServiceProxy as the bottom layer and link with the session manager. We used the [Proxy](https://refactoring.guru/pt-br/design-patterns/proxy) Design Pattern because of the service request complexity.

**In the current version, we are temporarily using ConsoleApplication, terminal version of the application**

![](images\Diagram_Portal.PNG)

### DataWorflow: 
This container acts as a data formatter and validator before saving it into the database. Regarding this behavior, we used an [Adapter](https://refactoring.guru/design-patterns/adapter) design pattern to clean and reshape the data for the rest of the application.

![](images/Diagram_DataWorkflow.PNG)

### DataRequester: 
This container is responsible for requesting and receiving data from external APIs. Due to the possible asynchrony of the task, we used the [Observer](https://refactoring.guru/design-patterns/observer) design pattern to make sure the rest of the application could continue without problems. However, we also decided to implement the [abstract factory](https://refactoring.guru/design-patterns/abstract-factory) design once we could switch APIs or add new ones in the future.

**It was put together as part of DataWorkflow**

![](images\Diagram_DataRequester.PNG)

### Prediction:
The Prediction module has an ML model, implemented in TensorFlow, used to predict in real-time the consequences of the climate and air quality over the symptoms and occurrences of respiratory diseases. As this is a central point of the application, it will receive a large number of requests. For this reason, we used a [Proxy](https://refactoring.guru/design-patterns/proxy) Design to help handle those.

![](images\Diagram_Prediction.PNG)

### BDAcessPoint:
The access point uses a [factory](https://refactoring.guru/design-patterns/abstract-factory) Design pattern for the two possible databases to make the queries faster. The Design is divided through the GraphQuerier, RelationalQuerier, and RequestProcessor, which is the factory controller.

**The graph database was not used**

![](images\Diagram_BD_AcessPoint.PNG)

### Databases:
- SQL: Users, patients, symptoms and diagnosis. Also geolocated atmosphere data. It will use SQLite.
- Graph: Geographical information (political wise), relationship between symptoms and diseases. It will use Neo4j.