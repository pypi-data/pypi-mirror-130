# Import package in conf.py
# Add package to LIST_MODULES
rm -rf doc
mkdir doc
sphinx-apidoc -F -M -d 1 --separate -o doc iguanas iguanas/*setup*
cd doc
rm conf.py
cp ../iguanas_logo.png .
# Create conf.py file
cat >> conf.py <<EOL
import sys
import os
sys.path.insert(0, os.getcwd())
sys.path.insert(1, os.path.abspath('../iguanas/'))
project = 'Iguanas'
copyright = '2021, James Laidler'
author = 'James Laidler'
html_logo = 'iguanas_logo.png'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.napoleon',
    'nbsphinx',
    'sphinx_rtd_theme',
]
autodoc_member_order = "bysource"
templates_path = ['_templates']
language = 'en'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
todo_include_todos = True
EOL
# Create style.css so page width is not limited
cat >> _static/style.css <<EOL
.wy-nav-content {
    max-width: none;
}
EOL
# Reference style.css in layout.html template
cat >> _templates/layout.html <<EOL
{% extends "!layout.html" %}
{% block extrahead %}
    <link href="{{ pathto("_static/style.css", True) }}" rel="stylesheet" type="text/css">
{% endblock %}
EOL
rm index.rst
# Generate index.rst (for index.html page)
cat >> index.rst <<EOL
Iguanas
================================================

Introduction
------------

Iguanas is a fast, flexible and modular Python package for:

* Generating new fraud-capture rules using a labelled dataset.
* Optimising existing rules using a labelled or unlabelled dataset.
* Combining rule sets and removing/filtering those which are unnecessary.
* Generating rule scores based on their performance.

It aims to help streamline the process for developing a deployment-ready Rules-Based System (RBS) for **binary classification use cases**.

Installation
------------

See https://github.com/paypal/Iguanas for steps on installing Iguanas.

Package documentation
---------------------

The below links contain the following information for each module:

* Example notebooks showing how the module can be used.
* Docstrings for the classes and methods within the module.

.. toctree::
   :maxdepth: 3

   iguanas

EOL
# Add full Iguanas examples (add relevant part to iguanas.rst)
cp ../examples/*ipynb .
sed -i '' "5i\\
Notebooks \\
--------- \\
\\
.. toctree:: \\
    \ \ \ \ \ \ :titlesonly: \\
    \\
" iguanas.rst
sed -i '' "s/Module contents/ /" iguanas.rst
sed -i '' "s/---------------/  /" iguanas.rst
sed -i '' "s/\.\. automodule:: iguanas//" iguanas.rst
sed -i '' "s/:members:/ /" iguanas.rst
sed -i '' "s/:undoc-members:/ /" iguanas.rst
sed -i '' "s/:show-inheritance:/ /" iguanas.rst
echo ".. include:: ../READMEs/README_iguanas.rst" >> iguanas.rst

# Loop through modules and add part for example notebooks
LIST_MODULES="correlation_reduction rbs rule_application rule_generation rule_optimisation rule_scoring rule_selection rules"
for module in $LIST_MODULES
do
    echo $module    
    cp ../iguanas/$module/examples/*.ipynb .    
    filename="iguanas.$module.rst"            
    sed -i '' "5i\\
Notebooks \\
--------- \\
\\
.. toctree:: \\
    \ \ \ \ \ \ :titlesonly: \\
    \\
" $filename
    for file in ../iguanas/$module/examples/*.ipynb; do            
        file_only="${file##*/}"
        file_no_extension="${file_only%%.*}"                
        echo $file_only
        echo $file_no_extension        
        sed -i '' "11i\\
\ \ \ \ \ \ \ \ \ \ $file_no_extension \\
" $filename
    done
    sed -i '' "s/Module contents/ /" $filename
    sed -i '' "s/---------------/  /" $filename
    sed -i '' "s/\.\. automodule:: iguanas.$module.$module.$module//" $filename    
    sed -i '' "s/:members:/ /" $filename
    sed -i '' "s/:undoc-members:/ /" $filename
    sed -i '' "s/:show-inheritance:/ /" $filename
    echo ".. include:: ../READMEs/README_$module.rst" >> $filename
done
make clean
make html