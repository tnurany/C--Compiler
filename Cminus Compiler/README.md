[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/rwtl8aIH)
[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/rTDwB-7f)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=11443973&assignment_repo_type=AssignmentRepo)
# CminusAC: An Array and Control-flow Generator for Cminus

*Due Date*: Monday, November 30, 2023 @ 8am

## Purpose

The purpose of this project is to gain experience in giving meaning to a
programming language by generating x86-64 assembly for a subset of Cminus. Specifically,
you will be generating assembly for if-statements, while-loops and arrays.

#### Project Summary

In this project, you will add actions to the compiler developed in the previous project that will do the following

1. Generate assembly to test the results of an expression controlling an if-statement.
1. Generate assembly to branch through an if-then-else statement as determined by the controlling expression
1. Generate assembly to branch back to the beginning of and out of a while-loop as determined by the controlling expression.
1. Reserve space for an array of character, integers or floats.
1. Generate address arithmetic for an array reference.

Follow the methods given in class for generating code for if-statements, while-loops and arrays.



#### Requirements

All input for this project is provided in 
`input` directory. To run your compiler on the `test_if.cm` test case, for examle, type


```bash
    make test_if
```

#### Submission
Your code should be well-documented. You will submit all of your code via Github Classroom.
