# Cminus: A Language for Practice Implementation

## Purpose
This document describes the Cminus programming language.  It is intended
to provide enough detail to allow implementation of a parser
(context-free analyzer).   This document contains information that relevant to the
some portions of each assignment in this course.  

## Introduction
Cminus is a programming language designed for practice implementation.
Cminus is an extremely simplified version of C in which one may perform simple
integer calculations.  Cminus is intended to be simple enough to implement in a
single semester by any student willing to put in some effort. Each feature
included in the language was added specifically to illustrate some
problem that arises in the design and implementation of a very simple compiler.

Cminus supports three basic data types: *integer*, *char* and *float*.  Each type may be aggregated
into a one dimensional array. The language is intended to be *strongly typed*; that is, the type
of each expression should be determinable at compile time. 
Since there is no *boolean* data type, integers are used as
logical values.

Control structures in Cminus are limited.  It has an *if* statement,
a *while* statement and a *compound*
statement.  In addition, there is support for procedure calls.

## Lexical Properties of Cminus

In this section, any sequence of characters denoted inside of a pair of `"`'s indicates the actual string literal found inside of the `"`'s.


1.  In Cminus, blanks are significant.
1.  In Cminus, all keywords are reserved; that is, the programmer cannot use a Cminus keyword as the name of a variable.

The valid keywords are:

$$\begin{array}{lcl}
\langle \mathrm{CHAR} \rangle & \rightarrow & \mathtt{"char"}\\
\langle \mathrm{ELSE} \rangle & \rightarrow & \mathtt{"else"}\\
\langle \mathrm{EXIT} \rangle & \rightarrow & \mathtt{"exit"}\\
\langle \mathrm{FLOAT} \rangle & \rightarrow & \mathtt{"float"}\\
\langle \mathrm{IF} \rangle & \rightarrow & \mathtt{"if"}\\
\langle \mathrm{INT} \rangle & \rightarrow & \mathtt{"int"}\\
\langle \mathrm{READ} \rangle & \rightarrow & \mathtt{"read"}\\
\langle \mathrm{RETURN} \rangle & \rightarrow & \mathtt{"return"}\\
\langle \mathrm{VOID} \rangle & \rightarrow & \mathtt{"void"}\\
\langle \mathrm{WHILE} \rangle & \rightarrow & \mathtt{"while"}\\
\langle \mathrm{WRITE} \rangle & \rightarrow & \mathtt{"write"}\\
\end{array}$$


(Note that Cminus is *case sensitive,* that is, the variable
`X` differs from `x`.  Thus, `if` is a keyword, but
`IF` can be a variable name.)
\newpage

1. The following special characters have meanings in a Cminus
program. 

