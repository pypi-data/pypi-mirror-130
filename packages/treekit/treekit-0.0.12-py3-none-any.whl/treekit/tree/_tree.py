# -*- coding: utf-8 -*-

# Author: Daniel Yang <daniel.yj.yang@gmail.com>
#
# License: MIT


from typing import List, Union
from pyvis.network import Network # see also https://visjs.org/
from pathlib import Path
import webbrowser



class TreeNode:
    def __init__(self, val: Union[float, int, str] = None):
        self.val = val
        self.children = []

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


class tree(object):
    def __init__(self, data: List[Union[float, int, str]] = [], *args, **kwargs):
        """
        https://en.wikipedia.org/wiki/Binary_tree#Arrays
        "Binary trees can also be stored in breadth-first order as an implicit data structure in arrays"
        """
        super().__init__(*args, **kwargs)
        self.treetype = 'Tree'
        self.root = None
        
    def __repr__(self) -> str:
        if self.root:
            return f"TreeNode({self.root.val})"

    def remove_invalid_parenthese(self, s: str = '()())a)b()))'):
      """
      https://leetcode.com/problems/remove-invalid-parentheses/
      """
      def DFS(s='', pair=('(', ')'), anomaly_scan_left_range=0, removal_scan_left_range=0, depth=0, parent: TreeNode = None):
        # phase 1: scanning for anomaly
        stack_size = 0
        for index_i in range(anomaly_scan_left_range, len(s)):
            if s[index_i] == pair[0]:
                stack_size += 1
            elif s[index_i] == pair[1]:
                stack_size -= 1
                if stack_size == -1:
                    break
        if stack_size < 0:
            # phase 2: scanning for removal
            for index_j in range(removal_scan_left_range, index_i+1):
                if s[index_j] == pair[1]:
                    if index_j == removal_scan_left_range or s[index_j-1] != pair[1]:
                        new_s = s[:index_j] + s[(index_j+1):len(s)]
                        # add the node - start
                        if pair[0] == '(':
                          curr_node = TreeNode(val=new_s)
                        else:
                          curr_node = TreeNode(val=new_s[::-1])
                        parent.children.append(curr_node)
                        # add the node - end
                        DFS(s=new_s, pair=pair, anomaly_scan_left_range=index_i, removal_scan_left_range=index_j, depth=depth+1, parent=curr_node)
        elif stack_size > 0:
            # phase 3: reverse scanning
            DFS(s=s[::-1], pair=(')', '('), depth=depth, parent=parent)
        else:
          if pair[0] == '(':
              res.append(s)
          else:
              res.append(s[::-1])
      res = []
      self.root = TreeNode(val=s)
      DFS(s=s, pair=('(', ')'), depth=0, parent=self.root)
      self.show(heading='DFS Search Space for Removing Invalid Parentheses')
      return res

    def show(self, filename: str = 'output.html', heading: str = None):
        if not self.root:
            return
        def dfs(parent, level=0):
            if parent.children:
              for child in parent.children:
                g.add_node(child.val, shape="ellipse", level=level+1, title=f"child node of Node({parent.val}), level={level+1}")
                g.add_edge(parent.val, child.val)
                dfs(child, level=level+1)               
        g = Network(width='100%', height='60%')
        g.add_node(self.root.val, shape="ellipse", level=0, title=f"root node of the tree, level=0")
        dfs(parent=self.root)
        if not heading:
          g.heading = f"{self.treetype}"
        else:
          g.heading = heading
        g.set_options("""
var options = {
  "nodes": {
    "font": {
      "size": 20
    }
  },
  "edges": {
    "arrows": {
      "to": {
        "enabled": true
      }
    },
    "color": {
      "inherit": true
    },
    "smooth": false
  },
  "layout": {
    "hierarchical": {
      "enabled": true,
      "sortMethod": "directed"
    }
  },
  "physics": {
    "hierarchicalRepulsion": {
      "centralGravity": 0,
      "springConstant": 0.2,
      "nodeDistance": 150
    },
    "minVelocity": 0.75,
    "solver": "hierarchicalRepulsion"
  },
  "configure": {
      "enabled": true,
      "filter": "layout,physics" 
  }
}""")
        full_filename = Path.cwd() / filename
        g.write_html(full_filename.as_posix())
        webbrowser.open(full_filename.as_uri(), new = 2)
        return g
