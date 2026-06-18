# AI Programming Tutor

An AI-powered coding assessment platform that helps learners practice programming problems, receive automated feedback, analyze coding mistakes, and improve problem-solving skills through intelligent evaluation.

## Overview

Traditional coding platforms often provide only pass/fail results without explaining why a solution failed. This project addresses that problem by combining automated code execution, test case evaluation, and intelligent error analysis to provide personalized feedback to learners.

The platform acts as a virtual programming tutor that guides users through coding challenges while helping them understand and fix mistakes.

## Features

* Interactive coding challenges
* Automated code evaluation
* Secure code execution
* Intelligent error detection
* Personalized debugging suggestions
* Progress tracking dashboard
* Multiple difficulty levels
* Challenge management system
* Real-time assessment feedback

## Technologies Used

* Python
* Streamlit
* JSON
* Regular Expressions (Regex)
* HTML/CSS
* JavaScript
* Subprocess Module

## System Architecture

User Input
↓
Code Submission
↓
Execution Engine
↓
Test Case Validation
↓
Error Analysis
↓
Feedback Generation
↓
Performance Tracking

## Key Components

### Challenge Management

Stores coding problems with:

* Title
* Difficulty Level
* Category
* Description
* Test Cases
* Hints

### Code Execution Engine

Executes user-submitted Python code in an isolated environment using Python subprocesses and captures outputs, errors, and execution results.

### Automated Assessment System

Validates solutions against predefined test cases and generates pass/fail reports.

### Intelligent Error Analysis

Detects common programming errors such as:

* Syntax Errors
* Type Errors
* Name Errors
* Index Errors
* Indentation Errors
* ZeroDivision Errors

### Feedback Generator

Provides meaningful explanations and debugging suggestions rather than generic error messages.

## Installation

```bash
git clone https://github.com/prudhvi933/AI-Programming-Tutor.git
cd AI-Programming-Tutor
pip install -r requirements.txt
streamlit run app.py
```

## Future Improvements

* LLM-powered feedback generation
* Multi-language support
* Code complexity analysis
* AI-generated coding questions
* Personalized learning paths
* Plagiarism detection
* Cloud deployment

## Learning Outcomes

Through this project, I gained hands-on experience in:

* Python Development
* Streamlit Applications
* Automated Code Evaluation
* Error Analysis
* Educational Technology
* Software Architecture
* User Experience Design

## Author

Kandula Prudhvi

GitHub: https://github.com/prudhvi933
