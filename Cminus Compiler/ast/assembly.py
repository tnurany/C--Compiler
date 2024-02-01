assembly = ""
head = ""
offset = dict()
offset_count = 8
label_count = 0
float_var = 0
string_var = 0
registers = {"rbx": [True, None, None], "rcx": [True, None, None], "rdx": [True, None, None], "rsi": [True, None, None],
             "rdi": [True, None, None], "r8": [True, None, None], "r9": [True, None, None], "xmm0": [True, None, None],
             "xmm1": [True, None, None], "xmm2": [True, None, None], "xmm3": [True, None, None], "xmm4": [True, None, None],
             "xmm5": [True, None, None], "xmm6": [True, None, None], "xmm7": [True, None, None], "rax": [True, None, None]}

alignment = 16

global_var = []
global_var_dict = dict()
func_dict = dict()
global_stack = [] 
current_func = None   


def expr(node):
  global assembly
  global head
  global alignment
  global registers
  global offset
  global offset_count
  global float_var
  global string_var
  global global_var
  global label_count
  global global_var_dict
  global func_dict
  global global_stack
  global current_func
  fr_order = ["xmm0", "xmm1", "xmm2", "xmm3", "xmm4", "xmm5", "xmm6", "xmm7"]
  r_order = ["rcx", "r8", "r9","rsi", "rdi", "rdx", "rbx", "rax"]

  #
  # $prog -> $flist, $vlist
  if node.type == "$prog":
    
    vlist = node.children[0]
    flist = node.children[1]
    expr(vlist)

    # storing global variables
    for vdecl in vlist.children:
        v_type = str(vdecl.children[0].children[0])
        ilist = vdecl.children[1]
        v_offset = 0
        if v_type == "int":
            for ident in ilist.children:
                id = str(ident.children[0])
                global_var.append(id)
                if len(ident.children) == 1:
                    offset[id] = offset_count
                    offset_count += 8
                    # alignment += 8
                    v_offset += 8
                    head += f".comm {id}, 8, 8\n"
                else:
                    con = ident.children[1].type
                    if str(con.real_type) == "int":
                        arr_dim = int(con.children[0])
                    elif str(con.real_type) == "char":
                        arr_dim = int(ord(str(con.children[0])[1])) -96
                    v_offset += 8 * arr_dim
                    offset_count += 8 * arr_dim
                    offset[id] = offset_count -8
                    alignment += 8 * arr_dim
                    head += f".comm {id}, {8*arr_dim}, {8*arr_dim}\n"
        
        elif v_type == "float":
            for ident in ilist.children:
                id = str(ident.children[0])
                global_var.append(id)
                if len(ident.children) == 1:
                    offset[id] = offset_count
                    offset_count += 8
                    # alignment += 8
                    v_offset += 8
                    head += f".comm {id}, 8, 8\n"
                else:
                    con = ident.children[1].type
                    if str(con.real_type) == "int":
                        arr_dim = int(con.children[0])
                    elif str(con.real_type) == "char":
                        arr_dim = int(ord(str(con.children[0])[1])) -96
                    v_offset += 8 * arr_dim
                    offset_count += 8 * arr_dim
                    offset[id] = offset_count -8
                    alignment += 8 * arr_dim
                    head += f".comm {id}, {8*arr_dim}, {8*arr_dim}\n"
    
        elif v_type == "char":
            for ident in ilist.children:
                id = str(ident.children[0])
                global_var.append(id)
                if len(ident.children) == 1:
                    offset[id] = offset_count
                    offset_count += 8
                    # alignment += 8
                    v_offset += 8
                    head += f".comm {id}, 8, 8\n"
                else:
                    con = ident.children[1].type
                    if str(con.real_type) == "int":
                        arr_dim = int(con.children[0])
                    elif str(con.real_type) == "char":
                        arr_dim = int(ord(str(con.children[0])[1])) -96
                    v_offset += 8 * arr_dim
                    offset_count += 8 * arr_dim
                    offset[id] = offset_count -8
                    alignment += 8 * arr_dim
                    head += f".comm {id}, {8*arr_dim}, {8*arr_dim}\n"
              
    expr(flist)


  # arithmetic operation for add and sub
  elif node.type == "$add" or node.type == "$sub":
    if node.type == "$add":
      operation = "addq"
      operation_float = "addss"
    elif node.type == "$sub":
      operation = "subq"
      operation_float = "subss"
    
    loper = node.children[0]
    roper = node.children[1]
     
    reg1 = expr(loper)
    reg2 = expr(roper)

    # if the left operand real_type int and converted_type is float, we will convert it to float
    if loper.real_type == "int" and loper.converted_type == "float":
      #converting the int to float
      for r in fr_order:
        if registers[r][0] == True:
          registers[r][0] = False
          assembly += f"\tpxor %{r}, %{r}\n"
          assembly += f"\tcvtsi2ss %{reg1}, %{r}\n"
          registers[reg1][0] = True
          reg1 = r
          break
    # if the right operand real_type int and converted_type is float, we will convert it to float
    if roper.real_type == "int" and roper.converted_type == "float":
      #converting the int to float
      for r in fr_order:
        if registers[r][0] == True:
          registers[r][0] = False
          assembly += f"\tpxor %{r}, %{r}\n"
          assembly += f"\tcvtsi2ss %{reg2}, %{r}\n"
          registers[reg2][0] = True
          reg2 = r
          break

  
    if str(node.real_type) == "int":
       assembly += f"\t{operation} %{reg2}, %{reg1}\n"
       registers[reg2][0] = True
       return reg1
  
    elif str(node.real_type) == "float":
      assembly += f"\t{operation_float} %{reg2}, %{reg1}\n"
      registers[reg2][0] = True
      if str(node.converted_type) == "int":
        for r in r_order:
          if registers[r][0] == True:
            registers[r][0] = False
            assembly += f"\tcvttss2si %{reg1}, %{r}\n"
            registers[reg1][0] = True
            reg1 = r
            break
      return reg1

    elif str(node.real_type) == "char":
      assembly += f"\t{operation} %{reg2}, %{reg1}\n"
      registers[reg2][0] = True
      return reg1
  
  # arithmetic mul and div operation for int and float
  elif node.type == "$div" or node.type == "$mul":
    if node.type == "$div":
      operation = "idivq"
      operation_float = "divss"
    elif node.type == "$mul":
      operation = "imulq"
      operation_float = "mulss"

    loper = node.children[0]
    roper = node.children[1]
    
    reg1 = expr(loper)
    reg2 = expr(roper)
    if loper.real_type == "int" and loper.converted_type == "float":
      #converting the int to float
      for r in fr_order:
        if registers[r][0] == True:
          registers[r][0] = False
          assembly += f"\tpxor %{r}, %{r}\n"
          assembly += f"\tcvtsi2ss %{reg1}, %{r}\n"
          registers[reg1][0] = True
          reg1 = r
          break

    if roper.real_type == "int" and roper.converted_type == "float":
      #converting the int to float
      for r in fr_order:
        if registers[r][0] == True:
          registers[r][0] = False
          assembly += f"\tpxor %{r}, %{r}\n"
          assembly += f"\tcvtsi2ss %{reg2}, %{r}\n"
          registers[reg2][0] = True
          reg2 = r
          break
    
    if node.real_type == "int":
      assembly += f"\tmovq %{reg1}, %rax\n"
      assembly += f"\tcltd\n"
      assembly += f"\t{operation} %{reg2}\n"
      registers[reg1][0] = True
      registers[reg2][0] = True
      return "rax"

    elif str(node.real_type) == "float":
      assembly += f"\t{operation_float} %{reg2}, %{reg1}\n"
      registers[reg2][0] = True
      if str(node.converted_type) == "int":
        for r in r_order:
          if registers[r][0] == True:
            registers[r][0] = False
            assembly += f"\tcvttss2si %{reg1}, %{r}\n"
            registers[reg1][0] = True
            reg1 = r
            break
      return reg1


  # and and or operation for int and float
  elif node.type == "$and" or node.type == "$or":
    if node.type == "$and":
      operation = "and"
    elif node.type == "$or":
      operation = "or"
    loper = node.children[0]
    roper = node.children[1]
    
    reg1 = expr(loper)
    reg2 = expr(roper)

    if str(loper.real_type) == "float":
      for r in r_order:
        if registers[r][0] == True:
          registers[r][0] = False
          assembly += f"\tcvttss2si %{reg1}, %{r}\n"
          registers[reg1][0] = True
          reg1 = r
          break
    if str(roper.real_type) == "float":
      for r in r_order:
        if registers[r][0] == True:
          registers[r][0] = False
          assembly += f"\tcvttss2si %{reg2}, %{r}\n"
          registers[reg2][0] = True
          reg2 = r
          break
      
    assembly += f"\t{operation} %{reg2}, %{reg1}\n"
    registers[reg2][0] = True
    return reg1


  # logical not operation for int and float
  elif node.type == "$not":
    reg = expr(node.children[0])
    assembly += f"\tnot %{reg}\n"
    return reg


  # logical operation for int and float
  elif node.type == "$lt" or node.type == "$le" or node.type == "$gt" or node.type == "$ge" or node.type == "$eq" or node.type == "$ne":
    if node.type == "$lt":
      operation = "setl"
    elif node.type == "$le":
      operation = "setle"
    elif node.type == "$gt":
      operation = "setg"
    elif node.type == "$ge":
      operation = "setge"
    elif node.type == "$eq":
      operation = "sete"
    elif node.type == "$ne":
      operation = "setne"

    loper = node.children[0]
    roper = node.children[1]

    reg1 = expr(loper)
    reg2 = expr(roper)


    if str(loper.real_type) == "float":
      for r in r_order:
        if registers[r][0] == True:
          registers[r][0] = False
          assembly += f"\tcvttss2si %{reg1}, %{r}\n"
          registers[reg1][0] = True
          reg1 = r
          break
    if str(roper.real_type) == "float":
      for r in r_order:
        if registers[r][0] == True:
          registers[r][0] = False
          assembly += f"\tcvttss2si %{reg2}, %{r}\n"
          registers[reg2][0] = True
          reg2 = r
          break

    if node.real_type == "int":
      assembly += f"\txor %rax, %rax\n"
      assembly += f"\tcmpq %{reg2}, %{reg1}\n"
      assembly += f"\t{operation} %al\n"
      assembly += f"\tmovzbq %al, %rax\n"
      registers[reg2][0] = True
      registers[reg1][0] = True
      return "rax"
    
    elif node.real_type == "float":
      assembly += f"\txor %rax, %rax\n"
      assembly += f"\tcomiss %{reg2}, %{reg1}\n"
      assembly += f"\t{operation} %al\n"
      assembly += f"\tmovzbq %al, %rax\n"
      registers[reg2][0] = True
      registers[reg1][0] = True
      return "rax"
 

  
  # scan operation for int, float and char
  elif node.type == "$read":
    id = expr(node.children[0])

    if id in global_var:
      if node.children[0].real_type == "int":
        assembly += f"\tleaq {id}(%rip), %rsi\n"
        assembly += f"\tleaq .int_rformat(%rip), %rdi\n"
        assembly += f"\tmovq $0, %rax\n"
        if alignment % 16 != 0:
          mod = 16 - (alignment % 16)
          assembly += f"\tsub ${mod}, %rsp\n"
          alignment += mod
        assembly += f"\tcall scanf\n"
      
      elif node.children[0].real_type == "float":
        assembly += f"\tleaq {id}(%rip), %rsi\n"
        assembly += f"\tleaq .float_rformat(%rip), %rdi\n"
        assembly += f"\tmovq $0, %rax\n"
        if alignment % 16 != 0:
          mod = 16 - (alignment % 16)
          assembly += f"\tsub ${mod}, %rsp\n"
          alignment += mod
        assembly += f"\tcall scanf\n"

      elif node.children[0].real_type == "char":
        assembly += f"\tleaq {id}(%rip), %rsi\n"
        assembly += f"\tleaq .char_rformat(%rip), %rdi\n"
        assembly += f"\tmovq $0, %rax\n"
        if alignment % 16 != 0:
          mod = 16 - (alignment % 16)
          assembly += f"\tsub ${mod}, %rsp\n"
          alignment += mod
        assembly += f"\tcall scanf\n"
    else:
      ofs = func_dict[current_func][id]
      # if the variable is an int, we will use the int_rformat
      if node.children[0].real_type == "int":
        assembly += f"\tleaq -{ofs}(%rbp), %rsi\n"
        assembly += f"\tleaq .int_rformat(%rip), %rdi\n"
        assembly += f"\tmovq $0, %rax\n"
        if alignment % 16 != 0:
          mod = 16 - (alignment % 16)
          assembly += f"\tsub ${mod}, %rsp\n"
          alignment += mod
        assembly += f"\tcall scanf\n"
      
      # if the variable is a float, we will use the float_rformat
      elif node.children[0].real_type == "float":
        assembly += f"\tleaq -{ofs}(%rbp), %rsi\n"
        assembly += f"\tleaq .float_rformat(%rip), %rdi\n"
        assembly += f"\tmovq $0, %rax\n"
        if alignment % 16 != 0:
          mod = 16 - (alignment % 16)
          assembly += f"\tsub ${mod}, %rsp\n"
          alignment += mod
        assembly += f"\tcall scanf\n"

      # if the variable is a char, we will use the char_rformat
      elif node.children[0].real_type == "char":
        assembly += f"\tleaq -{ofs}(%rbp), %rsi\n"
        assembly += f"\tleaq .char_rformat(%rip), %rdi\n"
        assembly += f"\tmovq $0, %rax\n"
        if alignment % 16 != 0:
          mod = 16 - (alignment % 16)
          assembly += f"\tsub ${mod}, %rsp\n"
          alignment += mod
        assembly += f"\tcall scanf\n"


  elif node.type == "$fdecl":
    func_type = node.children[0]
    func_name = str(node.children[1])
    plist = node.children[2]
    vlist = node.children[3]
    cmpd = node.children[4]

    current_func = func_name
    offset_count = 8

    assembly += f"\t.text\n"
    assembly += f"\t.globl {func_name}\n"
    assembly += f"\t.type {func_name}, @function\n"
    assembly += f"{func_name}:\n"
    assembly += f"\tpushq %rbp\n"
    assembly += f"\tmovq %rsp, %rbp\n"
    # assembly += f"\tsubq $8, %rsp\n"

    var_dict = dict()
    offset_sum = 0
    
    # parameters of the function
    p_len = len(plist.children)
    assembly += f"\tsubq ${8*p_len}, %rsp\n"
    alignment += 8*p_len
    int_reg = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
    float_reg = ["xmm0", "xmm1", "xmm2", "xmm3", "xmm4", "xmm5", "xmm6", "xmm7"]
    i = 0
    for pdecl in plist.children:
      param_type = str(pdecl.children[0].children[0])
      ident = pdecl.children[1]
      id = str(ident.children[0])
      if param_type == "int":
        assembly += f"\tmovq %{int_reg[i]}, -{offset_count}(%rbp)\n"
      elif param_type == "float":
        assembly += f"\tmovss %{float_reg[i]}, -{offset_count}(%rbp)\n"
      var_dict[id] = offset_count
      # offset[id] = offset_count
      offset_count += 8
      offset_sum += 8
      i += 1

    func_dict[func_name] = var_dict

    



    expr(vlist)
    
    # storing the local variables
    for vdecl in vlist.children:
      v_type = str(vdecl.children[0].children[0])
      ilist = vdecl.children[1]

      # total offset per variable type
      v_offset = 0

      if v_type == "int":
        for ident in ilist.children:
          id = str(ident.children[0])
          var_dict[id] = offset_count
          if len(ident.children) == 1:
            # offset[id] = offset_count
            var_dict[id] = offset_count
            offset_count += 8
            alignment += 8
            v_offset += 8
          else:
            con = ident.children[1].type
            if str(con.real_type) == "int":
              arr_dim = int(con.children[0])
            elif str(con.real_type) == "char":
              arr_dim = int(ord(str(con.children[0])[1])) -96
            v_offset += 8 * arr_dim
            offset_count += 8 * arr_dim
            offset[id] = offset_count -8
            var_dict[id] = offset_count -8
            alignment += 8 * arr_dim
        assembly += f"\tsubq ${v_offset}, %rsp\n"

      elif v_type == "float":
        for ident in ilist.children:
          id = str(ident.children[0])
          var_dict[id] = offset_count
          if len(ident.children) == 1:
            var_dict[id] = offset_count
            # offset[id] = offset_count
            offset_count += 8
            alignment += 8
            v_offset += 8
          else:
            con = ident.children[1].type
            if str(con.real_type) == "int":
              arr_dim = int(con.children[0])
            elif str(con.real_type) == "char":
              arr_dim = int(ord(str(con.children[0])[1])) -96
            v_offset += 8 * arr_dim
            offset_count += 8 * arr_dim
            # offset[id] = offset_count -8
            var_dict[id] = offset_count -8
            alignment += 8 * arr_dim
        assembly += f"\tsubq ${v_offset}, %rsp\n"


      elif v_type == "char":
        for ident in ilist.children:
          id = str(ident.children[0])
          func_dict[func_name].append(id)
          if len(ident.children) == 1:
            # offset[id] = offset_count
            var_dict[id] = offset_count
            offset_count += 8
            alignment += 8
            v_offset += 8
          else:
            con = ident.children[1].type
            if str(con.real_type) == "int":
              arr_dim = int(con.children[0])
            elif str(con.real_type) == "char":
              arr_dim = int(ord(str(con.children[0])[1])) -96
            v_offset += 8 * arr_dim
            offset_count += 8 * arr_dim
            # offset[id] = offset_count -8
            var_dict[id] = offset_count -8
            alignment += 8 * arr_dim
        assembly += f"\tsubq ${v_offset}, %rsp\n"


    # fixing alignment
    if alignment % 16 != 0:
      mod = 16 - (alignment % 16)
      assembly += f"\tsubq ${mod}, %rsp\n"
      alignment += mod
  
    expr(cmpd)

    # fixing alignment
    if alignment % 16 != 0:
      mod = 16 - (alignment % 16)
      assembly += f"\tsubq ${mod}, %rsp\n"
      alignment += mod

    assembly += f"\tleave\n"
    assembly += f"\tret\n"
      
  # common procedures
  elif node.type == "$vlist" or node.type == "$ilist"\
        or node.type == "$flist" or node.type == "$plist" or node.type == "$read"\
        or node.type == "$cmpd" or node.type == "$vdecl"\
        or node.type == "$ident":
    for child in node.children:
      expr(child)

  # function call
  elif node.type == "$fcall" or node.type == "$pcall":
    func_name = node.children[0]
    elist = node.children[1]
    expr(elist)
    reg_list = []
    for r in registers:
      if registers[r][0] == False:
        if r in ["xmm0", "xmm1", "xmm2", "xmm3", "xmm4", "xmm5", "xmm6", "xmm7"]:
          continue
        if r == "rsp" or r == "rbp":
          continue
        reg_list.append(r)
        assembly += f"\tpushq %{r}\n"
        alignment += 8
    
    #alignment
    align_done = False
    if alignment % 16 != 0:
      mod = 16 - (alignment % 16)
      assembly += f"\tsubq ${mod}, %rsp\n"
      alignment += mod
      align_done = True

    assembly += f"\tcall {func_name}\n"
    if node.real_type == "int":
      for reg in r_order:
        if registers[reg][0] == True:
          registers[reg][0] = False
          assembly += f"\tmovq %rax, %{reg}\n"
          break
    elif node.real_type == "float":
      for reg in fr_order:
        if registers[reg][0] == True:
          registers[reg][0] = False
          assembly += f"\tmovss %xmm0, %{reg}\n"
          break
    
    if align_done:
      assembly += f"\taddq $8, %rsp\n"
      alignment -= 8

    for r in reversed(reg_list):
      assembly += f"\tpopq %{r}\n"
      alignment -= 8
    

    if node.type == "$fcall":
      return reg
    

  elif node.type == "$elist":
    int_reg = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
    float_reg = ["xmm0", "xmm1", "xmm2", "xmm3", "xmm4", "xmm5", "xmm6", "xmm7"]
    i = 0
    for child in node.children:
      reg = expr(child)
      # print(reg)
      
      if str(child.converted_type) == "float":
        assembly += f"\tmovss %{reg}, %{float_reg[i]}\n"
      elif str(child.converted_type) == "int":
        assembly += f"\tmovq %{reg}, %{int_reg[i]}\n"
      elif str(child.converted_type) == "char":
        assembly += f"\tmovq %{reg}, %{int_reg[i]}\n"
      registers[reg][0] = True
      i += 1

  elif node.type == "$assign":
    # if node.children[0] == "$vardef":
    verdef = node.children[0]
    con = node.children[1]
    reg = expr(con)
    
    if verdef.type == "$vardef":
      id = expr(verdef)
      if str(con.real_type) == "int" and str(con.converted_type) == "float":
        #converting the int to float
        for r in fr_order:
          if registers[r][0] == True:
            registers[r][0] = False
            assembly += f"\tpxor %{r}, %{r}\n"
            assembly += f"\tcvtsi2ss %{reg}, %{r}\n"
            registers[reg][0] = True
            reg = r
            break
      
      if str(con.real_type) == "float" and str(con.converted_type) == "int":
        #converting the float to int
        for r in r_order:
          if registers[r][0] == True:
            registers[r][0] = False
            assembly += f"\tcvttss2si %{reg}, %{r}\n"
            registers[reg][0] = True
            reg = r
            break

      # if id is a global variable
      if id in global_var:
        if str(verdef.real_type) == "float":
          assembly += f"\tmovss %{reg}, {id}(%rip)\n"
        elif str(verdef.real_type) == "int":
          assembly += f"\tmovq %{reg}, {id}(%rip)\n"
        
      else:
        ofs = func_dict[current_func][id]
        if str(verdef.real_type) == "float":
          assembly += f"\tmovss %{reg}, -{ofs}(%rbp)\n"
        # assembly += f"\tmovq ${registers[reg][1]}, {reg}\n"
        elif str(verdef.real_type) == "int":
          assembly += f"\tmovq %{reg}, -{ofs}(%rbp)\n"
        elif str(verdef.real_type) == "char":
          assembly += f"\tmovq %{reg}, -{ofs}(%rbp)\n"
      
      registers[reg][0] = True

    elif verdef.type == "$arraydef":
      id, dim_reg = expr(verdef)
      ofs = func_dict[current_func][id]

      if str(verdef.real_type) == "float":
        assembly += f"\tmovss %{reg}, -{ofs}(%rbp, %{dim_reg}, 8)\n"
      elif str(verdef.real_type) == "int":
        assembly += f"\tmovq %{reg}, -{ofs}(%rbp, %{dim_reg}, 8)\n"
      elif str(verdef.real_type) == "char":
        assembly += f"\tmovq %{reg}, -{ofs}(%rbp, %{dim_reg}, 8)\n"
      registers[reg][0] = True
      registers[dim_reg][0] = True

  # variable reference
  elif node.type == "$varref":
    id = str(node.children[0])


    if id in func_dict[current_func]:
      ofs = func_dict[current_func][id]
      if node.real_type == "int":
        for r in r_order:
          if registers[r][0] == True:
            registers[r][0] = False
            assembly += f"\tmovq -{ofs}(%rbp), %{r}\n"
            return r
      elif node.real_type == "float":
        for r in fr_order:
          if registers[r][0] == True:
            registers[r][0] = False
            assembly += f"\tmovss -{ofs}(%rbp), %{r}\n"
            if node.converted_type  == "int":
              for ri in r_order:
                if registers[ri][0] == True:
                  registers[ri][0] = False
                  assembly += f"\tcvttss2si %{r}, %{ri}\n"
                  return ri
            return r
      elif node.real_type == "char":
        for r in r_order:
          if registers[r][0] == True:
            registers[r][0] = False
            assembly += f"\tmovq -{ofs}(%rbp), %{r}\n"
            return r
  

    # if id is a global variable
    else:
      if node.real_type == "float":
        for r in fr_order:
          if registers[r][0] == True:
            registers[r][0] = False
            assembly += f"\tmovss {id}(%rip), %{r}\n"
            return r
      elif node.real_type == "int":
        for r in r_order:
          if registers[r][0] == True:
            registers[r][0] = False
            assembly += f"\tmovq {id}(%rip), %{r}\n"
            return r
      elif str(node.real_type) == "char":
        for r in r_order:
          if registers[r][0] == True:
            registers[r][0] = False
            assembly += f"\tmovq {id}(%rip), %{r}\n"
            return r

    # # if id is a local variable
    # else:
    #   ofs = func_dict[current_func][id]
    #   if node.real_type == "int":
    #     for r in r_order:
    #       if registers[r][0] == True:
    #         registers[r][0] = False
    #         assembly += f"\tmovq -{ofs}(%rbp), %{r}\n"
    #         return r
    #   elif node.real_type == "float":
    #     for r in fr_order:
    #       if registers[r][0] == True:
    #         registers[r][0] = False
    #         assembly += f"\tmovss -{ofs}(%rbp), %{r}\n"
    #         if node.converted_type  == "int":
    #           for ri in r_order:
    #             if registers[ri][0] == True:
    #               registers[ri][0] = False
    #               assembly += f"\tcvttss2si %{r}, %{ri}\n"
    #               return ri
    #         return r
    #   elif node.real_type == "char":
    #     for r in r_order:
    #       if registers[r][0] == True:
    #         registers[r][0] = False
    #         assembly += f"\tmovq -{ofs}(%rbp), %{r}\n"
    #         return r
  
  elif node.type == "$vardef":
    id = node.children[0]
    return id


  elif node.type == "$arraydef":
    id = node.children[0]
    dim = node.children[1]
    dim_reg = expr(dim)
    if dim.real_type == "char":
      assembly += f"\tsubq $97, %{dim_reg}\n"
    return id, dim_reg
  
  elif node.type == "$arrayref":
    id = node.children[0]
    dim = node.children[1]
    dim_reg = expr(dim)

    if str(dim.real_type) == "char":
      assembly += f"\tsubq $97, %{dim_reg}\n"

    ofs = func_dict[current_func][id]
    if str(node.real_type) == "float":
      for r in fr_order:
        if registers[r][0] == True:
          registers[r][0] = False
          assembly += f"\tmovss -{ofs}(%rbp, %{dim_reg}, 8), %{r}\n"
          registers[dim_reg][0] = True
          return r
    
    elif str(node.real_type) == "int":
      for r in r_order:
        if registers[r][0] == True:
          registers[r][0] = False
          assembly += f"\tmovq -{ofs}(%rbp, %{dim_reg}, 8), %{r}\n"
          registers[dim_reg][0] = True
          return r

    elif str(node.real_type) == "char":
      for r in r_order:
        if registers[r][0] == True:
          registers[r][0] = False
          assembly += f"\tmovq -{ofs}(%rbp, %{dim_reg}, 8), %{r}\n"
          registers[dim_reg][0] = True
          return r

  elif str(node.type) == "$if":
    cond = node.children[0]
    then = node.children[1]
    reg = expr(cond)
    # else  label
    else_label = f".L{label_count}"
    label_count += 1

    assembly += f"\tcmp $1, %{reg}\n"
    assembly += f"\tjne {else_label}\n"
    expr(then)
    
    # end label
    end_label = f".L{label_count}"
    label_count += 1
    assembly += f"\tjmp {end_label}\n"
    assembly += f"{else_label}:\n"
    
    if len(node.children) > 2:
      else_ = node.children[2]
      expr(else_)
      assembly += f"\tjmp {end_label}\n"
    
    assembly += f"{end_label}:\n"
    
    registers[reg][0] = True


  elif str(node.type) == "$while":
    cond = node.children[0]
    body = node.children[1]
    # start label
    start_label = f".L{label_count}"
    label_count += 1

    # end label
    end_label = f".L{label_count}"
    label_count += 1

    assembly += f"{start_label}:\n"
    reg = expr(cond)
    assembly += f"\tcmp $1, %{reg}\n"
    assembly += f"\tjne {end_label}\n"
    expr(body)
    assembly += f"\tjmp {start_label}\n"
    assembly += f"{end_label}:\n"
    registers[reg][0] = True


  elif node.type == "$write":
    reg = expr(node.children[0])
    
    if str(node.children[0].real_type) == "int":
      assembly += f"\tmovq %{reg}, %rsi\n"
      registers[reg][0] = True
      assembly += f"\tleaq .int_wformat(%rip), %rdi\n"
      assembly += f"\tmov $0, %rax\n"
      assembly += f"\tcall printf\n"
    
    elif str(node.children[0].real_type) == "str":
      str_var = node.children[0].str_const
      assembly += f"\tleaq .string_const{str_var}(%rip), %rdi\n"
      assembly += f"\tcall printf\n"
    
    elif str(node.children[0].real_type) == "float":
      if reg != "xmm0":
        assembly += f"\tmovss %{reg}, %xmm0\n"
      registers[reg][0] = True
      assembly += f"\tcvtss2sd %xmm0, %xmm0\n"
      assembly += f"\tleaq .float_wformat(%rip), %rdi\n"
      assembly += f"\tmovq $1, %rax\n"
      assembly += f"\tcall printf\n"
    
    elif str(node.children[0].real_type) == "char":
      assembly += f"\tmovq %{reg}, %rax\n"
      registers[reg][0] = True
      assembly += f"\tmovsbq %al, %rax\n"
      assembly += f"\tmovq %rax, %rdi\n"
      assembly += f"\tcall putchar\n"
      assembly += f"\tmovq $10, %rax\n"
      assembly += f"\tmovsbq %al, %rax\n"
      assembly += f"\tmovq %rax, %rdi\n"
      assembly += f"\tcall putchar\n"
      
    
    # for printing values
    
  

  elif node.type == "$str":
    head += f'.string_const{string_var}:.string "{node.children[0]}\n"\n'
    node.str_const = string_var
    string_var += 1   

 
  elif node.type == "$icon":
    for r in r_order:
      if registers[r][0] == True:
        registers[r][0] = False
        registers[r][1] = node.children[0]
        assembly += f"\tmovq ${node.children[0]}, %{r}\n"
        return r
      
  elif node.type == "$fcon":
    for r in fr_order:
      if registers[r][0] == True:
        registers[r][0] = False
        registers[r][1] = node.children[0]
        head += f".float{float_var}:\t.float {node.children[0]}\n"
        assembly += f"\tmovss .float{float_var}(%rip), %{r}\n"
        float_var += 1
        return r
    
  elif node.type == "$ccon":
    # if node.converted_type == "char":
    #   for r in r_order:
    #     if registers[r][0] == True:
    #       registers[r][0] = False
    #       registers[r][1] = node.children[0]
    #       assembly += f"\tmovq ${node.children[0]}, %{r}\n"
    #       return r
    # elif node.converted_type == "int":
    for r in r_order:
      if registers[r][0] == True:
        registers[r][0] = False
        registers[r][1] = ord(str(node.children[0])[1])
        assembly += f"\tmovq ${ord(str(node.children[0])[1])}, %{r}\n"
        return r
  
  elif node.type == "$type":
    pass

  elif node.type == "$ret":
    reg = expr(node.children[0])
    if str(node.children[0].real_type) == "int":
      assembly += f"\tmovq %{reg}, %rax\n"
      return "rax"
      # assembly += f"\tleave\n\tret\n"
    
    elif str(node.children[0].real_type) == "float":
      assembly += f"\tmovss %{reg}, %xmm0\n"
      return "xmm0"
      # assembly += f"\tleave\n\tret\n"
    
    elif str(node.children[0].real_type) == "char":
      assembly += f"\tmovq %{reg}, %rax\n"
      return "rax"
    
    registers[reg][0] = True
    
    

def asm(fn, node):
  global assembly
  global head
  
  # assembly = ""
  head = ''
  head += f"\t.section .rodata\n"
  head += f".char_wformat: .string \"%c\\n\"\n"
  head += f".int_wformat: .string \"%d\\n\"\n"
  head += f".float_wformat: .string \"%f\\n\"\n"
  head += f".str_wformat: .string \"%s\\n\"\n"
  head += f".char_rformat: .string \"%c\"\n"
  head += f".int_rformat: .string \"%ld\"\n"
  head += f".float_rformat: .string \"%f\"\n"
  
  # assembly += f"\n"
  # assembly += f"\t.text\n"
  # assembly += f"\t.globl main\n"
  # assembly += f"\t.type main,@function\n"    
  # assembly += f"main:\n"
  # assembly += f"\tpushq %rbp\n"
  # assembly += f"\tmovq %rsp, %rbp\n"
  # assembly += f"\tsubq $8, %rsp\n"
  
  # print(node)
  expr(node)

  assembly = head + assembly 
  # assembly += f"\tleave\n\tret\n"

  with open(fn, 'w') as file:
    file.write(assembly) 