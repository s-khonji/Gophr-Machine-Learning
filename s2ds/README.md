## S2DS GOPHR 

A repository for the GOPHR S2DS project. 

### Getting Started

#### Python Interpreter

To work with this Python repository, you need a Python interpreter and the conda Python environment manager. The easiest
way to start is to download Anaconda's Python distribution which includes both. Get the 'Individual Edition' for your OS
at https://www.anaconda.com/products/individual and install it.

#### Environment 

A package manager ensures that the packages used in the repository code met the same requirements on every copy of
the repository. To achieve this, an environment is created according to the definitions in the `environment.yml` file in
the repository root.
To create the provided conda environment run the following command in the terminal after completing the 
installation of Anaconda:
```
conda env create --file environment.yml
```
If you're running a Windows system, you may need to run the commands from the `Anaconda Prompt (Anaconda3)` entry in the
start menu. You may use the regular terminal on MacOS.

Once you have created the environment, you need to activate it with 
```
conda activate s2ds
```
You see the currently active conda environment as a prefix to the command prompt enclosed in parentheses. It should be
`(s2ds)` after activation with the previous command.

You may need to reactivate the environment every time you start a new command prompt which is not prefixed by `(s2ds)`.

#### Jupyter notebook

An easy way to run Python code, conduct analyses and share results is by Jupyter notebooks which provide an interactive
interface to the the packages and functions in the current environment. You start the Jupyter server by running the
following command in an environment terminal
```
jupyter notebook
```
Then your default web browser should open a tab with an illustration of the project's repository structure. By
convention, Jupyter notebooks are stored in the subfolder `notebooks`. Change to that folder in the Jupyter browser tab.

### Project Gophr notebooks

A jupyter notebook contains executable Python code cells, along with their result from previous executions and
additional Markup cells containing headings, comments and explanations. You can execute ('run') a notebook cell on your 
own by pressing Shift + Enter or by using the appropriate button from the Jupyter browser tab. You also can run a whole 
notebook at once.

Each project notebook has been run so that its output can be directly inspected. It only has to be re-run if you're
going to change the code. Each notebook also contains the relevant background information to what it does code in the
comment cells.

There are three types of relevant project notebooks:
* __Cleaning and Feature Extraction__: This notebooks reads the SQL queries, cleans the data and extracts the feature
for further modeling, along with extensive commenting on how these tasks are achieved. If you want to run any of the
other notebooks, you need to run this notebook first.
* __Team Gophr EDA Notebook__: This notebooks contains all kinds of exploratory data analysis. If you're looking for
graphs and figures, this is the place to go.
* __ML models 1, 2, 3__: Three notebooks which contain our three modeling approaches, and their respective results, the models
their evaluation.

### Project structure

A brief description of the repository structure:
* __data__: Folder for actual query results, cleaned and external datasets. Data files and folders are created on the
fly if needed.
* __model__: Binary representations of the trained models.
* __notebooks__: Jupyter notebooks, see previous section.
* __reports__: This actually contains only the subfolder figures with some additional figures that may be not contained 
in the EDA notebook.
* __src__: The project source tree with the corresponding project Python packages. The packages are
    * __data__: modules for querying and cleaning the data, along with the actual queries
    * __features__: modules for feature generation
    * __models__: modules accomplishing the actual modeling
    * __utils__: modules providing some utility functions for path and input/output handling
    * __viz__: modules for visualisation
  

### Notes

The SQL query credentials are hard coded in the Python file `src/data/execute_query_and_save_df.py`, which should be 
altered in another deployment context for security reasons.