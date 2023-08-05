
ailab-lite
===============================

**AI Lab** is a cloud-based enterprise software application built by [Fathom Solutions](https://fathom.io/) that enables building data workflows, managing experiments and deploying models. The **ailab-lite** library enables us to harness the power of the AI Lab product in a simple Jupyter Notebook setting. By adding this extension, the user can exploit the GUI node editor to create and test complicated data pipelines. Below is a link to a visualisation of how to generate an example workflow in Jupyter Notebook using the **ailab-lite** extension:

https://github.com/fathom-io/ailab-lite/blob/master/graphics/workflow.gif

The main idea of this product resolves around using the UI to construct a graph, which is later used to generate a data processing pipeline. The following image shows an example visualisation of a particular graph in the AI Lab product. 

<img src="https://github.com/fathom-io/ailab-lite/blob/master/graphics/ailab_example.png"/>

Next , there is the same graph generated in the Jupyter Notebook extension.

<img src="https://github.com/fathom-io/ailab-lite/blob/master/graphics/ailab_lite_example.png"/>

Each node represents a certain data transformation, model or validation process. Thinking of all these elements as one large graph lets us encapsulate our whole data processing and prediction pipeline into one object. Communication between each node is assured thanks to using a similar API to the ones used in libraries:
- scikit-learn https://scikit-learn.org/stable/developers/develop.html
- MLlib https://spark.apache.org/docs/latest/ml-pipeline.html

### Buttons
Buttons in the editor are revealed after a dataset and at least one component are added to the graph. Before running an experiment, validation must be performed. After clicking the validation button and reveiving positive feedback, the run option appears. When running an experiment the results are printed below the GUI and additional files are saved in the same folder as the opened notebook.


Installation
------------

To install use pip:

    $ pip install ailab_lite

------------

### Instructions

#### Jupyter Notebook/Lab
Import node editor widget:
```python
from ailab_lite import NodeEditorWidget
```

Import pandas:
```python
import pandas as pd
```

Decalare dataset:
```python
example = pd.read_csv("example.csv")
```

Run widget:
```python
NodeEditorWidget(env=globals())
```
We initialize it with `globals()` so all previously defined datasets are available in node editor.

We can pass workflow definition directly when initializing widget:
```python
NodeEditorWidget(env=globals(), workflow_definition="definition")
```

---

### Running example
The `examples` directory contain example of widget usage. It contain predefined workflow.
To run it, simply `cd` to the directory and run `jupyter notebook` or `jupyter lab` command.

(In order to run widget in the example first time it is required to run all cells. Other way the widget won't render)

---

### Development
For a development installation (requires [Node.js](https://nodejs.org) and [Yarn version 1](https://classic.yarnpkg.com/)),

    $ git clone https://github.com/fathoms-io/ailab-lite.git
    $ cd ailab-lite
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --overwrite --sys-prefix ailab_lite
    $ jupyter nbextension enable --py --sys-prefix ailab_lite

When actively developing your extension for JupyterLab, run the command:

    $ jupyter labextension develop --overwrite ailab_lite

Then you need to rebuild the JS when you make a code change:

    $ cd js
    $ yarn run build

You then need to refresh the JupyterLab page when your javascript changes.