$$\begin{array}{lcl}
\langle \mathrm{AND} \rangle & \rightarrow & \mathtt{"\&\&"}\\
\langle \mathrm{ASSIGN} \rangle & \rightarrow & \mathtt{"="}\\
\langle \mathrm{CM} \rangle & \rightarrow & \mathtt{","}\\
\langle \mathrm{DIVIDE} \rangle & \rightarrow & \mathtt{"/"}\\
\langle \mathrm{DQ} \rangle & \rightarrow & \mathtt{"""}\\
\langle \mathrm{EQ} \rangle & \rightarrow & \mathtt{"=="}\\
\langle \mathrm{GE} \rangle & \rightarrow & \mathtt{">="}\\
\langle \mathrm{GT} \rangle & \rightarrow & \mathtt{">"}\\
\langle \mathrm{LBR} \rangle & \rightarrow & \mathtt{"\{"}\\
\langle \mathrm{LBK} \rangle & \rightarrow & \mathtt{"["}\\
\langle \mathrm{LE} \rangle & \rightarrow & \mathtt{"<="}\\
\langle \mathrm{LP} \rangle & \rightarrow & \mathtt{"("}\\
\langle \mathrm{LT} \rangle & \rightarrow & \mathtt{"<"}\\
\langle \mathrm{MINUS} \rangle & \rightarrow & \mathtt{"-"}\\
\langle \mathrm{NE} \rangle & \rightarrow & \mathtt{"!="}\\
\langle \mathrm{NOT} \rangle & \rightarrow & \mathtt{"!"}\\
\langle \mathrm{OR} \rangle & \rightarrow & \mathtt{"||"}\\
\langle \mathrm{PLUS} \rangle & \rightarrow & \mathtt{"+"}\\
\langle \mathrm{RBR} \rangle & \rightarrow & \mathtt{"\}"}\\
\langle \mathrm{RBK} \rangle & \rightarrow & \mathtt{"]"}\\
\langle \mathrm{RP} \rangle & \rightarrow & \mathtt{")"}\\
\langle \mathrm{SC} \rangle & \rightarrow & \mathtt{";"}\\
\langle \mathrm{SQ} \rangle & \rightarrow & \mathtt{"'"}\\
\langle \mathrm{TIMES} \rangle & \rightarrow & \mathtt{"*"}\\
\end{array}$$

2.  Comments are delimited by the characters `/*` and `*/`.
A `/*` begins a comment; it is valid in no other context.
A `*/` ends a comment; it cannot appear inside a comment.
Comments may appear before or after any other token.

2.  Identifiers are written with upper and
lowercase letters 
The implementor may restrict the length of identifiers so long as
identifiers of at least 31 characters are legal.
Identifiers are definedas follows:

$$\begin{array}{l c l}
\langle \mathrm{LETTER} \rangle&\rightarrow&`"a"` \; \mid \; `"b"` \; \mid \; `"c"` \; \mid \; \cdots \; \mid \; `"z"` \; \mid \; `"A"` \; \mid \; `"B"` \; \mid \; \cdots \; \mid \; `"Z"`\\
\langle \mathrm{DIGIT} \rangle &\rightarrow&`"0"` \; \mid \; `"1"` \; \mid \; `"2"` \; \mid \; \cdots \; \mid \; `"9"`\\
\langle \mathrm{ID} \rangle &\rightarrow&\langle \mathrm{LETTER} \rangle \; (\langle \mathrm{LETTER} \rangle \; \mid \langle \mathrm{DIGIT} \rangle \; )^{*}\\
\end{array}$$


4.  Constants are defined as follows:

$$\begin{array}{l c l}
\langle \mathrm{POSITIVE} \rangle &\rightarrow&`"1"` \; \mid \; `"2"` \; \mid \; `"3"` \; \mid \; ... \; \mid \; `"9"`\\
\langle \mathrm{INTCON} \rangle &\rightarrow&\langle \mathrm{POSITIVE} \rangle \; \langle \mathrm{DIGIT} \rangle^{*} \; \mid \; `"0"`\\
\langle \mathrm{FLOATCON} \rangle  & \rightarrow & \langle \mathrm{INTCON} \rangle \; \langle \mathrm{DOT} \rangle \; (\langle \mathrm{DIGIT} \rangle)^*\\
\langle \mathrm{CHARCON} \rangle & \rightarrow & \langle \mathrm{SQ} \rangle \; \neg (\langle \mathrm{SQ} \rangle) \; \langle \mathrm{SQ} \rangle\\
\end{array}$$

Special string constants are acceptable in `write` statements:

$\langle \mathrm{STRING} \rangle \; \rightarrow \; \langle \mathrm{DQ} \rangle \; (\; \neg ( \; \langle \mathrm{DQ} \rangle\;)\;)^* \; \langle \mathrm{DQ} \rangle$


## Cminus Syntax
This section gives a syntactic description of Cminus.
The sections following the grammar provide implementation notes on the
various parts of the grammar.
The grammar, as stated, defines the language.  It may require some
massaging before implementation with any particular parser generator
system.
### BNF
The following grammar describes the context-free syntax of Cminus:

$$\begin{array}{ l c l}
\langle\mathrm{program}\rangle&\rightarrow& \langle \mathrm{procedures} \rangle\\ 
 & \mid & \langle \mathrm{declList} \rangle \; \langle \mathrm{procedures} \rangle\\
 & & \\
 \langle \mathrm{declList} \rangle & \rightarrow & \langle \mathrm{type} \rangle \; \langle \mathrm{identifierList} \rangle \; \langle \mathrm{SC}\rangle \\
 & \mid & \langle \mathrm{declList} \rangle \; \langle \mathrm{type} \rangle \; \langle \mathrm{identifierList} \rangle \; \langle \mathrm{SC} \rangle\\
  & & \\
\langle \mathrm{procedures} \rangle & \rightarrow & \langle \mathrm{procedureDecl} \rangle \; \langle \mathrm{procedures} \rangle\\
& &  \langle \mathrm{procedureDecl} \rangle\\
 & & \\
\langle \mathrm{procedureDecl} \rangle & \rightarrow & \langle \mathrm{procedureHead} \rangle \; \langle \mathrm{procedureBody} \rangle \\
 & & \\
\langle \mathrm{procedureHead} \rangle & \rightarrow & \langle \mathrm{functionDecl} \rangle \; \langle \mathrm{declList} \rangle \\
& \mid & \langle \mathrm{functionDecl} \rangle\\
 & & \\
\langle \mathrm{functionDecl} \rangle 	& \rightarrow &  \langle \mathrm{type} \rangle \; \langle \mathrm{ID} \rangle \; \langle \mathrm{LPAREN} \rangle \; \langle \mathrm{paramDeclList} \rangle \; \langle \mathrm{RPAREN} \rangle\\
& \mid &  \langle \mathrm{type} \rangle \; \langle \mathrm{ID} \rangle \; \langle \mathrm{LPAREN} \rangle \; \langle \mathrm{RPAREN} \rangle\\
 & & \\
\langle \mathrm{ProcedureBody} \rangle & \rightarrow & \langle \mathrm{LBRACE} \rangle \; \langle \mathrm{StatementList} \rangle \; \langle \mathrm{RBRACE} \rangle\\
 & & \\
\langle \mathrm{paramDeclList} \rangle & \rightarrow & \langle \mathrm{paramDeclList} \rangle \; \langle \mathrm{CM} \rangle \; \langle \mathrm{paramDecl} \rangle\\
& \mid & \langle \mathrm{paramDecl} \rangle\\
 & & \\
\langle \mathrm{paramDecl} \rangle & \rightarrow & \langle \mathrm{type} \rangle \; \langle \mathrm{varDecl} \rangle\\
 & & \\
\langle \mathrm{identifierList}\rangle&\rightarrow& \langle \mathrm{varDecl}\rangle \\
 & \mid &  \langle \mathrm{identifierList} \rangle \; \langle \mathrm{CM} \rangle \; \langle \mathrm{varDecl}\rangle \\
 & & \\
\langle\mathrm{varDecl}\rangle 	&\rightarrow& \langle\mathrm{ID}\rangle \\
 & \mid & \langle \mathrm{ID} \rangle \; \langle\mathrm{LBK}\rangle \; \langle\mathrm{INTCON}\rangle \; \langle\mathrm{RBK}\rangle\\ 
 & \mid & \langle \mathrm{ID} \rangle \; \langle\mathrm{LBK}\rangle \; \langle\mathrm{CHARCON}\rangle \; \langle\mathrm{RBK}\rangle\\ 
  & & \\
\langle \mathrm{type} \rangle&\rightarrow& \langle \mathrm{INT} \rangle\\
&\mid&\langle \mathrm{CHAR} \rangle\\
&\mid&\langle \mathrm{FLOAT} \rangle\\
&\mid&\langle \mathrm{VOID} \rangle\\
 & & \\
\langle\mathrm{statement}\rangle&\rightarrow&\langle \mathrm{assignment}\rangle \\
&\mid&\langle \mathrm{callStatement}\rangle \\
&\mid&\langle \mathrm{ifStatement}\rangle \\
&\mid&\langle \mathrm{whileStatement}\rangle\\
&\mid&\langle \mathrm{ioStatement}\rangle\\
&\mid&\langle \mathrm{returnStatement}\rangle\\
&\mid&\langle \mathrm{exitStatement}\rangle\\
&\mid&\langle \mathrm{cpdStatement}\rangle\\
 & & \\
\langle\mathrm{assignment}\rangle&\rightarrow&\langle \mathrm{variable}\rangle \; \langle \mathrm{ASSIGN} \rangle \; \langle \mathrm{expr}\rangle \; \langle \mathrm{SC} \rangle\\
 & &\\
\langle\mathrm{ifStatement}\rangle&\rightarrow&\langle \mathrm{IF} \rangle \; \langle \mathrm{LP} \rangle \; \langle\mathrm{ Expr}\rangle \; \langle \mathrm{RP} \rangle\;  \langle \mathrm{cpdStatement} \rangle \\
&\mid&\langle \mathrm{IF} \rangle \; \langle \mathrm{LP} \rangle \; \langle\mathrm{ Expr}\rangle \; \langle \mathrm{RP} \rangle\;  \langle \mathrm{cpdStatement} \rangle \; ( \; \langle \mathrm{ELSE} \rangle \; \langle \mathrm{cpdStatement} \rangle \; )?\\
 & &\\
\langle \mathrm{callStatement} \rangle & \rightarrow & \langle \mathrm{ID} \rangle \; \langle \mathrm{LP} \rangle \; \langle \mathrm{argList} \rangle \; \langle \mathrm{RP} \rangle \; \langle \mathrm{SC} \rangle \\
& \mid & \langle \mathrm{ID} \rangle \; \langle \mathrm{LP} \rangle \; \langle \mathrm{RP} \rangle \; \langle \mathrm{SC} \rangle \\
 & &\\
\langle \mathrm{whileStatement}\rangle&\rightarrow&\langle \mathrm{WHILE} \rangle \; \langle \mathrm{LP} \rangle \; \langle \mathrm{expr}\rangle \; \langle \mathrm{RP} \rangle \; \langle\mathrm{ Statement}\rangle\\
 & &\\
\langle \mathrm{ioStatement}\rangle&\rightarrow&\langle \mathrm{READ} \rangle \; \langle \mathrm{LP} \rangle \;  \langle \mathrm{variable}\rangle \; \langle \mathrm{RP} \rangle \; \langle \mathrm{SC} \rangle \\
&\mid&\langle \mathrm{WRITE} \rangle \; \langle \mathrm{LP} \rangle \; ( \; \langle \mathrm{expr}\rangle \; \mid \; \langle \mathrm{STRING}\rangle\;) \; \langle \mathrm{RP} \rangle \; \langle \mathrm{SC} \rangle\\
 & &\\
\langle \mathrm{returnStatement} \rangle &\rightarrow& \langle \mathrm{RETURN} \rangle \; \langle \mathrm{expr} \rangle \; \langle \mathrm{SC} \rangle\\
 & &\\
\langle \mathrm{exitStatement} \rangle &\rightarrow& \langle \mathrm{EXIT} \rangle \; \langle \mathrm{SC} \rangle\\
 & &\\
\langle \mathrm{cpdStatement}\rangle&\rightarrow&\langle \mathrm{LBR} \rangle \; \mathrm{statementList} \; \langle \mathrm{RBR} \rangle\\
 & & \\
\langle \mathrm{statementList} \rangle & \rightarrow & \langle \mathrm{statement} \rangle\\
& \mid & \langle \mathrm{statementList} \rangle \; \langle \mathrm{statement} \rangle\\
\end{array}$$

The grammar for expressions is:

$$\begin{array}{ l c l}
\langle \mathrm{expr}\rangle&\rightarrow &\langle \mathrm{simpleExpr}\rangle\\
&\mid&\langle \mathrm{NOT} \rangle \; \langle \mathrm{simpleExpr}\rangle\\
& \mid & \langle \mathrm{simpleExpr}\rangle \; \langle \mathrm{OR} \rangle \; \langle \mathrm{simpleExpr}\rangle\\
& \mid & \langle \mathrm{simpleExpr}\rangle \; \langle \mathrm{AND} \rangle \; \langle \mathrm{simpleExpr}\rangle\\
 & & \\
\langle \mathrm{simpleExpr} \rangle & \rightarrow & \langle \mathrm{addExpr} \rangle \\
 & \mid & \langle \mathrm{addExpr} \rangle \;  \langle \mathrm{EQ} \rangle \; \langle \mathrm{addExpr} \rangle\\
 & \mid & \langle \mathrm{addExpr} \rangle \;  \langle \mathrm{NE} \rangle \; \langle \mathrm{addExpr} \rangle\\
  & \mid & \langle \mathrm{addExpr} \rangle \;  \langle \mathrm{LE} \rangle \; \langle \mathrm{addExpr} \rangle\\
   & \mid & \langle \mathrm{addExpr} \rangle \;  \langle \mathrm{LT} \rangle \; \langle \mathrm{addExpr} \rangle\\
    & \mid & \langle \mathrm{addExpr} \rangle \;  \langle \mathrm{GE} \rangle \; \langle \mathrm{addExpr} \rangle\\
     & \mid & \langle \mathrm{addExpr} \rangle \;  \langle \mathrm{GT} \rangle \; \langle \mathrm{addExpr} \rangle\\
  & & \\    
\langle \mathrm{addExpr} \rangle & \rightarrow & \langle \mathrm{muilExpr} \rangle\\
 & \mid & \langle \mathrm{muilExpr} \rangle \; \langle \mathrm{PLUS} \rangle \;  \langle \mathrm{muilExpr} \rangle\\
 & \mid & \langle \mathrm{muilExpr} \rangle \; \langle \mathrm{MINUS} \rangle \;  \langle \mathrm{muilExpr} \rangle\\
 & & \\
\langle \mathrm{muilExpr} \rangle & \rightarrow & \langle \mathrm{factor} \rangle\\
 & \mid & \langle \mathrm{factor} \rangle \; \langle \mathrm{TIMES} \rangle  \; \langle \mathrm{factor} \rangle\\
& \mid & \langle \mathrm{factor} \rangle \; \langle \mathrm{DIVIDE} \rangle  \; \langle \mathrm{factor} \rangle \\
 & & \\
\langle \mathrm{factor}\rangle&\rightarrow&\langle \mathrm{variable}\rangle \\
&\mid& \langle \mathrm{constant} \rangle \\
&\mid& \langle \mathrm{ID} \rangle \; \langle \mathrm{LP} \rangle \; \langle \mathrm{argList} \rangle \; \langle \mathrm{RP} \rangle\\
&\mid& \langle \mathrm{ID} \rangle \; \langle \mathrm{LP} \rangle \; \langle \mathrm{RP} \rangle\\
&\mid& \langle \mathrm{LP} \rangle \; \langle \mathrm{expr}\rangle \; \langle \mathrm{RP} \rangle\\
 & & \\
\langle \mathrm{variable}\rangle&\rightarrow&\langle \mathrm{ID}\rangle\\
&\mid&\langle \mathrm{ID}\rangle \; \langle \mathrm{LBK} \rangle \; \langle \mathrm{expr}\rangle \; \langle \mathrm{RBK} \rangle\\
 & & \\
 \langle \mathrm{constant}\rangle&\rightarrow& \langle \mathrm{INTCON} \rangle\\
 &\mid& \langle \mathrm{CHARCON} \rangle \\ 
 &\mid& \langle \mathrm{FLOATCON} \rangle \\
 & & \\ 
 \langle \mathrm{argList} \rangle & \rightarrow & \langle \mathrm{expr} \rangle \\
  & \mid & \langle \mathrm{argList} \rangle \; \langle \mathrm{CM} \rangle \; \langle \mathrm{expr} \rangle\\
\end{array}$$

### Section Notes
#### Declarations
Cminus has four standard types: `int`, `char`, `void` and `float`.
Integers, characters and floats occupy a single machine ``word''.  Void types are only for procedures that do not return a value. The standard types may be composed into
a structured array type.  An identifier may represent one of six
types of objects:

1. an integer variable 
1. an integer array
1. a character variable
1. a character array
1. a floating point variable 
1. a floating point array

Identifiers are declared to be variables or arrays in a variable declaration.
Only singly dimensioned arrays are permitted in Cminus. Indexing begins at 0 as in C and Java.

*Example:*

```
int x,y;
int a[15];
float vector[100];
```

#### Function Declarations

The semantics of function definition are simple.
A function returns the value of the expression specified in
the first `return` statement that it executes.

*Example:*
```
int max (int a, int b) {
     if (a < b) {
          return b;
     }
     else {
          return a;
     }
}
```

#### Procedure Declarations

A procedure is declared as a function with a `void` return type. No return statement may appear in a procedure. 

*Example:*
```
void swap (int a[2]) {
     int temp; 

     temp = a[0];
     a[0] = a[1];
     a[1] = temp;
}
``` 

#### Assignment Statement

The assignment statement requires that the *left hand side*
(the $\langle \mathrm{variable} \rangle$ non-terminal) and *right hand side* (the $\langle \mathrm{expr} \rangle$
non-terminal) evaluate to have the same type.
If they have different types, either coercion is required or a
context-sensitive error has occurred.
The coercion rules for assignment are simple.
If both sides are numeric (of type `int` or `float`), the
right hand side is converted to the type of the left hand side.
If both sides are numeric (of type `int` or `char`), the
right hand side is converted to the type of the left hand side.

#### If Statement
The grammar for the `if-else` construct is written to eliminate the dangling else ambiguity.
This is done by forcing a $ \langle \mathrm{cpdStatement} \rangle$ in each of the then- and else-clauses.
To evaluate an if statement, the expression is evaluated.
For an integer value, Cminus defines `0` as *false*; any other
value is equivalent to *true*.

*Examples:*
```
if (c == d) { d = a; }
if (b == 0) { b = 2*a; } else { b = b/2; }
```
#### While Statement
The while statement provides a simple mechanism for iteration.
Cminus's while statement behaves like the while statement in many other
languages; it executes the statement in the loop's body until the
controlling expression becomes false. The controlling expression will be treated as a boolean value encoded
into an `int` expression.
#### Input-Output Statements
Cminus provides two primitives for input and output.
The `read` and `write` statements are intended to provide direct
access to primitives implemented in the target abstract machine.

*Examples:*
```
read (x);
write (x+y);
write ('error');
```
#### Return Statements
Cminus allows functions to return values. The type of the return value needs to be the same type as the type of the function, or it must be converted to that type.

*Example:*
```
int f() {
     return 7;
}
```
#### Exit Statement
An exit statement in Cminus exits the program completely.

#### Expressions
Cminus expressions compute simple values of type `int`, `char` or `float`
For both integer and floating point numbers,
arithmetic and comparison are defined.
##### *Coercion:*
The type rules are specified in the assignment for the type checker.

##### *Operator Precedence:*
Operator precedences in Cminus are specified in the table below.
Multiplication and division have the highest priority, `&&` and `||` have
the lowest. 

| Operator | Precedence |
| -------- | ---------- |
|`*, /`    |5 |
|`+, -`|4|
|`<, <=, =, >=, >, !=`|3|
|`!`|2|
|`&&, \|\|`|1|

Relational operators always produce an integer. 

##### *Booleans:* 
Because Cminus has no booleans, relational expressions are defined to
yield integer results.
Thus, a relational expression of the form
`a~==~b`
is considered to be an arithmetic expression whose value is `0`
if the relation does not hold and not `0` otherwise.
Hence, both the `if-else` and `while` statements test
integer values; the expression is considered *false* if it
evaluates to `0` and to *true* if it evaluates to anything else.
Consider the following example which tests for either of two conditions
being true:

```
read (a); read (b); read (c); read (d);
if ((a == b) + (c < d)) { write ('error'); }
```

Note that relational expressions should be enclosed in parentheses because
they have very low precedence.
In the above example, the special operator `||` could have been used.
In Cminus the operator `||` takes two integer operands. `||` produces the
result `0` if both operands evaluate to `0`;
otherwise, it produces `1`.
The operator `&&` evaluates to `1` if both operands are
nonzero; otherwise it evaluates to `0`.
The unary logical operator `!` evaluates to `1` if its argument
is zero and to `0` otherwise.

##### *Function/Procedure Invocation:*

Cminus uses parentheses to indicate invocation and square
brackets to indicate subscripting of an array.
This simplifies the grammar --- many languages use parentheses for both
purposes.Parameters are passed call-by-value. Note the the value of an array is the address of the array, just as in C.

## An Example Program
The following program represents a simple example program written in Cminus.
This program successively reads pairs of integers from the input file
and prints out their product.
```
int main() {
     int x, y;
     read(x); read(y);
     while ((x $!=$ 0) || (y $!=$ 0)) {
          write (x*y);
          read (x); read (y);
     }
     exit;
}
```