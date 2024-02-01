#global var
CUR_TYPE = None
errors = ["error_arith", "error_bool", "error_cmp", "error_und", "error_dmul", "error_unr",
          "error_prm", "error_bnd", "error_dim", "error_sub", "error_rtt", "error_nrt", "error_vrt",
          "error_fnp", "error_prf", "error_npr"]

#
# global_var_dict = {var_name : [var_type, ident_node, array_flag, var_ref_flag],
#                    arr_name : [arr_type, ident_node, array_flag, arr_ref_flag], ...}
global_var_dict = dict()

#
# global_func_dict = {func_name : [func_type, {param_dict}, {local_var_dict}, fdecl_node, fdecl_type, func_ref_flag], ...}
# note the format to store param_dict and local_var_dict is going to be same as global_var_dict
global_func_dict = dict()

#
# stack for function scoping.
global_stack = []

#
# dictionary for array
# array_dict = {array_name : [subscript_type, array_dim, array_type], ....}
array_dict = dict()




def type_checker(node):
  # variables
  global CUR_TYPE
  global global_var_dict
  global global_func_dict
  global array_dict


  #
  # $prog -> $flist, $vlist
  if node.type == "$prog":
    node.real_type = "none"
    node.converted_type = "none"
    vlist = node.children[0]
    flist = node.children[1]

    # global variable and array
    type_checker(vlist)
    # varriable dictionary
    # var_dict = dict()
    var_ref = 0
    for vdecl in vlist.children:
      v_type = vdecl.children[0].children[0]
      ilist = vdecl.children[1]

      for ident in ilist.children:
        v_name = ident.children[0].type
        arr_flag = 0
        if v_name not in global_var_dict:
          if len(ident.children) > 1:
            arr_flag = 1
          global_var_dict[str(v_name)] = [str(v_type), ident, arr_flag, var_ref]
        
        else:
          # global_var_dict[str(v_name)] = [str(v_type), ident, arr_flag, var_ref]
          ident.real_type = "error_dmul"

    
    # functions scoping
    type_checker(flist)

    for v in global_var_dict:
      if global_var_dict[v][3] == 0:
        global_var_dict[v][1].real_type = "error_unr"
    


  # arithmetic operation
  elif node.type == "$add" or node.type == "$sub" or node.type == "$mul" or node.type == "$div":
    op1 = node.children[0]
    op2 = node.children[1]
    type_checker(op1)
    type_checker(op2)

    # setting operand's type
    op1_type = op1.real_type
    op2_type = op2.real_type 

    #getting the result data type from the arithmetic table
    data_type = arith_table(str(op1_type), str(op2_type))

    #setting the data type for $add 
    node.real_type = data_type

    # if $add type is not error 
    if data_type not in errors:
      # if the $add real type is none, then operand's type will stay same as real type
      if data_type == "none":
        op1.converted_type = op1.real_type
      
      # converting type for the operand whichever is not similar to $add datatype
      elif data_type != op1_type:
        op1.converted_type = data_type
      elif data_type != op2_type:
        op2.converted_type = data_type

      # setting the $add converted data_type
      node.converted_type = data_type
    
    # if $add real type is error then the converted type will be none
    else:
      node.converted_type = "none"


  # boolean operation
  elif node.type == "$and" or node.type == "$or":
    op1 = node.children[0]
    op2 = node.children[1]
    type_checker(op1)
    type_checker(op2)

    op1_type = op1.real_type
    op2_type = op2.real_type 

    # getting result type from the boolean table
    data_type = bool_table(str(op1_type), str(op2_type))

    # setting type for the operation node
    node.real_type = data_type
    node.converted_type = data_type

    # changing the data_type to none if the result type is error
    if data_type in errors:
       node.converted_type = "none"

  
  # for relational operation
  elif node.type == "$ge" or node.type == "$gt" or node.type == "$lt" or \
      node.type == "$le" or node.type == "$eq" or node.type == "$ne":
    
    op1 = node.children[0]
    op2 = node.children[1]
    # if str(op1)[0] != "$":
      # op1 = node.children[0].type
      # op2 = node.children[1].type

    type_checker(op1)
    type_checker(op2)

    op1_type = op1.real_type
    op2_type = op2.real_type 

    data_type = comp_table(str(op1_type), str(op2_type))

    node.real_type = data_type

    # if the result type is not error
    if data_type not in errors:
      # if the operands are a combination of float and int, then the converted type will be float
      if op1_type == "float" and op2_type == "int":
        op2.converted_type = "float"
      elif op2_type == "float" and op1_type == "int":
        op1.converted_type = "float"

      # for not error result, the result converted type will be the same
      node.converted_type = data_type

    # setting the converted type to none for error result type
    else:
      node.converted_type = "none"
    
  
  
  # for not operation
  elif node.type == "$not":
    op = node.children[0]

    type_checker(op)

    # operand has to be int
    # if the operand is not int, raising error
    if op.real_type == "int":
      node.real_type = "int"
      node.converted_type = "int"
    elif op.real_type == "float" or op.real_type == "char":
      node.real_type = "error_bool"
      node.converted_type = "none"
    else:
      node.real_type = "none"
      node.converted_type = "none"
      


  # common procedures
  elif node.type == "$vlist" or node.type == "$ilist" or node.type == "$elist"\
      or node.type == "$flist" or node.type == "$plist" or node.type == "$if" or node.type == "$read"\
      or node.type == "$cmpd" or node.type == "$write":
    
    # setting real and converted type to none
    node.real_type = "none"
    node.converted_type = "none"

    # recursively calling type checkers to set their types
    for item in node.children:
      type_checker(item)


  
  # for $fdecl -> ret_type , fname, plist, vlist, cmpd
  elif node.type == "$fdecl":

    ret_type = node.children[0]
    fname = node.children[1].type
    pl = node.children[2]
    vl = node.children[3]
    cmp = node.children[4]

    global_stack.append(str(fname))
    
    type_checker(ret_type)
    # type_checker(fid)
    type_checker(pl)
    type_checker(vl)

    # making a list of parameter types of a function
    type_list = []
    for pdecl in pl.children:
      p_ident = pdecl.children[1]
      ident_type = p_ident.real_type
      # ptype = pdecl.children[0].children[0]
      type_list.append(str(ident_type))

    # adding the types of parameter with an "&" sign in between in a string
    rl_type = ""
    for i in range(len(type_list)):
      if i == len(type_list) - 1:
        rl_type += type_list[i]
      else:
        rl_type += type_list[i]
        rl_type += "&"
    
    # adding the parameter type with the function type with an "->" in between
    rl_type += "->" + str(ret_type.children[0])

    # setting the real and converted type of the function
    node.real_type = rl_type
    node.converted_type = rl_type

    # making a parameter dictionary with the same format as the variable dictionary
    param_dict = dict()
    param_ref = 0
    for pdecl in pl.children:
      param_type = pdecl.children[0].children[0]
      ident = pdecl.children[1]
      param_name = str(ident.children[0])

      if (param_name not in param_dict):
        arr_flag = 0
        if len(ident.children) > 1:
          arr_flag = 1
        
        param_dict[str(param_name)] = [str(param_type), ident, arr_flag, param_ref]
      else:
        ident.real_type = "error_dmul"

    # making a variable dictionary eith the same format as the global variable dictionary
    local_var_dict = dict()
    l_var_ref = 0 

    for vdecl in vl.children:
      var_type = vdecl.children[0].children[0]
      ilist = vdecl.children[1]

      for ident in ilist.children:
        vname = str(ident.children[0])
        
        if (vname not in local_var_dict) and (vname not in param_dict):
          arr_flag = 0
          if len(ident.children) > 1:
            arr_flag = 1
          
          local_var_dict[str(vname)] = [str(var_type), ident, arr_flag, l_var_ref]
      
        else:
          ident.real_type = "error_dmul"
    
    if fname not in global_func_dict:
      global_func_dict[fname] = [str(ret_type.children[0]), param_dict, local_var_dict, node, rl_type, 0]

    else:
      global_func_dict[fname] = [str(ret_type.children[0]), param_dict, local_var_dict, node, rl_type, 0]
      node.real_type = "error_nrt"


    
    type_checker(cmp)
    ret_found = 0
    for state in cmp.children:
      # if a function has return statement
      if str(state.type) == "$ret":
        ret_found = 1
        # if the function return type does not match with the return type
        if global_func_dict[fname][0] != str(state.children[0].real_type):
          state.real_type = "error_rtt"
          state.converted_type = "none"
        # a procedure with a return statement
        if global_func_dict[fname][0] == "void":
          node.real_type = "error_vrt"

    # a funtion with no return statement
    # if ret_found == 0:
    #   if str(global_func_dict[fname][0]) != "void":
    #     node.real_type = "error_nrt"


    # checking if the parameters of the function has been referred or defined
    for p in global_func_dict[fname][1]:
      if global_func_dict[fname][1][p][3] == 0:
        global_func_dict[fname][1][p][1].real_type = "error_unr"
    
    # checking if the local variables of the function has been referred or defined
    for p in global_func_dict[fname][2]:
      if global_func_dict[fname][2][p][3] == 0:
        global_func_dict[fname][2][p][1].real_type = "error_unr"


    # removing the last function
    global_stack.pop()

       

  elif node.type == "$ident":
    # setting real and converted type of a variable
    node.real_type = CUR_TYPE 
    node.converted_type = CUR_TYPE
    var_name = node.children[0]
    

    # if $ident has more than 1 children, that implies that it is an array
    if len(node.children) >1:
      # array type
      array_type = node.real_type
      con = node.children[1].type
      type_checker(con)

      # array dimention and subscript type
      array_dim = con.children[0]
      subs_type = con.real_type
      
      # for int subscript type 
      if str(subs_type) == "int":
        node.real_type = str(node.real_type) + "[" + str(con.children[0]) + "]"
        node.converted_type = node.real_type
        # storing the array name with a list of subscript type, array dimention and array type
        array_dict[str(var_name)] = [str(subs_type), str(array_dim), array_type]

      # for char subscript type
      elif str(subs_type) == "char":
        subs_char_dim = ord(str(con.children[0])[1])
        node.real_type = str(node.real_type) + "[" + str(subs_char_dim) + "]"
        node.converted_type = node.real_type
        array_dict[str(var_name)] = [str(subs_type), str(subs_char_dim), array_type]

    
 
  elif node.type == "$vardef" or node.type == "$varref":
    id = str(node.children[0])   
    
    #function scope
    func = global_stack[-1]

    # checking if the variable is in the local variable of the current function
    if id in global_func_dict[func][2]:
      # raising var_ref flag
      global_func_dict[func][2][id][3] = 1
      # setting real_type and converted_type
      node.real_type = global_func_dict[func][2][id][0]
      node.converted_type = global_func_dict[func][2][id][0]
      # checking if the non-array local_variable is calling an array
      if global_func_dict[func][2][id][2] == 1:
        node.real_type = "error_sub"
        node.converted_type = "none"

    # checking if the variable is in the parameter of the current function
    elif id in global_func_dict[func][1]:
      #raising flag
      global_func_dict[func][1][id][3] = 1
      # setting real_type and converted_type
      node.real_type = global_func_dict[func][1][id][0]
      node.converted_type = global_func_dict[func][1][id][0]
      # checking if the non-array parameter is calling an array
      if global_func_dict[func][1][id][2] == 1:
        node.real_type = "error_dim"
        node.converted_type = "none"

    # checking if the variable in the global variable dictionary
    elif str(id) in global_var_dict:
      global_var_dict[id][3] = 1
      # setting real_type and converted_type
      node.real_type = global_var_dict[id][0]
      node.converted_type = global_var_dict[id][0]
      # if it is a global variable, checking if a variable is calling an array
      if global_var_dict[id][2] == 1:
        node.real_type = "error_dim"
        node.converted_type = "none"
    

    # else the variable is undeclared
    else:
      node.real_type = "error_und"
      node.converted_type = "none"
       


  elif node.type == "$pdecl":
    node.real_type = "none"
    node.converted_type = "none"
    #processing $type
    dtype = type_checker(node.children[0])
    CUR_TYPE = dtype
    # processing $ident
    ident = node.children[1]
    type_checker(ident)
    


  elif node.type == "$vdecl":
    node.real_type = "none"
    node.converted_type = "none"

    ilist = node.children[1]
    #processing $type
    dtype = node.children[0]
    type_checker(node.children[0])
    CUR_TYPE = dtype.children[0]

    # processing $ilist
    type_checker(node.children[1])
    
    


  elif node.type == "$type":
    node.real_type = "none"
    node.converted_type = "none"
    return node.children[0]



  elif node.type == "$assign":
    node.real_type = "none"
    node.converted_type = "none"

    loper = node.children[0]
    roper = node.children[1]
    type_checker(loper)
    type_checker(roper)

    if str(roper.real_type) in errors:
      loper.converted_type = "none"

    elif roper.real_type == "none":
      roper.converted_type = "none"
      # pass
    elif str(loper.real_type) in errors:
      roper.converted_type = "none"
    else:
      roper.converted_type = loper.real_type



  elif node.type == "$fcall":
    func_name = node.children[0]
    elist = node.children[1]
    type_checker(elist)
    current_func = global_stack[-1]

    if func_name in global_func_dict:
      if global_func_dict[func_name][0] == "void":
        node.real_type = "error_fnp"
        node.converted_type = "none"
      
      else:
        fcall_type = ""
        i = 0
        elist_len = len(elist.children)
        for e_child in elist.children:
          if e_child.type == "$varref" or e_child.type == "$vardef":
            var_name = e_child.children[0]
            if var_name in global_var_dict:
              e_child.real_type = global_var_dict[var_name][1].real_type
              e_child.converted_type = e_child.real_type
              if i == elist_len - 1:
                fcall_type += str(e_child.real_type)
              else:
                fcall_type += str(e_child.real_type)
                fcall_type += "&"

            elif var_name in global_func_dict[current_func][1]:
              e_child.real_type = global_func_dict[current_func][1][var_name][1].real_type
              e_child.converted_type = e_child.real_type
              if i == elist_len - 1:
                fcall_type += str(e_child.real_type)
              else:
                fcall_type += str(e_child.real_type) + "&"
            
            elif var_name in global_func_dict[current_func][2]:
              e_child.real_type = global_func_dict[current_func][2][var_name][1].real_type
              e_child.converted_type = e_child.real_type
              if i == elist_len - 1:
                fcall_type += str(e_child.real_type)
              else:
                fcall_type += e_child.real_type
                fcall_type += "&"

            else:
              e_child.real_type = "error_und"
              e_child.converted_type = "none"
          
          else:
            if i == elist_len - 1:
              fcall_type += e_child.real_type
            else:
              fcall_type += e_child.real_type
              fcall_type += "&"
          i += 1

        fcall_type += "->" + global_func_dict[func_name][0]

        node.real_type = global_func_dict[func_name][0]
        node.converted_type = node.real_type     

    else:
      node.real_type = "error_fnp"
      node.converted_type = "none"
      if func_name in global_var_dict:
        node.real_type = "error_nfn"
        node.converted_type = "none"
        global_var_dict[func_name][3] = 1
    
    if func_name in global_func_dict and global_func_dict[func_name][0] != "void":
      fdecl_type = global_func_dict[func_name][4]
      
      if fcall_type != fdecl_type:
        node.real_type = "error_prm"
        node.converted_type = "none"
    



  elif node.type == "$pcall":
    proc_name = node.children[0]
    elist = node.children[1]
    type_checker(elist)

    node.real_type = "void"
    node.converted_type = "void"
    
    if proc_name not in global_func_dict: 
      node.real_type = "error_npr"
      node.converted_type = "none"
      if proc_name in global_var_dict:
        global_var_dict[proc_name][3] = 1

    else:
      if global_func_dict[proc_name][0] != "void":
        node.real_type = "error_prf"
        node.converted_type = "none"
        for con in elist.children:
          if con.type == "$varref":
            con.real_type = global_func_dict[proc_name][1][con.children[0]][1].real_type
            con.converted_type = con.real_type
      
      else:
        fdecl_type = global_func_dict[proc_name][4]
        pcall_type = ""
        elist_len = len(elist.children)
        for con in elist.children:
          if elist_len > 1:
            pcall_type += str(con.real_type) + "&"
          else:
            pcall_type += str(con.real_type)
          elist_len -= 1
        pcall_type += "->void"
        if str(fdecl_type) != pcall_type:
          node.real_type = "error_prm" 
          node.converted_type = "none"


    
  
  elif node.type == "$arrayref" or node.type == "$arraydef":
    arr_name = node.children[0]
    con = node.children[1]
    type_checker(con)

    # current funtion scope
    current_func = global_stack[-1]

    # array within the scope
    # if array is found in the right scope it is going to change into 1
    arr_found = 0

    if con.type != "$varref":
      # checking if the array is in the local function variable
      if arr_name in global_func_dict[current_func][2]:
        # raising var_ref flag
        global_func_dict[current_func][2][arr_name][3] = 1
        if global_func_dict[current_func][2][arr_name][2] == 1:
          node.real_type = array_dict[arr_name][2]
          node.converted_type = node.real_type
          arr_found = 1
        else:
          node.real_type = "error_dim"
          node.converted_type = "none"

      # checking if the array is in the local function parameter
      elif arr_name in global_func_dict[current_func][1]:
        # raising var_ref flag
        global_func_dict[current_func][1][arr_name][3] = 1
        if global_func_dict[current_func][1][arr_name][2] == 1:
          node.real_type = array_dict[arr_name][2]
          node.converted_type = node.real_type
          arr_found = 1
        else:
          node.real_type = "error_dim"
          node.converted_type = "none"

      # checking if the array is in global_var_dict
      elif arr_name in global_var_dict:
        # raising var_ref flag
        global_var_dict[arr_name][3] = 1
        # checking if the array_flag is 1 or not
        if global_var_dict[arr_name][2] == 1:
          node.real_type = array_dict[arr_name][2]
          node.converted_type = node.real_type
          arr_found = 1
        else:
          node.real_type = "error_dim"
          node.converted_type = "none"
          
      else:
        node.real_type = "error_und"
        node.converted_type = "none"
    
    else:
      if con.real_type in errors:
        node.real_type = "error_sub"
        node.converted_type = "none"
      elif arr_name in array_dict:
        node.real_type = array_dict[arr_name][2]
        node.converted_type = node.real_type
        # raising referrence flag
        if arr_name in global_func_dict[current_func][2]:
          global_func_dict[current_func][2][arr_name][3] = 1
        elif arr_name in global_func_dict[current_func][1]:
          global_func_dict[current_func][1][arr_name][3] = 1
        elif arr_name in global_var_dict:
          global_var_dict[arr_name][3] = 1
        

      elif arr_name not in array_dict:
        node.real_type = "error_und"
        node.converted_type = "none"
    
    if arr_name in global_func_dict[current_func][2]:
      if global_func_dict[current_func][2][arr_name][2] == 1:
        arr_found = 1
    elif arr_name in global_func_dict[current_func][1] :
      if global_func_dict[current_func][1][arr_name][2] == 1:
        arr_found = 1
    elif arr_name in global_var_dict:
      if global_var_dict[arr_name][2] == 1:
        arr_found = 1

    if (arr_found == 1):      
      # if the con real type is int
      if con.real_type == "int": 
        # checking if the input array dimention is in the range of (0 - declared dim) 
        # if not, gives the correct error
        if type(con.children[0]) == "int":
          if int(con.children[0]) < 0 or int(con.children[0]) >= int(array_dict[arr_name][1]):
            node.real_type = "error_bnd"
            node.converted_type = "none"
      
      # if constant type is char
      elif str(con.real_type) == "char":
        if str(con.children[0][0]) == "'":
          char_id = ord(str(con.children[0])[1])-96
        else:
          char_id = ord(str(con.children[0]))-96

        # if the subscript is out of range
        if char_id < 0 or char_id >= int(array_dict[arr_name][1]):
          node.real_type = "error_bnd"
          node.converted_type = "none"
        # changing converted type for char to int    
        con.converted_type = "int"

      else:
        if str(con.children[0]) != array_dict[arr_name][1]:
          node.real_type = "error_bnd"
          node.converted_type = "none"

      # if the constant type is not equal to the subscript type
      if str(con.real_type) != array_dict[arr_name][0]:
        node.real_type = "error_sub"
        node.converted_type = "none"
      


  elif node.type == "$while":
    node.real_type = "none"
    node.converted_type = "none"
    
    for item in node.children:
      type_checker(item)
    
    node.children[0].converted_type = "int"




  elif node.type == "$ret":
    node.real_type = "none"
    node.converted_type = "none"
    vref = node.children[0]
    type_checker(vref)
    func_name = global_stack[-1]
    global_func_dict[func_name][5] = 1

    

  elif node.type == "$fcon":
    node.real_type = "float"
    node.converted_type = "float"

  elif node.type == "$str":
    node.real_type = "str"
    node.converted_type = "str"
  
  elif node.type == "$ccon":
    node.real_type = "char"
    node.converted_type = "char"
    
  elif node.type == "$icon":
    node.real_type = "int"
    node.converted_type = "int"

  













