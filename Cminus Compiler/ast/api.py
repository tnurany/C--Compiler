# Initialize an ASTNode with a given value.
# Args:
# value (str): The value associated with this node, typically representing
#              the type of AST node, e.g., "$and" or "$varref".

# Add a child node to the current ASTNode.
# Args:
# child_node (ASTNode): The child node to be added to the current node.

# Generate a string representation of the ASTNode.
# Returns:
# str: A string representation of the ASTNode and its children, if any.
class ASTNode:
    def __init__(self, type):
        self.type = type
        self.children = []
        self.real_type = ''
        self.converted_type = ''
        self.str_const = -1

    def add_child(self, child_node):
        self.children.append(child_node)

    def __str__(self):
        if not self.children:
            return f"{self.type}"
            #return f"{selt.type}:{self.real_type}:{self.converted_type}"
        else:
            children_str = " ".join(str(child) for child in self.children)
            # return f"#({self.type} {children_str})"
        
            return f"#({self.type}:{self.real_type}:{self.converted_type} {children_str})"
    
    def print_funtion(self):
        if not self.children:
            return f"{self.type}"
            #return f"{selt.type}:{self.real_type}:{self.converted_type}"
        else:
            children_str = " ".join(str(child) for child in self.children)
            # return f"#({self.type} {children_str})"

            return f"#({self.type}:{self.real_type}:{self.converted_type} {children_str})"



# **
# * Return a string representation based on the tree grammar
# *
# * @param n an ASTNode
# * @return a char*
def getTreeNodeRep(n):
    # Base case: If the node has no children, return its value as a string
    # if not n.children:
    #     return n.value

    # # Recursive case: Build the string representation by traversing children
    # child_reprs = [getTreeNodeRep(child) for child in n.children]

    # # Combine the node's value with its children's representations
    # return f"#{n.value} {' '.join(child_reprs)}"

    return n.print_funtion() 


# **
# * makeProg - Create a $prog node
# *
# * @param vlist a $vlist node
# * @param flist a $flist node
# *
# *              Add vlist if non-NULL
# *              Add flist if non-NULL
# *
# * @return a $prog node
# *
def makeProg(vlist, flist):
    # Create a new $prog node
    prog_node = ASTNode("$prog")

    # Add vlist to the $prog node if it's not None
    if vlist is not None:
        prog_node.add_child(vlist)

    # Add flist to the $prog node if it's not None
    if flist is not None:
        prog_node.add_child(flist)
    return prog_node


# **
# * makeFlist - Create a $flist node
# *
# * @param node  a $flist node
# * @param fdecl a $fdecl node
# *
# *              If node is NULL, create a new $flist node. Otherwise, use node.
# *              Add fdecl if non-NULL
# *
# * @return a $flist node
# *
def makeFlist(node, fdecl):
    # Create a new $flist node if node is None
    flist_node = ASTNode("$flist") if node is None else node

    # Add fdecl to the $flist node if it's not None
    if fdecl is not None:
        flist_node.add_child(fdecl)
    return flist_node


# **
# * makeFdecl - Create a $fdecl node
# *
# * @param node  a $fdecl node test
# * @param type  a $type node
# * @param id    a string
# * @param plist a $plist node
# * @param vlist a $vlist node
# * @param stmts a $cmpd node
# *
# *              If node is NULL, create a new $fdecl node. Otherwise, use node.
# *              Add type if non-NULL
# *              Add id if non-NULL
# *              Add plist if non-NULL
# *              Add vlist if non-NULL
# *              Add stmts if non-NULL
# *
# * @return a $fdecl node
# *
def makeFdecl(node, type, id, plist, vlist, stmts):
    # Create a new $fdecl node if node is None
    fdecl_node = ASTNode("$fdecl") if node is None else node

    # Add type to the $fdecl node if it's not None
    if type is not None:
        fdecl_node.add_child(type)

    # Add id to the $fdecl node if it's not None
    if id is not None:
        fdecl_node.add_child(ASTNode(id))

    # Add plist to the $fdecl node if it's not None
    if plist is not None:
        fdecl_node.add_child(plist)

    # Add vlist to the $fdecl node if it's not None
    if vlist is not None:
        fdecl_node.add_child(vlist)

    # Add stmts to the $fdecl node if it's not None
    if stmts is not None:
        fdecl_node.add_child(stmts)
    return fdecl_node


