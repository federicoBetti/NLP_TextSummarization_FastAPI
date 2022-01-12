# Document Summarization

## Overview
This project consists in using FastAPI module to store documents and their summaries with the main CRUD operations.

I have used ```sqlite``` as database since it is easy to use and to reproduce on other devices. The database file is ```summary_app.db``` and it must be present in the main folder.

Document object has three fields: 
```
id: automatic generated id
text: text of the document
summary: generated summary by the AI model
```

## Files
- ai_nlp.py : this file contains the AI model used for summarization. The AI model has been wrapped in a class so that it 
can be easily upgraded. A test model has been also implemented to reduce the loading and computation time of the summary.
The ```SummaryModel``` class can be extended with new type of summarization model. The new class should then be added also to the Enum ```Models```
- api.py : main FastAPI file with the developed endpoints.
- config.ini : configuration file. So far, just the AI model choice is written there. 
DB configuration, endpoints etc. can be added to this file.
- crud.py : file in which the main CRUD operations are performed.
- database.py : main db file, used for db creation and connection.
- models.py : in this file there is the data model of the document-based app.
- schemas.py : Pydantic file in which models are specified
- test_api.py : Test file used to test API endpoints.

All these files are in the same folder for simplicity, considering the size of the project. A more structured folder structure can be used with more complex projects.


## How to RUN
At first all packages in ```requirements.txt``` file should be installed.
```
pip install -r requirements.txt
```
In order to run APIs
```
uvicorn api:app --reload
```
```--reload``` is needed in the development phase to reflect changes in the code directly in the APIs.
APIs can be tested with FastAPI default test page at ```http://127.0.0.1:8000/docs```

## Tests
First API tests have been implemented in the ```test_api.py``` file. They can be improved using an external database and making them more complete with all APIs endpoints fully tested.
To run test:
```
pytest
```
## AI
The class ```SummaryModelTransformer``` uses a pretrained summarization model from HuggingFace. There are many alternatives, some may use neural networks some may not. It really depends on the use case, on the performance required and on the computation power available which is the best choice.

Using the Transformer class will download the model selected. If you want to use the Test summarizer, you need to change the ```ModelType``` line in ```config.ini``` in ```TEST```. If a wrong ```ModelType``` is written that, by default, ```TEST``` will be used.

## Improvements
Many improvements can be done to this "app". Just to mention some of them:
- improve AI model (finetune on custom data, select different starting models, test simpler and lighter models).
- add tests and constraints on inputs from APIs
- add security tokens
- add users
- add new tests