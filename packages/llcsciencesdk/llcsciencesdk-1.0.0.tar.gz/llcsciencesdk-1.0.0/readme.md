# LLC Science SDK

> A simple way to fetch scientific data from the Science Admin. 

## Installation

```sh
pip install llcsciencesdk
```

## Updating to a new version

```sh
pip install llcsciencesdk -U
```

## Usage

#### Getting the data in JSON format

```python
from llcsciencesdk.llc_api import ScienceSdk

llc_api = ScienceSdk()
llc_api.login("username", "password")
model_input = llc_api.get_model_input_as_json(1)
```

#### Getting the data as a list of DataFrames

```python
from llcsciencesdk.llc_api import ScienceSdk

llc_api = ScienceSdk()
llc_api.login("username", "password")
model_input = llc_api.get_model_inputs_as_df(1)
```

#### Getting data with legacy version8 and version11 parameter names

```python
from llcsciencesdk.llc_api import ScienceSdk

llc_api = ScienceSdk()
llc_api.login("username", "password")
model_input = llc_api.get_model_input_as_json(1, legacy_parameters=True)
```

#### Getting data for old model runs using the old API structure

```python
from llcsciencesdk.llc_api import ScienceSdk

llc_api = ScienceSdk()
llc_api.login("username", "password")
model_input = llc_api.get_old_model_inputs([43])
```


#### Connecting to staging and local envs is also possible

```python
from llcsciencesdk.llc_api import ScienceSdk

llc_api = ScienceSdk(environment="staging")
# or 
llc_api = ScienceSdk(environment="local")

llc_api.login("username", "password")
model_input = llc_api.get_model_inputs(1)
```

