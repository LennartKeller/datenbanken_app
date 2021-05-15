# FastAl

An easy, web-based and active learning aided annotation tool.

## Installation

Install the backend dependencies using pipenv

```bash
pipenv install --dev
```

Install the frontend dependencies using yarn

```bash
yarn install
```

## Create a collection

A collection represents a bunch of texts and one or more annotations tasks associated with the texts.
It is defined by a single JSON file, containing both the configuration of the annotation process, and the data.
It has the following general format:

__Note__: Currently only sequence classification is available as task-type.

```json
{
    "Config": {
        "Name": "TestCollection",
        "Tasks": [
            {
                "Type": "SequenceClassification",
                "Name": "Task-1",
                "Description": "Short task description for annotators.",
                "Classes": [
                    "Negative",
                    "Positive"
                ],
                "ActiveLearning": {
                    "Enabled": true,
                    "Start": 1,
                    "ModelName": "LogRegUncertainty"
                }
            }
        ]
    },
    "Texts": [
        "Text 1...", 
	"Text 2...",
	"..."
    ]
}
```

If a annotation task should not be alleviated by active learning, just remove the active learning part
from the task configuration.
It is also possible to use active learning with multiple tasks of the same collection, in this case at each iteration
an instance for each task is queried.


## Initialization

To initialize the database use the builtin cli-tool (from within the pipenv environment)

```bash
python cli.py init-db
```

To add a collection also use the cli-tool
```bash
python cli.py from-json <YourCollection>.json
```

## Startup

To start the development server for the backend type

```bash
pipenv shell
flask run --debugger --reload
```

To start the frontend dev server type

```
yarn serve
```

The application should now be running under http://localhost:8080

## Define custom active learning components
TODO