# **
# * makePlist - Create a $plist node
# *
# * @param node  a $plist node
# * @param vdecl a $pdecl node
# *
# *              If node is NULL, create a new $plist node. Otherwise, use node.
# *              Add vdecl to node if non-NULL
# *
# * @return a pvlist node
# *
def makePlist(node, pdecl):
    # Create a new $plist node if node is None
    if pdecl is None:
        plist_node = ASTNode("#($plist:none:none)")
    
    else:
        plist_node = ASTNode("$plist") if node is None else node

    # Add pdecl to the $plist node if it's not None
    if pdecl is not None:
        plist_node.add_child(pdecl)
    

    return plist_node



# **
# * makePdecl - Create a $pdecl node
# *
# * @param type a $type node
# * @param id   a $ident node
# *
# *             Add type to node
# *             Add id to node
# *
# * @return a $vdecl node
# *
def makePdecl(type, id):
    # Create a new $pdecl node
    pdecl_node = ASTNode("$pdecl")

    # Add type to the $pdecl node
    pdecl_node.add_child(type)

    # Add id to the $pdecl node
    pdecl_node.add_child(id)
    return pdecl_node


# **
# * makeVlist - Create a $vlist node
# *
# * @param node  a $vlist node
# * @param vdecl a $vdecl node
# *
# *              If node is NULL, create a new $vlist node. Otherwise, use node.
# *              Add id to node if non-NULL
# *
# * @return a $vlist node
# *
def makeVlist(node, vdecl):
    if vdecl is None:
        vlist_node = ASTNode("#($vlist:none:none)")
    else:
        # Create a new $vlist node if node is None
        vlist_node = ASTNode("$vlist") if node is None else node

    # Add vdecl to the $vlist node if it's not None
    if vdecl is not None:
        vlist_node.add_child(vdecl)
    
    return vlist_node


# **
# * makeVdecl - Create a $vdecl node
# *
# * @param type a $type node
# * @param ids  a $ilist node
# *
# *             Add type to node
# *             Add ids to node
# *
# * @return a $vdecl node
# *
def makeVdecl(type, ids):# Create a new $vdecl node
    vdecl_node = ASTNode("$vdecl")

    # Add type to the $vdecl node
    vdecl_node.add_child(type)

    # Add ids to the $vdecl node
    vdecl_node.add_child(ids)
    return vdecl_node


# **
# * makeIlist - Create a $ilist node
# *
# * @param node a $ilist node
# * @param id   a $ident node
# *
# *             If node is NULL, create a new $ilist node. Otherwise, use node.
# *             Add id to node if non-NULL
# *
# * @return a $ilist node
# *
def makeIlist(node, id):
    # Create a new $ilist node if node is None
    ilist_node = ASTNode("$ilist") if node is None else node

    # Add id to the $ilist node if it's not None
    if id is not None:
        ilist_node.add_child(id)
    return ilist_node


# **
# * makeIdent - Create a $ident node
# *
# * @param id    a string
# * @param dimen a string
# *
# *              Add id
# *              Add dimen if non-NULL
# *
# * @return a $ident node
# *
def makeIdent(id, dimen):
    # Create a new $ident node
    ident_node = ASTNode("$ident")

    # Add id to the $ident node
    ident_node.add_child(ASTNode(id))

    # Add dimen to the $ident node if it's not None
    if dimen is not None:
        ident_node.add_child(ASTNode(dimen))
    return ident_node


