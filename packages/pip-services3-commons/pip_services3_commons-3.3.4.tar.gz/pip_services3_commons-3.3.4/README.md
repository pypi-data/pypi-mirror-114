# <img src="https://uploads-ssl.webflow.com/5ea5d3315186cf5ec60c3ee4/5edf1c94ce4c859f2b188094_logo.svg" alt="Pip.Services Logo" width="200"> <br/> Portable Abstractions and Patterns for Python

This module is a part of the [Pip.Services](http://pip.services.org) polyglot microservices toolkit.
It provides a set of basic patterns used in microservices or backend services.
Also the module implemenets a reasonably thin abstraction layer over most fundamental functions across
all languages supported by the toolkit to facilitate symmetric implementation.

The module contains the following packages:
- **Commands** - commanding and eventing patterns
- **Config** - configuration pattern
- **Convert** - portable value converters
- **Data** - data patterns
- **Errors**- application errors
- **Random** - random data generators
- **Refer** - locator inversion of control (IoC) pattern
- **Reflect** - portable reflection utilities
- **Run** - component life-cycle management patterns
- **Validate** - validation patterns

<a name="links"></a> Quick links:

* [Configuration Pattern](https://www.pipservices.org/recipies/configuration) 
* [Locator Pattern](https://www.pipservices.org/recipies/references)
* [Component Lifecycle](https://www.pipservices.org/recipies/component-lifecycle)
* [Components with Active Logic](https://www.pipservices.org/recipies/active-logic)
* [Data Patterns](https://www.pipservices.org/recipies/memory-persistence)
* [API Reference](https://pip-services3-python.github.io/pip-services3-commons-python/index.html)
* [Change Log](CHANGELOG.md)
* [Get Help](https://www.pipservices.org/community/help)
* [Contribute](https://www.pipservices.org/community/contribute)

## Use

Install the Python package as
```bash
pip install pip_services3_commons
```

Then you are ready to start using the Pip.Services patterns to augment your backend code.

For instance, here is how you can implement a component, that receives configuration, get assigned references,
can be opened and closed using the patterns from this module.

```python
from pip_services3_commons.config import IConfigurable, ConfigParams
from pip_services3_commons.refer import IReferenceable, IReferences, Descriptor
from pip_services3_commons.run import IOpenable


class MyComponentA(IConfigurable, IReferenceable, IOpenable):
    _param1 = 'ABC'
    _param2 = 123
    _another_component: MyComponentB
    _opened = True

    def configure(self, config):
        self._param1 = ConfigParams.get_as_string_with_default("param1", self._param1)
        self._param2 = config.get_as_integer_with_default("param2", self._param2)

    def set_references(self, references):
        self._another_component = references.get_one_required(
            Descriptor("myservice", "mycomponent-b", "*", "*", "1.0")
        )

    def is_opened(self):
        return self._opened

    def open(self, correlation_id):
        self._opened = True
        print("MyComponentA has been opened.")

    def close(self, correlation_id):
        self._opened = True
        print("MyComponentA has been closed.")
```

Then here is how the component can be used in the code

```python
from pip_services3_commons.config import IConfigurable, ConfigParams
from pip_services3_commons.refer import References, Descriptor

my_component_A = MyComponentA()

# Configure the component
my_component_A.configure(ConfigParams.from_tuples(
    'param1', 'XYZ',
    'param2', 987
))

# Set references to the component
my_component_A.set_references(References.from_tuples(
    Descriptor("myservice", "mycomponent-b", "default", "default", "1.0"), my_component_B
))

# Open the component
my_component_A.open("123")
print("MyComponentA has been opened.")
```

## Develop

For development you shall install the following prerequisites:
* Python 3.7+
* Visual Studio Code or another IDE of your choice
* Docker

Install dependencies:
```bash
pip install -r requirements.txt
```

Run automated tests:
```bash
python test.py
```

Generate API documentation:
```bash
./docgen.ps1
```

Before committing changes run dockerized build and test as:
```bash
./build.ps1
./test.ps1
./clear.ps1
```

## Contacts

The library is created and maintained by:
- **Sergey Seroukhov**
- **Danil Prisiazhnyi**
