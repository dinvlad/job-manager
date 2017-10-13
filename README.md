# Job Monitor

Job Monitor API and UI for interacting with asynchronous batch jobs.

## Development

Prequisite: the following commands assume you have symlinked your preferred
local API backend docker compose file as `docker-compose.yml` (alternatively,
use `docker-compose -f dsub-google-compose.yml CMD`), e.g.:

```
ln -sf dsub-local-compose.yml docker-compose.yml

# For dsub local, also create a local tmp dir before continuing:
mkdir /tmp/dsub-local
```

Then...

```
docker-compose up
```

Navigate to http://localhost:4200.

Note: websocket reload on code change does not work in docker-compose (see
https://github.com/angular/angular-cli/issues/6349).

Changes to `package.json` or `requirements.txt` require a rebuild:

```
docker-compose up --build
```

Alternatively, rebuild a single component:

```
docker-compose build ui
```

### Google dsub provider

The Google dsub provider requires making authorized calls to the Google Genomics
Pipelines API. The dsub shim server authorizes via [application default
credentials](https://developers.google.com/identity/protocols/application-default-credentials).
On your workstation, you'll need to first login via [gcloud](https://cloud.google.com/sdk/docs/quickstarts).

```
gcloud auth application-default login
ln -sf dsub-google-compose.yml docker-compose.yml
docker-compose up
```

Navigate to http://localhost:4200?parentId=MY_CLOUD_PROJECT_ID.

## Setup Lint Git Hook:
```
sudo pip install yapf
ln -s -f ../../hooks/pre-commit .git/hooks/pre-commit
```

## Updating the API using swagger-codegen

We use [swagger-codegen](https://github.com/swagger-api/swagger-codegen) to automatically implement the API as defined in api/jobs.yaml.
Whenever the API is updated, follow these steps to update the UI implementation:

If you do not already have the jar, you can download it here:
```
wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.2.3/swagger-codegen-cli-2.2.3.jar -O swagger-codegen-cli.jar
```

Clear out existing generated models:
```
rm ui/src/app/shared/model/*
```

Regenerate both the python and angular definitions.
```
java -jar swagger-codegen-cli.jar generate \
 -i api/jobs.yaml \
 -l typescript-angular2 \
 -o ui/src/app/shared
java -jar swagger-codegen-cli.jar generate \
 -i api/jobs.yaml \
 -l python-flask \
 -o servers/dsub \
 -DsupportPython2=true,packageName=jobs
```

Finally, update the UI implementation to resolve any broken dependencies on old API definitions or implement additional functionality to match the new specs.

## Job Monitor UI

UI-specific documentation can be found in the [ui/ folder](ui/README.md).

### Running unit tests

From the /ui directory, run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

### Running end-to-end tests

From the /ui directory, run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).
Before running the tests make sure you are serving the app via `ng serve`.

## Jobs API servers

### dsub

Thin shim around [dsub](https://github.com/googlegenomics/dsub), see
[servers/dsub](servers/dsub).

#### Running unit tests

```
cd servers/dsub
pip install tox
tox
```

#### requirements.txt

requirements.txt is autogenerated from requirements-to-freeze.txt. The latter
lists only direct dependencies. To regenerate requirements.txt:

```
virtualenv --python=/usr/bin/python2 /tmp/dsub-shim-requirements
source /tmp/dsub-shim-requirements/bin/activate
pip install -r servers/dsub/requirements-to-freeze.txt
pip freeze | sort > servers/dsub/requirements.txt
deactivate
```