# **
# * makeType - make an $type node
# *
# * @param type a string, one of "char", "float", "int", or "void"
# *
# *             Create a new $type node.
# *
# * @return a $type node
# *
def makeType(type):
    # Create a new $type node with the specified type string
    type_node = ASTNode("$type")
    type_node.add_child(ASTNode(type))
    return type_node


# **
# * makeAssign - make an $assign node
# *
# * @param lval a definition
# * @param rval an expression
# *
# *             Create a new $assign node.
# *             Add id to node
# *
# * @return a $assign node
# *
def makeAssign(lval, rval):
    # Create a new $assign node
    assign_node = ASTNode("$assign")

    # Add lval (left-hand side) to the $assign node
    assign_node.add_child(lval)

    # Add rval (right-hand side) to the $assign node
    assign_node.add_child(rval)
    return assign_node


# **
# * makeVardef - make an $vardef node
# *
# * @param id an identifier
# *
# *           Create a new $vardef node.
# *           Add id to node
# *
# * @return a $vardef node
# *
def makeVardef(id):
    # Create a new $vardef node
    vardef_node = ASTNode("$vardef")

    # Add id (identifier) to the $vardef node
    vardef_node.add_child(id)
    return vardef_node


# **
# * makeArraydef - make an $arraydef node
# *
# * @param id        an identifier
# * @param subscript an expression subscript
# *
# *                  Create a new $arraydef node.
# *                  Add id to node
# *                  Add subscript to node
# *
# * @return a $arraydef node
# *
def makeArraydef(id, subscript):
    # Create a new $arraydef node
    arraydef_node = ASTNode("$arraydef")

    # Add id (identifier) to the $arraydef node
    arraydef_node.add_child(id)

    # Add subscript to the $arraydef node
    arraydef_node.add_child(subscript)
    return arraydef_node


# **
# * makePcall - make an $pcall node
# *
# * @param id   an identifier
# * @param args an $elist node
# *
# *             Create a new $pcall node.
# *             Add id to node
# *             Add args to node
# *
# * @return a $pcall node
# *
def makePcall(id, args):
    # Create a new $pcall node
    pcall_node = ASTNode("$pcall")

    # Add id (identifier) to the $pcall node
    pcall_node.add_child(id)

    # Add args (arguments) to the $pcall node
    pcall_node.add_child(args)
    return pcall_node


# **
# * makeIf - Create a $if node
# *
# * @param node a $if node
# * @param test an expression node
# * @param thn  a statement node
# * @param els  a statement node
# *
# *             If node is NULL, create a new $if node. Otherwise, use node.
# *             Add test,thn, and/or els to node if any is non-NULL
# *
# * @return a $if node
# *
def makeIf(node, test, thn, els):
    # Create a new $if node if node is None
    if_node = ASTNode("$if") if node is None else node

    # Add test to the $if node if it's not None
    if test is not None:
        if_node.add_child(test)

    # Add thn to the $if node if it's not None
    if thn is not None:
        if_node.add_child(thn)

    # Add els to the $if node if it's not None
    if els is not None:
        if_node.add_child(els)
    return if_node


# **
# * makeWhile - make a $while node
# *
# * Create a new $while node.
# *
# * @param expr an expression
# * @param body a statement
# *
# * @return a $while node
# *
def makeWhile(expr, stmt):
    # Create a new $while node
    while_node = ASTNode("$while")

    # Add expr (expression) to the $while node
    while_node.add_child(expr)

    # Add stmt (statement) to the $while node
    while_node.add_child(stmt)
    return while_node


# **
# * makeRead - make a $read node
# *
# * Create a new $read node.
# *
# * @param var a variable reference
# *
# * @return a $read node
# *
def makeRead(var):
    # Create a new $read node
    read_node = ASTNode("$read")

    # Add var (variable reference) to the $read node
    read_node.add_child(var)
    return read_node