def arith_table(op1, op2):
    key = (op1, op2)
    table = {
    ('int', 'int'): 'int',
    ('float', 'float'): 'float',
    ('char', 'char'): 'char',
    # int, float combination
    ('int', 'float'): 'float',
    ('float', 'int'): 'float',
    #int, char combination
    ('char', 'int'): 'int',
    ('int', 'char'): 'int',
    # char, float combination
    ('char', 'float'): 'error_arith',
    ('float', 'char'): 'error_arith'
    }

    if key in table:
        return table[key]
    else:
      return "none"
    

def bool_table(op1, op2):
    key = (op1, op2)
    table = {
    ('int', 'int'): 'int',
    ('float', 'float'): 'int',
    ('char', 'char'): 'int',
    # int, float combination
    ('int', 'float'): 'int',
    ('float', 'int'): 'int',
    # char, int combination
    ('char', 'int'): 'error_bool',
    ('int', 'char'): 'error_bool',
    # float, char combination
    ('char', 'float'): 'error_bool',
    ('flaot', 'char'): 'error_bool'
    }

    if key in table:
        return table[key] 
    else:
      return "none"

def comp_table(operand1, operand2):
    key = (operand1, operand2)
    table = {
    ('int', 'int'): 'int',
    ('float', 'float'): 'int',
    ('char', 'char'): 'int',
    # int, float comb
    ('int', 'float'): 'int',
    ('float', 'int'): 'int',
    # char, int comb
    ('char', 'int'): 'error_cmp',
    ('int', 'char'): 'error_cmp',
    #char, floar comb
    ('char', 'float'): 'error_cmp',
    ('float', 'char'): 'error_cmp',
    # Add rules for other comparison operators
    }

    if key in table:
        return table[key]
    else:
      return "none"
    