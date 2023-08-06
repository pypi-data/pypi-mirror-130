.. -*- mode: rst -*-

|BuildTest|_ |PyPi|_ |License|_ |Downloads|_ |PythonVersion|_

.. |BuildTest| image:: https://travis-ci.com/daniel-yj-yang/treekit.svg?branch=main
.. _BuildTest: https://app.travis-ci.com/github/daniel-yj-yang/treekit

.. |PythonVersion| image:: https://img.shields.io/badge/python-3.8%20%7C%203.9-blue
.. _PythonVersion: https://img.shields.io/badge/python-3.8%20%7C%203.9-blue

.. |PyPi| image:: https://img.shields.io/pypi/v/treekit
.. _PyPi: https://pypi.python.org/pypi/treekit

.. |Downloads| image:: https://pepy.tech/badge/treekit
.. _Downloads: https://pepy.tech/project/treekit

.. |License| image:: https://img.shields.io/pypi/l/treekit
.. _License: https://pypi.python.org/pypi/treekit


=====================================================
Library for Studying and Applying Tree Data Structure
=====================================================

Installation
------------

.. code-block::

   pip install treekit


Sample Usage
------------

>>> from treekit import binarytree
>>> bt1 = binarytree([13, 3, 14, 0, 4, None, None, None, 2, None, 7]) # data array in breadth-first order, see: https://en.wikipedia.org/wiki/Binary_tree#Arrays
>>> bt1.show() # this will create an output.html and open a tab in web browser to view it
>>> bt1.height
3
>>> bt1.inorder # bt.preorder # bt.postorder # bt.levelorder
[0, 2, 3, 4, 7, 13, 14]
>>> bt1.preorder
[13, 3, 0, 2, 4, 7, 14]
>>> bt1.flatten(target="preorder", inplace=True)
>>> bt1.inorder
[13, 3, 0, 2, 4, 7, 14]
>>> bt1.preorder
[13, 3, 0, 2, 4, 7, 14]
>>> bt1.find_maximum_path_sum()
(43, Node(13)

>>> from treekit import tree
>>> t1 = tree()
>>> t1.remove_invalid_parenthese('()())a)b()))')
['((ab()))', '((a)b())', '(()ab())', '(()a)b()', '(())ab()', '()(ab())', '()(a)b()', '()()ab()']

>>> from treekit import bst
>>> bst1 = bst(h=4)
>>> bst1.show()

------------

Screenshot 1: Binary Search Tree, height = 4
--------------------------------------------
|image1|

------------

Screenshot 2: DFS Search Space for Removing Invalid Parentheses
---------------------------------------------------------------
|image2|


.. |image1| image:: https://github.com/daniel-yj-yang/treekit/raw/main/treekit/examples/BST_height=4.png
.. |image2| image:: https://github.com/daniel-yj-yang/treekit/raw/main/treekit/examples/Remove_Invalid_Parentheses.png

