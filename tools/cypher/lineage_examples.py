examples = """

1. Lineage of CV Field of CalcView and CVNode with all the element of the path
match Path = (start:CVField {{Name:"StartingCVField", parentCV : "Calc_View", parent_node :"CVNode"}} ) -[:IS_MAPPED*]-(end:DBField) 
UNWIND Nodes(Path) as element
RETURN 
  element.Name as Field, 
  CASE 
    WHEN "DBField" IN labels(element) THEN element.Object
    ELSE element.parent_node 
  END AS Object, 
  CASE 
    WHEN "DBField" IN labels(element) THEN element.Schema
    ELSE element.parentCV
  END AS Source

2. Lineage of CV Starting CV Field of CalcView with all the element of the path
match Path = (start:CVField {{Name:"StartingCVField", parentCV : "Calc_View", parent_node :"Semantics"}} ) -[:IS_MAPPED*]-(end:DBField) 
UNWIND Nodes(Path) as element
RETURN 
  element.Name as Field, 
  CASE 
    WHEN "DBField" IN labels(element) THEN element.Object
    ELSE element.parent_node 
  END AS Object, 
  CASE 
    WHEN "DBField" IN labels(element) THEN element.Schema
    ELSE element.parentCV
  END AS Source

"""
