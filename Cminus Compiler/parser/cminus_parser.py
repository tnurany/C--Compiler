import sys
import os
import ply.yacc as yacc
import cminus_scanner 

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
ast = os.path.dirname(current) + "/ast"

# adding the parent directory to
# the sys.path.

sys.path.append(ast)

from api import *
from type import *
from assembly import *

# from ast.api import *

start ='program'
tokens = cminus_scanner.tokens

def p_program_procs(attr): 
  'program : procedures'
  attr[0] = makeProg(makeVlist(None, None), attr[1])

def p_program_decls(attr):
  'program : declList procedures'
  attr[0] = makeProg(attr[1], attr[2])

def p_procedures(attr):
  'procedures : procedures procedureDecl'
  attr[0] = makeFlist(attr[1], attr[2])

def p_procedures_decl(attr):
  'procedures : procedureDecl'
  attr[0] = makeFlist(None, attr[1])

def p_decl(attr):
  'declList : type identifierList SEMICOLON'
  attr[0] = makeVlist(None, makeVdecl(attr[1], attr[2]))

def p_decl_list(attr):
  'declList : declList type identifierList SEMICOLON'
  attr[0] = makeVlist(attr[1], makeVdecl(attr[2], attr[3]))

def p_procedure_decl(attr):
  'procedureDecl : procedureHead procedureBody'
  # prodHead = [type, id, paramList, decList]
  # procBody = CmptStmt
  attr[0] = makeFdecl(None, attr[1][0], attr[1][1], attr[1][2], attr[1][3], attr[2])

def p_procedure_head_decl(attr):
  'procedureHead : functionDecl declList'
  # funcDec = [type, id, paramlist]
  # declList
  attr[1].append(attr[2])
  # procedureHead = [type, id, paramlist, declList]
  attr[0] = attr[1]
  

def p_procedure_head(attr):
  'procedureHead : functionDecl'
  # procedureHead = [type, id, paramlist]
  attr[1].append(makeVlist(None, None))
  attr[0] = attr[1]


def p_function_decl(attr):
  'functionDecl : type IDENTIFIER LPAREN paramDeclList RPAREN LBRACE'
  # functionDecl = [type, id, paramlist]
  attr[0] = [attr[1], attr[2], attr[4]]


def p_function_decl_noparam(attr):
  'functionDecl : type IDENTIFIER LPAREN RPAREN LBRACE'
  # functionDecl = [type, Id, null_paramlist]
  attr[0] = [attr[1], attr[2], makePlist(None, None)]


def p_procedure_body(attr):
  'procedureBody : statementList RBRACE'
  attr[0] = attr[1]

def p_param_decl_list_decl(attr):
  'paramDeclList : type varDecl'
  attr[0] = makePlist(None, makePdecl(attr[1], attr[2]))

def p_param_decl_list(attr):
  'paramDeclList : paramDeclList COMMA type varDecl'
  attr[0] = makePlist(attr[1], makePdecl(attr[3], attr[4]))

def p_id_list_vardecl(attr):
  'identifierList : varDecl'
  attr[0] = makeIlist(None, attr[1])

def p_id_list(attr):
  'identifierList : identifierList COMMA varDecl'
  attr[0] = makeIlist(attr[1], attr[3])

def p_var_decl_id(attr):
  'varDecl : IDENTIFIER'
  attr[0] = makeIdent(attr[1], None)
  
def p_var_decl_array(attr):
  'varDecl : IDENTIFIER LBRACKET INTCON RBRACKET'
  attr[0] = makeIdent(attr[1], makeIcon(attr[3]))

def p_var_decl_array_char(attr):
  'varDecl : IDENTIFIER LBRACKET CHARCON RBRACKET'
  attr[0] = makeIdent(attr[1], makeCcon(attr[3]))

def p_type_char(attr):
  'type  : CHAR'
  attr[0] = makeType(attr[1])

def p_type_int(attr):
  'type  : INT'
  attr[0] = makeType(attr[1])

def p_type_float(attr):
  'type : FLOAT'
  attr[0] = makeType(attr[1])

def p_type_void(attr):
  'type : VOID'
  attr[0] = makeType(attr[1])

