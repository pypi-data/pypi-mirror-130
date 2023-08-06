Welcome to the Iguanas documentation!
=====================================

.. image:: _static/iguanas_logo.png
   :width: 400px
   :height: 269px 
   :align: center

What is Iguanas?
----------------

Iguanas is a fast, flexible and modular Python package for:

* Generating new fraud-capture rules using a labelled dataset.
* Optimising existing rules using a labelled or unlabelled dataset.
* Combining rule sets and removing/filtering those which are unnecessary.
* Generating rule scores based on their performance.

It aims to help streamline the process for developing a deployment-ready rules-based system (RBS) for **binary classification use cases**.

What are rules and rule-based systems (RBS)?
--------------------------------------------

A **rule** is a set of conditions which, if met, trigger a certain response.​ An example of a rule is one that captures a particular type of fraudulent behaviour for an e-commerce company:

*If the number of transactions made from a given email address in the past 4 hours is greater than 10, reject the transaction.​*

An **RBS** is one that leverages a number of these rules to provide a certain outcome.​

For example, an e-commerce company might employ an RBS to *accept*, *reject* and *review* its transactions.​

The pros and cons of an RBS
---------------------------

As with any approach, there are pros and cons to RBS’s.​

**Pros**

* Rules are intuitive, so the outcome given by the RBS is easy to understand.​​
* RBS’s are flexible, since rules can be quickly added to address new behaviour.​​
* Rules can be built using domain knowledge, which may capture behaviour an ML model would have missed.​​

**Cons**

* Linked to the last pro - domain knowledge is usually required to build rules.​ If you don’t have the domain knowledge, creating rules can be difficult.​
* Generating these rules can be challenging and time consuming, especially if a data-guided approach is used.​
* Difficult to tweak existing rules to address new trends.​

The solution – Iguanas!
-----------------------

Iguanas addresses the cons of an RBS for binary classification problems:​

* Iguanas only requires a historic dataset to generate rules – similar to the requirements of an ML model.​​
* Iguanas quickly and easily generates high performance rules and utilizes an API that is familiar to most data scientists - Sklearn’s fit/transform methology.​
* Iguanas’ rule optimization module allows the user to tweak the thresholds of current rules using a labelled dataset.​
* Iguanas also has a host of other modules which help to streamline the RBS set up process.​

Getting started
---------------

The :ref:`installation.index` section provides instructions on installing Iguanas on your system. Once installed, take a look at the :ref:`examples.index` section for how Iguanas can be used. The :ref:`api.index` section also provides documentation for the classes and methods in each module.

.. toctree::
    :maxdepth: 2
    :hidden:

    install/index
    user_guide/index
    api/index
    examples/index
    about_the_project/index