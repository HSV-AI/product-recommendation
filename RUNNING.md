# Dependencies

This project uses Kedro for running pipelines and managing configurable data locations. The highest version of Python that kedro supports is 3.8, so we recommend running a python virtual environment with python=3.8

There is a dependency conflict between kedro\[pandas.CSVDataSet\] and the AWS s3fs library. To get this to work, we need to install s3fs first, followed by the requirement.txt.

To install dependencies, use:
```
?>python -m pip install s3fs
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