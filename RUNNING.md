# Dependencies

This project uses Kedro for running pipelines and managing configurable data locations. The highest version of Python that kedro supports is 3.8, so we recommend running a python virtual environment with python=3.8

To install dependencies, use:
```
?>python -m pip install -r src/requirements.txt
```

# Running

To check for a correct kedro installation, run

```
?>kedro info
```

To get a list of pipelines available to run:

```
?>kedro pipeline list
```

```
?>kedro run --pipeline pipeline_name
```