def p_statement_assignment(attr):
  'statement 	: assignment'
  attr[0] = attr[1]

def p_statement_if(attr):
  'statement 	: ifStatement'
  attr[0] = attr[1]

def p_statement_while(attr):
  'statement 	: whileStatement'
  attr[0] = attr[1]

def p_statement_io(attr):
  'statement 	: ioStatement'
  attr[0] = attr[1]

def p_statement_returnn(attr):
  'statement 	: returnStatement'
  attr[0] = attr[1]

def p_statement_exit(attr):
  'statement 	: exitStatement'
  attr[0] = attr[1]

def p_statement_compound(attr):
  'statement 	: compoundStatement'
  attr[0] = attr[1]

def p_statemet_callStatement(attr):
  'statement : callStatement'
  attr[0] = attr[1]

def p_callStatement(attr):
  'callStatement 	: IDENTIFIER LPAREN RPAREN SEMICOLON'
  attr[0] = makePcall(attr[1], makeElist(None, None))

def p_callStatement_args(attr):
  'callStatement 	: IDENTIFIER LPAREN argList RPAREN SEMICOLON'
  attr[0] = makePcall(attr[1], attr[3])

def p_assignment(attr):
  'assignment  : variable_def ASSIGN expr SEMICOLON'
  attr[0] = makeAssign(attr[1], attr[3])

def p_variable_def(attr):
  'variable_def 	: IDENTIFIER'
  attr[0] = makeVardef(attr[1])

def p_variable_def_array(attr):
  'variable_def 	: IDENTIFIER LBRACKET expr RBRACKET'  
  attr[0] = makeArraydef(attr[1], attr[3])
   
				
def p_if(attr):
  'ifStatement	: IF testAndThen ELSE compoundStatement'
  attr[0] = makeIf(None, attr[2][0], attr[2][1], attr[4])

def p_if_then(attr):
  'ifStatement : IF testAndThen'
  attr[0] = makeIf(None, attr[2][0], attr[2][1], None)
		
def p_test_then(attr):
  'testAndThen	: test compoundStatement'
  attr[0] = [attr[1], attr[2]]
				
def p_test(attr):
  'test		: LPAREN expr RPAREN'
  attr[0] = attr[2]

def p_while_stmt(attr):
  'whileStatement  : WHILE whileExpr statement'
  attr[0] = makeWhile(attr[2], attr[3])
                
def p_while_expr(attr):
  'whileExpr	: LPAREN expr RPAREN'
  attr[0] = attr[2]
				
def p_read(attr):
  'ioStatement     : READ LPAREN variable_def RPAREN SEMICOLON'
  attr[0] = makeRead(attr[3])
                
def p_write_expr(attr):
  'ioStatement : WRITE LPAREN expr RPAREN SEMICOLON'
  attr[0] = makeWrite(attr[3])

def p_write_str(attr):
  'ioStatement : WRITE LPAREN stringConstant RPAREN SEMICOLON'
  attr[0] = makeWrite(attr[3])


def p_return_stmt(attr):
  'returnStatement : RETURN expr SEMICOLON'
  attr[0] = makeRet(attr[2])

def p_exit_stmt(attr):
  'exitStatement 	: EXIT SEMICOLON'
  attr[0] = makeExit()

def p_compound_stmt(attr):
  'compoundStatement 	: LBRACE statementList RBRACE'
  attr[0] = attr[2]

def p_stmt_list_stmt(attr):
  'statementList   : statement'
  attr[0] = makeCmpd(None, attr[1])

def p_stmt_list(attr):
  'statementList : statementList statement'
  attr[0] = makeCmpd(attr[1], attr[2])

def p_expr(attr):
  'expr : simpleExpr'
  attr[0] = attr[1]

def p_expr_or(attr):
  'expr : expr OR simpleExpr'
  attr[0] = makeOr(attr[1], attr[3])

def p_expr_and(attr):
  'expr : expr AND simpleExpr'
  attr[0] = makeAnd(attr[1], attr[3])

def p_expr_not(attr):
  'expr : NOT simpleExpr'
  attr[0] = makeNot(attr[2])

