# PyDelica: Serverless OpenModelica with Python

## About

PyDelica is an API providing a quick and easy to use interface to compile, customise and run OpenModelica models with Python. Unlike OMPython it does not require the launch of a server session to use OMShell but rather dynamically adjusts files produced after model compilation in order to update options and parameters. The lack of server requirement means models can be run in tandem without calling multiple OMC sessions which can be very taxing on CPU. Furthermore PyDelica is able to detect errors during model runs by reading the `stderr` and `stdout` from OpenModelica and throw appropriate exceptions to terminate the program execution.

## Installation

To use PyDelica you will require an installation of OpenModelica on your system, the API has been confirmed to work on both Windows and Linux, but if OM is installable on macOS it should also be possible to still use it. 

To install run:

```bash
pip install pydelica
```

## Getting Started
For the purposes of demonstration the included test model `tests/models/SineCurrent.mo` will be used.
### PyDelica Session
All uses of PyDelica require an instance of the `Session` class:

```python
from pydelica import Session

session = Session()
```

#### Logging
The `Session` class has one optional argument which is used to set the log level output within OpenModelica itself. The options are based on the `-lv` flag within OM. By default the level is set to `Normal` which means no log level output.

As an example if you wanted to run with statistics logging `-lv=LOG_STATS` you would setup with the following:

```python
from pydelica import Session
from pydelica.logger import OMLogLevel

session = Session(OMLogLevel.STATS)
```

See the source for more options [here](https://gitlab.com/krizar/pydelica/-/blob/master/pydelica/logging.py).

#### Building/Compiling Models
Before you can run a model you must first compile it. This is done using the `build_model` member function which takes the path to the Modelica source file.

```python
model_path = os.path.join('tests', 'models', 'SineCurrent.mo')
session.build_model(model_path)
```

If the required model is not top level, that is to say it exists within a module or , we can optionally specify the address within Modelica. This is also required if the required model is not the default. For example say model `A` existed within module `M`:

```python
model_path = 'FictionalModelFile.mo'
session.build_model(model_path, 'M.A')
```

#### Examining Parameters and Options
We can examine all parameters for a given model using the `get_parameters` method which will return a Python dictionary:

```python
session.get_parameters('SineCurrentModel')
```

if the parameter is unique to a single model then the model name argument can be dropped. Returning the value for a single parameter is as simple as:

```python
session.get_parameter(<parameter-name>)
```

For simulation options the analogous methods are `get_simulation_options` and `get_simulation_option` respectively for general case, for more specific see below.

#### Setting Parameters and Options
Set a parameter to a different value using the `set_parameter` function:

```python
session.set_parameter(<parameter-name>, <new-value>)
```

#### Further Configuration
The output file type can be specified:

```python
from pydelica.options import OutputFormat
session.set_output_format(OutputFormat.CSV) # Other options are MAT and PLT
```

Set the solver:

```python
from pydelica.options import Solver
session.set_solver(Solver.DASSL)    # Other options are EULER and RUNGE_KUTTA
```

Set the time range:

```python
# Each argument is optional
session.set_time_range(start_time=0, stop_time=10, model_name='SineCurrentModel')
```

Set tolerance:

```python
# Model name is optional
session.set_tolerance(tolerance=1E-9, model_name='SineCurrentModel')
```

Set variable filter for outputs:

```python
# Model name is optional
session.set_variable_filter(filter_str='output*', model_name='SineCurrentModel')
```

#### Running the Simulation
To run the simulation use the `simulate` method. If a model name is specified then that model is run,
else this is the first model in the model list. At the simulation step parameter values are written to the
XML file read by the binary before the model binary is executed.

```python
# Model name is optional, verbosity is also optional and overwrites that of the session
session.simulate(model_name='SineCurrentModel', verbosity=OMLogLevel.DEBUG)
```

#### Retrieving Results
To view the results use the `get_solutions` method which will return a python dictionary containing
the solutions for all models after a model run:

```python
solutions = session.get_solutions()
```
The variables for each model are stored as a Pandas dataframe.

## Troubleshooting

### PyDelica cannot find OMC
PyDelica relies on either locating OMC on UNIX using the `which` command, or in the case of Windows using the `OPENMODELICAHOME` environment variable. Ensure at least one of these is available after installating OpenModelica.

## Docker
PyDelica is available on Docker, images can be found [here]()