# **
# * makeWrite - make a $write node
# *
# * Create a new $write node.
# *
# * @param expr an expression
# *
# * @return a $write node
# *
def makeWrite(expr):
    # Create a new $write node
    write_node = ASTNode("$write")

    # Add expr (expression) to the $write node
    write_node.add_child(expr)
    return write_node


# **
# * makeRet - make a $ret node
# *
# * Create a new $ret node.
# *
# * @param expr an expression
# *
# * @return a $ret node
# *
def makeRet(expr):
    # Create a new $ret node
    ret_node = ASTNode("$ret")

    # Add expr (expression) to the $ret node
    ret_node.add_child(expr)
    return ret_node


# **
# * makeExit - make an $exit node
# *
# * Create a new $exit node.
# *
# * @return a $exit node
# *
def makeExit():
    # Create a new $exit node
    exit_node = ASTNode("#($exit:none:none)")
    return exit_node


# **
# * makeCmpd - Create a $cmpd node
# *
# * @param node a $cmpd node
# * @param stmt a statement node
# *
# *             If node is NULL, create a new $cmpd node. Otherwise, use node.
# *             Add stmt to node
# *
# * @return a $cmpd node
# *
def makeCmpd(node, stmt):
    # Create a new $cmpd node if node is None
    cmpd_node = ASTNode("$cmpd") if node is None else node

    # Add stmt (statement) to the $cmpd node
    cmpd_node.add_child(stmt)
    return cmpd_node


# **
# * makeNot - make an $not node
# *
# * @param oper the operand
# *
# *             Create a new $not node.
# *             Add oper to node
# *
# * @return a $not node
# *
def makeNot(oper):
    # Create a new $not node
    not_node = ASTNode("$not")

    # Add oper (operand) to the $not node
    not_node.add_child(oper)
    return not_node


# **
# * makeOr - make an $or node
# *
# * @param loper the left operand
# * @param roper the right operand
# *
# *              Create a new $or node.
# *              Add loper to node
# *              Add roper to node
# *
# * @return a $or node
# *
def makeOr(loper, roper):
    # Create a new $or node
    or_node = ASTNode("$or")

    # Add loper to the $or node
    or_node.add_child(loper)

    # Add roper to the $or node
    or_node.add_child(roper)

    return or_node


# **
# * makeAnd - make an $and node
# *
# * @param loper the left operand
# * @param roper the right operand
# *
# *              Create a new $and node.
# *              Add loper to node
# *              Add roper to node
# *
# * @return a $and node
# *
def makeAnd(loper, roper):
    # Create a new $and node
    and_node = ASTNode("$and")

    # Add loper to the $and node
    and_node.add_child(loper)

    # Add roper to the $and node
    and_node.add_child(roper)
    
    return and_node


# **
# * makeEq - make an $eq node
# *
# * @param loper the left operand
# * @param roper the right operand
# *
# *              Create a new $eq node.
# *              Add loper to node
# *              Add roper to node
# *
# * @return a $eq node
# *
def makeEq(loper, roper):
    # Create a new $eq node
    eq_node = ASTNode("$eq")

    # Add loper to the $eq node
    eq_node.add_child(loper)

    # Add roper to the $eq node
    eq_node.add_child(roper)

    return eq_node


# **
# * makeNe - make an $ne node
# *
# * @param loper the left operand
# * @param roper the right operand
# *
# *              Create a new $ne node.
# *              Add loper to node
# *              Add roper to node
# *
# * @return a $ne node
# *
def makeNe(loper, roper):
    # Create a new $ne node
    ne_node = ASTNode("$ne")

    # Add loper to the $ne node
    ne_node.add_child(loper)

    # Add roper to the $ne node
    ne_node.add_child(roper)

    return ne_node