def p_simple_expr(attr):
  'simpleExpr	: addExpr'
  attr[0] = attr[1]

def p_simple_expr_eq(attr):
  'simpleExpr	: simpleExpr EQ addExpr'
  attr[0] = makeEq(attr[1], attr[3])

def p_simple_expr_ne(attr):
  'simpleExpr	: simpleExpr NE addExpr'
  attr[0] = makeNe(attr[1], attr[3])

def p_simple_expr_le(attr):
  'simpleExpr	: simpleExpr LE addExpr'
  attr[0] = makeLe(attr[1], attr[3])

def p_simple_expr_lt(attr):
  'simpleExpr	: simpleExpr LT addExpr'
  attr[0] = makeLt(attr[1], attr[3])

def p_simple_expr_ge(attr):
  'simpleExpr	: simpleExpr GE addExpr'
  attr[0] = makeGe(attr[1], attr[3])

def p_simple_expr_gt(attr):
  'simpleExpr	: simpleExpr GT addExpr'
  attr[0] = makeGt(attr[1], attr[3])

def p_add_expr(attr):
  'addExpr		:  mulExpr'
  attr[0] = attr[1]

def p_add_expr_plus(attr):
  'addExpr :  addExpr PLUS mulExpr'
  attr[0] = makeAdd(attr[1], attr[3])
            
def p_add_expr_minus(attr):
  'addExpr :  addExpr MINUS mulExpr'
  attr[0] = makeSub(attr[1], attr[3])

def p_mul_expr(attr):
  'mulExpr	:  factor'
  attr[0] = attr[1]

def p_mul_expr_times(attr):
  'mulExpr	:  mulExpr TIMES factor'
  attr[0] = makeMul(attr[1], attr[3])


def p_mul_expr_div(attr):
  'mulExpr	:  mulExpr DIVIDE factor'
  attr[0] = makeDiv(attr[1], attr[3])
				
def p_factor_var(attr):
  'factor  : variable'
  attr[0] = attr[1]
				
def p_factor_const(attr):
  'factor  : constant'
  attr[0] = attr[1]
				
def p_factor_func(attr):
  'factor  : IDENTIFIER LPAREN RPAREN'
  attr[0] = makeFcall(attr[1], makeElist(None, None))
				
def p_factor_func_args(attr):
  'factor  : IDENTIFIER LPAREN argList RPAREN'
  attr[0] = makeFcall(attr[1], attr[3])
				
def p_factor_expr(attr):
  'factor  : LPAREN expr RPAREN'
  attr[0] = attr[2]

def p_variable(attr):
  'variable 	: IDENTIFIER'
  attr[0] = makeVarref(attr[1])

def p_variable_array(attr):
  'variable 	: IDENTIFIER LBRACKET expr RBRACKET' 
  attr[0] = makeArrayref(attr[1], attr[3])  

def p_string_const(attr):
  'stringConstant : STRING'
  attr[0] = makeStr(attr[1])

def p_float_const(attr):
  'constant : FLOATCON'
  attr[0] = makeFcon(attr[1])

def p_int_const(attr):
  'constant : INTCON'
  attr[0] = makeIcon(attr[1])

def p_char_const(attr):
  'constant : CHARCON'
  attr[0] = makeCcon(attr[1])

def p_arg_list_arg(attr):
  'argList : expr'
  attr[0] = makeElist(None, attr[1])


def p_arg_list(attr):
  'argList : argList COMMA expr'
  attr[0] = makeElist(attr[1], attr[3])

def p_error(t):
    raise RuntimeError("File: "+filename+", line "+str(t.lexer.lineno)+":syntax error ")


def parse_program(fn):
  global filename
  filename = fn
  parser = yacc.yacc()
  with open(filename, 'r') as file:
    data = file.read()
  root = parser.parse(data)
  
  type_checker(root)

  return root


def compile_program(fn):
  global filename
  filename = fn
  parser = yacc.yacc()
  with open(filename, 'r') as file:
    data = file.read()
  root = parser.parse(data)
  
  type_checker(root)
  asm_fn = fn.replace("input", "output").replace(".cm", ".s")
  asm(asm_fn, root)

  return "Success"

  