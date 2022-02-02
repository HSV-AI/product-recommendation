# Dependencies

This project uses Kedro for running pipelines and managing configurable data locations. The highest version of Python that kedro supports is 3.8, so we recommend running a python virtual environment with python=3.8

To install dependencies, use:
```
?>python -m pip install -r src/requirements.txt
```

# AWS Configuration

In order to load/save data from AWS S3 locations, you will need to have your key & secret tokens exported in your environment. The best way to do this is to create a .env file at the root of the repository and add your information to that file. The .env file is ignored (based on the .gitignore file) and will not be uploaded to the repository.

```
# Needed by the implicit library - otherwise it will warn you
export OPENBLAS_NUM_THREADS=1

export AWS_ACCESS_KEY_ID=<your key ID here>
export AWS_SECRET_ACCESS_KEY=<your secret key here>
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