# **
# * makeLe - make an $le node
# *
# * @param loper the left operand
# * @param roper the right operand
# *
# *              Create a new $le node.
# *              Add loper to node
# *              Add roper to node
# *
# * @return a $le node
# *
def makeLe(loper, roper):
    # Create a new $le node
    le_node = ASTNode("$le")

    # Add loper (left operand) to the $le node
    le_node.add_child(loper)

    # Add roper (right operand) to the $le node
    le_node.add_child(roper)
    return le_node


# **
# * makeLt - make an $lt node
# *
# * @param loper the left operand
# * @param roper the right operand
# *
# *              Create a new $lt node.
# *              Add loper to node
# *              Add roper to node
# *
# * @return a $lt node
# *
def makeLt(loper, roper):
    # Create a new $lt node
    lt_node = ASTNode("$lt")

    # Add loper (left operand) to the $lt node
    lt_node.add_child(loper)

    # Add roper (right operand) to the $lt node
    lt_node.add_child(roper)
    return lt_node


# **
# * makeGe - make an $ge node
# *
# * @param loper the left operand
# * @param roper the right operand
# *
# *              Create a new $ge node.
# *              Add loper to node
# *              Add roper to node
# *
# * @return a $ge node
# *
def makeGe(loper, roper):
    # Create a new $ge node
    ge_node = ASTNode("$ge")

    # Add loper (left operand) to the $ge node
    ge_node.add_child(loper)

    # Add roper (right operand) to the $ge node
    ge_node.add_child(roper)
    return ge_node


# **
# * makeGt - make an $gt node
# *
# * @param loper the left operand
# * @param roper the right operand
# *
# *              Create a new $gt node.
# *              Add loper to node
# *              Add roper to node
# *
# * @return a $gt node
# *
def makeGt(loper, roper):
    # Create a new $gt node
    gt_node = ASTNode("$gt")

    # Add loper (left operand) to the $gt node
    gt_node.add_child(loper)

    # Add roper (right operand) to the $gt node
    gt_node.add_child(roper)
    return gt_node


# **
# * makeAdd - make an $add node
# *
# * @param loper the left operand
# * @param roper the right operand
# *
# *              Create a new $add node.
# *              Add loper to node
# *              Add roper to node
# *
# * @return a $add node
# *
def makeAdd(loper, roper):
    # Create a new $add node
    add_node = ASTNode("$add")

    # Add loper (left operand) to the $add node
    add_node.add_child(loper)

    # Add roper (right operand) to the $add node
    add_node.add_child(roper)
    return add_node


# **
# * makeSub - make an $sub node
# *
# * @param loper the left operand
# * @param roper the right operand
# *
# *              Create a new $sub node.
# *              Add loper to node
# *              Add roper to node
# *
# * @return a $sub node
# *
def makeSub(loper, roper):
    # Create a new $sub node
    sub_node = ASTNode("$sub")

    # Add loper (left operand) to the $sub node
    sub_node.add_child(loper)

    # Add roper (right operand) to the $sub node
    sub_node.add_child(roper)
    return sub_node


# **
# * makeMul - make an $mul node
# *
# * @param loper the left operand
# * @param roper the right operand
# *
# *              Create a new $mul node.
# *              Add loper to node
# *              Add roper to node
# *
# * @return a $mul node
# *
def makeMul(loper, roper):
    # Create a new $mul node
    mul_node = ASTNode("$mul")

    # Add loper (left operand) to the $mul node
    mul_node.add_child(loper)

    # Add roper (right operand) to the $mul node
    mul_node.add_child(roper)
    return mul_node


# **
# * makeDiv - make an $div node
# *
# * @param loper the left operand
# * @param roper the right operand
# *
# *              Create a new $div node.
# *              Add loper to node
# *              Add roper to node
# *
# * @return a $div node
# *
def makeDiv(loper, roper):
    # Create a new $div node
    div_node = ASTNode("$div")

    # Add loper (left operand) to the $div node
    div_node.add_child(loper)

    # Add roper (right operand) to the $div node
    div_node.add_child(roper)
    return div_node


