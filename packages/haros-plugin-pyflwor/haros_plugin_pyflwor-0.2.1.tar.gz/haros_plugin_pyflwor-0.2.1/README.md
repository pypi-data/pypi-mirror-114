# HAROS Pyflwor Plugin

This is a HAROS plugin to query extracted Computation Graph models using [pyflwor](https://github.com/timtadh/pyflwor).

Basic use cases include ensuring that every topic has at most one publisher (a common guideline in many systems), or detecting the use of conditional publishers and subscribers.
For instance, the latter is given by the pattern:

```python
nodes/publishers[len(self.conditions) > 0] | nodes/subscribers[len(self.conditions) > 0]
```

This pattern matches publishers or subscribers with associated conditions (e.g., under an `if` statement).

A more complex example is a compile-time type-checking system for ROS topics, a feature that ROS lacks.

```python
for p in <nodes/publishers | nodes/subscribers>,
    s in <nodes/publishers | nodes/subscribers>
where p.topic_name == s.topic_name and p.type != s.type
return p, s
```

Pattern matches are reported as issues to HAROS, and may show up as highlights in extracted models.

![HAROSviz](./docs/viz-query-model.png?raw=true "HAROS visualizer with issue highlights")

## Installing

Installing a pre-packaged release:

```bash
pip install haros-plugin-pyflwor
```

Installing from source:

```bash
git clone https://github.com/git-afsantos/haros-plugin-pyflwor.git
cd haros-plugin-pyflwor
pip install -e .
```

## Usage

Queries can be defined in HAROS project files, under specific configurations, and specified as input for this plugin.
For example:

```yaml
%YAML 1.1
---
project: Fictibot
packages:
  - fictibot_drivers
  - fictibot_controller
  - fictibot_multiplex
  - fictibot_msgs
configurations:
  name_collision:
    launch:
      - fictibot_controller/launch/name_collision.launch
    user_data:
      haros_plugin_pyflwor:
        - name: Query 6 - One Publisher Per Topic
          details: "Found {n} publishers on a single topic - {entities}"
          query: "topics[len(self.publishers) > 1]"
```

- The `name` field is the title for the reported issue in HAROS.
- The `details` field (optional) is a Python format string with a long description of the reported issue.
It accepts the parameters `entities` (the matched entities), `value` (if the query returns a specific value, e.g., a number) and `n` (the number of matches).
- The `query` field is where the query itself goes.

Queries follow the [pyflwor](https://github.com/timtadh/pyflwor) syntax.

By default, they have a number of builtin functions available:

```python
QUERY_CONTEXT = {
    "True": True,
    "False": False,
    "None": None,
    "abs": abs,
    "bool": bool,
    "cmp": cmp,
    "divmod": divmod,
    "float": float,
    "int": int,
    "isinstance": isinstance,
    "len": len,
    "long": int,
    "max": max,
    "min": min,
    "pow": pow,
    "sum": sum,
    "round": round,
    "is_rosglobal": is_rosglobal
}

def is_rosglobal(name):
    return name and name.startswith("/")
```

Queries have access to the following base entities (see the [HAROS metamodel](https://github.com/git-afsantos/haros/blob/master/haros/metamodel.py)):

- `config` - the current `Configuration` being queried.
- `nodes` - the set of *runtime* nodes belonging to the configuration (`NodeInstance`).
- `topics` - the set of topics belonging to the configuration (`Topic`).
- `services` - the set of services belonging to the configuration (`Service`).
- `parameters` - the set of parameters belonging to the configuration (`Parameter`).


## Bugs, Questions and Support

Please use the [issue tracker](https://github.com/git-afsantos/haros-plugin-pyflwor/issues).

## Contributing

See [CONTRIBUTING](./CONTRIBUTING.md).

## Acknowledgment

Until March 2021, this work was financed by the ERDF – European Regional Development Fund through the Operational Programme for Competitiveness and Internationalisation - COMPETE 2020 Programme and by National Funds through the Portuguese funding agency, FCT - Fundação para a Ciência e a Tecnologia within project PTDC/CCI-INF/29583/2017 (POCI-01-0145-FEDER-029583).
