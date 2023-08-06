# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['buildgraph']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'buildgraph',
    'version': '0.0.2',
    'description': 'Tools for building',
    'long_description': '# Build Graph\n\nBuild Graph provides a set of tools to run build steps in order of their dependencies.\n\nBuild graphs can be constructed by hand, or you can let the library construct the graph for you.\n\nIn the following examples, we\'ll be using this step definition:\n```\nclass Adder(BaseStep):\n    """\n    Returns its input added to a small random number\n    """\n    def execute(self, n):\n        new = n + 1\n        print(new)\n        return new\n```\n\n## Manual construction\n\n### Defining steps\n\nSteps are defined by constructing a step definition and binding the required arguments.\n\n```\n# This will create a single \'Adder\' step with input 5\na = Adder(5)\n```\n\nStep arguments can be other steps:\n\n```\n# This will provide the output from step a as input to step b\na = Adder(0).alias("a")  # Set an alias to identify the steps\nb = Adder(a).alias("b")\n```\n\nTo run the steps, we pick the last step in the graph and call its `run` method.\n\n```\n...\nresult = b.run()\nprint(result)  # 2\n```\n\nA step from anywhere in the graph can be run, but only that step\'s dependencies will be executed.\n\n```\nprint(a.run())  # 1 - Step b won\'t be run\n```\n\n\n### Side dependencies\n\nSometimes you\'ll need to run a step `a` before step `b`, but `a`\'s output won\'t be used by `b`.\n\n```\nclass Printer(BaseStep):\n    """\n    Returns its input added to a small random number\n    """\n    def execute(self, msg):\n        print(msg)\n\np = Printer("Hi")\na = Adder(0).alias("a")\nb = Adder(a).alias("b").after(p)  # This ensures b will run after p\nb.run()\n```\n\nThe `after(*steps)` method specified steps that must be run first. If multiple steps are provided it doesn\'t enforce an ordering between those steps.\n\n\n### Detatched steps\n\nIf a step is defined but not listed as a dependency it won\'t be run:\n\n```\na = Adder(0).alias("a")\nb = Adder(1).alias("b")\nb.run()  # This won\'t run a\n```\n\nYou can check which steps will be run with the `getExecutionOrder` and `printExecutionOrder` methods.\n\n\n### Circular dependencies\n\nBuildgraph will check for loops in the graph before running it and will raise an exception if one is detected.\n\n\n## Automatic construction\n\nThe `@buildgraph` decorator builds a graph where every node is reachable from the final node.\n\n```\n@buildgraph\ndef addergraph():\n    a = Adder(0)\n    b = Adder(1)\n    c = Adder(2)\n\naddergraph.run()  # This will run all 3 steps\n```\n\nIf the steps don\'t have dependencies the execution order isn\'t guaranteed, but generally the steps that are defined first will be run first unless another dependency enforces a different order.\n\n\n### Returning from a graph\n\nGraphs can return results from a step too.\n\n```\n@buildgraph\ndef addergraph():\n    a = Adder(0)\n    b = Adder(a)\n    return b\n\nresult = addergraph.run() \nprint(result)  # 1\n```\n\n\n## Extending steps\n\nAll steps must inherit from `BaseStep` and implement an `execute` method.\n\nYou can see example steps from `src/steps.py`. These steps can also be imported and used in code.\n\n\n## Type checking\n\nBuildgraph will perform type checking when the graph is built if the `execute` method has type annotations on its parameters.\n\n\n## Configuring buildgraph\n\nBy default buildgraph prints coloured output. You can disable this with `buildgraph.setColor(False)`.',
    'author': 'ubuntom',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ubuntom/buildgraph',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