# **
# * makeFcall - make an $fcall node
# *
# * @param id   an identifier
# * @param args an $elist node
# *
# *             Create a new $fcall node.
# *             Add id to node
# *             Add args to node
# *
# * @return a $fcall node
# *
def makeFcall(id, args):
    # Create a new $fcall node
    fcall_node = ASTNode("$fcall")

    # Add id (identifier) to the $fcall node
    fcall_node.add_child(id)

    # Add args (arguments) to the $fcall node
    fcall_node.add_child(args)
    return fcall_node


# **
# * makeVarref - make an $varref node
# *
# * @param id an identifier
# *
# *           Create a new $varref node.
# *           Add id to node
# *
# * @return a $varref node
# *
def makeVarref(id):
    # Create a new $varref node
    varref_node = ASTNode("$varref")

    # Add id (identifier) to the $varref node
    varref_node.add_child(id)
    return varref_node


# **
# * makeArrayref - make an $arrayref node
# *
# * @param id        an identifier
# * @param subscript an expression subscript
# *
# *                  Create a new $arrayref node.
# *                  Add id to node
# *                  Add subscript to node
# *
# * @return a $arrayref node
# *
def makeArrayref(id, subscript):
    # Create a new $arrayref node
    arrayref_node = ASTNode("$arrayref")

    # Add id (identifier) to the $arrayref node
    arrayref_node.add_child(id)

    # Add subscript (expression subscript) to the $arrayref node
    arrayref_node.add_child(subscript)
    return arrayref_node


# **
# * makeStr - make an $str node
# *
# * @param val the string
# *
# *            Create a new $str node.
# *            Add val to node
# *
# * @return a $str node
# *
def makeStr(val):
    # # Create a new $str node
    # str_node = ASTNode("$str")

    # # Add val (string) to the $str node
    # str_node.add_child(val)

    # Create a new $str node
    str_node = ASTNode("$str")

    # Remove double quotes from the string value
    val_without_quotes = val.strip('"')

    # Add val (string value without quotes) to the $str node
    str_node.add_child(val_without_quotes)
    return str_node


# **
# * makeCcon - make an $ccon node
# *
# * @param val a string representation of the constant value
# *
# *            Create a new $ccon node.
# *            Add val to node
# *
# * @return an $ccon node
# *
def makeCcon(val):
    # Create a new $ccon node
    ccon_node = ASTNode("$ccon")

    # Add val (string representation of the constant value) to the $ccon node
    ccon_node.add_child(val)
    return ccon_node


# **
# * makeFcon - make an $fcon node
# *
# * @param val a string representation of the constant value
# *
# *            Create a new $fcon node.
# *            Add val to node
# *
# * @return an $fcon node
# *
def makeFcon(val):
    # Create a new $fcon node
    fcon_node = ASTNode("$fcon")

    # Add val (string representation of the constant value) to the $fcon node
    fcon_node.add_child(val)
    return fcon_node


# **
# * makeIcon - make an $icon node
# *
# * @param val a string representation of the constant value
# *
# *            Create a new $icon node
# *            Add val to node
# *
# * @return an $icon node
# *
def makeIcon(val):
    # Create a new $icon node
    icon_node = ASTNode("$icon")

    # Add val (string representation of the constant value) to the $icon node
    icon_node.add_child(val)
    return icon_node


# **
# * makeElist - make an $elist node
# *
# * @param node an $elist node
# * @param expr an expression node
# *
# *             If node is NULL, create a new $elist node. Otherwise, use node.
# *             Add expr to node
# *
# * @return an $elist node
# *
def makeElist(node, expr):
    if expr is None:
        elist_node = ASTNode("#($elist:none:none)")
    
    else:
        elist_node = ASTNode("$elist") if node is None else node

    # Add expr (expression node) to the $elist node
    if expr is not None:
        elist_node.add_child(expr)
    return elist_node