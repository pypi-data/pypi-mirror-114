.. isisysvic3daccess documentation master file, created by
   sphinx-quickstart on Fri Sep 25 10:54:55 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

============================
Documentation of myminions's
============================

*- by David Scheliga*

**My minions** is a loose collection of frequently used methods doing basic
bidding's.

.. image:: ../myminions_icon.png
   :height: 192px
   :width: 192px
   :alt: 3 minions
   :align: center

Indices and tables
==================

* :ref:`genindex`

Installation
============

Either install the current release from pip ...

.. code-block:: shell

   pip install myminions

... or the latest *dev*elopment state of the gitlab repository.

.. code-block:: shell

   $ pip install git+https://gitlab.com/david.scheliga/myminions.git@dev --upgrade

Module content
==============

.. py:currentmodule:: myminions


Helper for testing
------------------

.. autofunction:: myminions.copy_tree

.. autofunction:: myminions.file_trees_have_equal_paths

.. autofunction:: myminions.list_tree_relatively

.. autofunction:: myminions.remove_path_or_tree

.. autofunction:: myminions.testing.assert_existing_rel_paths_within_tree


Saving stuff on Linux and on Windows
------------------------------------
On one occasion changing, editing a text file in between Linux and Windows broke
the parsing with `json` and `yaml`. Originated from the module `dicthandling`
:func:`try_deconding_potential_text_content` is moved to `myminions`.

.. autofunction:: myminions.try_decoding_potential_text_content

.. autofunction:: myminions.load_yaml_file_content

.. autofunction:: myminions.update_yaml_file_content
