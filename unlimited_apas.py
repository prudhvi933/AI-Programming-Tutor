import streamlit as st
import tempfile
import os
from datetime import datetime
import subprocess
import sys
import json
import re

try:
    import requests
except ImportError:
    st.error("Install: pip install requests")
    st.stop()

st.set_page_config(
    page_title="AI Programming Tutor",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'submission_history' not in st.session_state:
    st.session_state.submission_history = []
if 'custom_questions' not in st.session_state:
    st.session_state.custom_questions = {}

# FIXED DARK THEME CSS
st.markdown("""
<style>
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff !important;
        padding: 2rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* ALL TEXT - FORCE WHITE */
    p, span, div, label, li {
        color: #ffffff !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #00ff88 !important;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        font-family: 'Courier New', monospace;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00ff88 0%, #00d4ff 100%) !important;
        color: #0a0a0a !important;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-family: 'Courier New', monospace;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #00d4ff 0%, #00ff88 100%) !important;
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.6);
        transform: translateY(-2px);
    }

    /* FIXED: Text inputs - WHITE TEXT ON DARK */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 2px solid #00ff88 !important;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 1.1rem !important;
        padding: 0.75rem !important;
        caret-color: #00ff88 !important;
    }

    /* Focus state */
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        background-color: #252540 !important;
        border-color: #00d4ff !important;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.3) !important;
        outline: none !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #888888 !important;
        opacity: 1 !important;
    }

    /* Text area specific - for code input */
    .stTextArea textarea {
        background-color: #1a1a2e !important;
        color: #00ff88 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 1rem !important;
        line-height: 1.5 !important;
        tab-size: 4 !important;
        -moz-tab-size: 4 !important;
    }

    /* Select boxes */
    .stSelectbox > div > div > select,
    .stSelectbox > div > div > div {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 2px solid #00ff88 !important;
    }

    /* Multiselect */
    .stMultiSelect > div > div {
        background-color: #1a1a2e !important;
        border: 2px solid #00ff88 !important;
    }

    .stMultiSelect span {
        color: #ffffff !important;
    }

    .stMultiSelect [data-baseweb="tag"] {
        background-color: #00ff88 !important;
        color: #0a0a0a !important;
        font-weight: bold !important;
    }

    /* Code blocks */
    .stCodeBlock {
        background-color: #0d1117 !important;
        border: 2px solid #00ff88 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    .stCodeBlock code {
        color: #00ff88 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 1rem !important;
        background-color: #0d1117 !important;
    }

    pre {
        background-color: #0d1117 !important;
        color: #00ff88 !important;
        border: 2px solid #00ff88 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    pre code {
        color: #00ff88 !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #1e1e1e, #2a2a3e) !important;
        color: #ffffff !important;
        border: 2px solid #00ff88 !important;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 1.1rem !important;
    }

    .streamlit-expanderContent {
        background-color: #1a1a2e !important;
        border: 2px solid #00ff88 !important;
        border-left: 4px solid #00ff88 !important;
        color: #ffffff !important;
    }

    .streamlit-expanderContent p,
    .streamlit-expanderContent span,
    .streamlit-expanderContent strong {
        color: #ffffff !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00ff88 !important;
        font-family: 'Courier New', monospace;
        font-size: 2.5rem !important;
        font-weight: bold !important;
    }

    [data-testid="stMetricLabel"] {
        color: #00d4ff !important;
        font-family: 'Courier New', monospace;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }

    /* Success/Error/Info boxes */
    .stSuccess {
        background-color: #1a3a1a !important;
        color: #00ff88 !important;
        border-left: 4px solid #00ff88 !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }

    .stSuccess p, .stSuccess span {
        color: #00ff88 !important;
    }

    .stError {
        background-color: #3a1a1a !important;
        color: #ff6666 !important;
        border-left: 4px solid #ff4444 !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }

    .stError p, .stError span {
        color: #ff6666 !important;
    }

    .stInfo {
        background-color: #1a1a3a !important;
        color: #00d4ff !important;
        border-left: 4px solid #00d4ff !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }

    .stInfo p, .stInfo span {
        color: #00d4ff !important;
    }

    .stWarning {
        background-color: #3a3a1a !important;
        color: #ffdd00 !important;
        border-left: 4px solid #ffaa00 !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }

    .stWarning p, .stWarning span {
        color: #ffdd00 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1a2e;
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #2a2a3e !important;
        color: #ffffff !important;
        border: 2px solid #00ff88 !important;
        border-radius: 8px 8px 0 0;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 1.2rem !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #00ff88, #00d4ff) !important;
        color: #0a0a0a !important;
        font-weight: bold !important;
    }

    /* Title styling */
    .title-text {
        color: #00ff88 !important;
        font-size: 3.5rem !important;
        font-weight: bold;
        text-align: center;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.8);
        margin-bottom: 0.5rem;
    }

    .subtitle-text {
        color: #00d4ff !important;
        font-size: 1.3rem !important;
        text-align: center;
        font-family: 'Courier New', monospace;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ENHANCED JavaScript for TAB key support
st.components.v1.html("""
<script>
(function () {
    function enableTabOnce(textarea) {
        if (textarea.dataset.tabFixed) return;
        textarea.dataset.tabFixed = "true";

        textarea.addEventListener("keydown", function (e) {
            if (e.key === "Tab") {
                e.preventDefault();

                const start = this.selectionStart;
                const end = this.selectionEnd;
                const value = this.value;

                this.value =
                    value.substring(0, start) +
                    "    " +
                    value.substring(end);

                this.selectionStart = this.selectionEnd = start + 4;

                this.dispatchEvent(new Event("input", { bubbles: true }));
            }
        });
    }

    function scan() {
        const textareas = parent.document.querySelectorAll("textarea");
        textareas.forEach(enableTabOnce);
    }

    scan();
    setInterval(scan, 1000);
})();
</script>
""", height=0)


# ============================================================================
# ENHANCED ERROR MESSAGE EXTRACTOR
# ============================================================================
def clean_error_message(error_text):
    """Extract clean, user-friendly error message from Python traceback"""
    if not error_text:
        return "Execution failed"

    lines = error_text.split('\n')
    
    # Extract line number if present
    line_number = None
    for line in lines:
        if 'line' in line.lower():
            match = re.search(r'line (\d+)', line, re.IGNORECASE)
            if match:
                line_number = match.group(1)
                break
    
    # Look for the actual error
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
            
        # Extract error type and message
        error_patterns = [
            ('SyntaxError:', 'SyntaxError'),
            ('IndentationError:', 'IndentationError'),
            ('NameError:', 'NameError'),
            ('TypeError:', 'TypeError'),
            ('IndexError:', 'IndexError'),
            ('ValueError:', 'ValueError'),
            ('AttributeError:', 'AttributeError'),
            ('ZeroDivisionError:', 'ZeroDivisionError'),
            ('KeyError:', 'KeyError'),
            ('ImportError:', 'ImportError'),
        ]
        
        for pattern, error_type in error_patterns:
            if pattern in line:
                message = line.split(pattern)[-1].strip()
                if line_number:
                    return f"{error_type} (line {line_number}): {message}"
                return f"{error_type}: {message}"
    
    return "Execution error: Check your code syntax"

# ============================================================================
# ENHANCED AI FEEDBACK GENERATOR
# ============================================================================
def generate_feedback(code, test_results, question):
    """Generate intelligent AI feedback based on test results"""
    feedback = []
    
    passed = sum(1 for t in test_results if t['passed'])
    total = len(test_results)
    
    # Perfect solution
    if passed == total:
        return ["🎉 **PERFECT!** All test cases passed! Your solution is correct! 🎉"]
    
    feedback.append(f"### 🤖 AI TUTOR FEEDBACK ({passed}/{total} tests passed)\n")
    
    # Analyze the code structure
    has_function_def = f"def {question['function_name']}" in code
    has_return = "return" in code
    lines = code.split('\n')
    
    # Get error messages from failed tests
    error_messages = []
    for result in test_results:
        if not result['passed'] and result.get('actual'):
            error_messages.append(str(result['actual']))
    
    error_msg = '\n'.join(error_messages) if error_messages else ""
    
    # SYNTAX ERRORS
    if "SyntaxError" in error_msg or "IndentationError" in error_msg:
        feedback.append("## ❌ SYNTAX ERROR DETECTED\n")
        
        if "expected ':'" in error_msg or "expected \':\''" in error_msg:
            feedback.append("**Problem:** Missing colon `:` at end of function definition\n")
            feedback.append("**Wrong:**")
            feedback.append("```python")
            feedback.append(f"def {question['function_name']}({question['parameters']})  # ❌ Missing colon")
            feedback.append("    return result")
            feedback.append("```\n")
            feedback.append("**Correct:**")
            feedback.append("```python")
            feedback.append(f"def {question['function_name']}({question['parameters']}):  # ✅ Has colon")
            feedback.append("    return result")
            feedback.append("```")
            
        elif "IndentationError" in error_msg or "expected an indented block" in error_msg:
            feedback.append("**Problem:** Incorrect indentation\n")
            feedback.append("Python requires **4 spaces** (or 1 TAB) for indentation inside functions.\n")
            feedback.append("**Wrong:**")
            feedback.append("```python")
            feedback.append(f"def {question['function_name']}({question['parameters']}):")
            feedback.append("return result  # ❌ Not indented")
            feedback.append("```\n")
            feedback.append("**Correct:**")
            feedback.append("```python")
            feedback.append(f"def {question['function_name']}({question['parameters']}):")
            feedback.append("    return result  # ✅ Indented (press TAB key)")
            feedback.append("```\n")
            feedback.append("💡 **Tip:** Press the TAB key in the code editor for automatic indentation!")
            
        else:
            feedback.append("**Common syntax issues:**")
            feedback.append("- Missing colon `:` after `def`, `if`, `for`, `while`")
            feedback.append("- Unbalanced parentheses `()` or brackets `[]`")
            feedback.append("- Incorrect indentation (use TAB key)")
            feedback.append("- Missing quotes around strings")
    
    # FUNCTION DEFINITION ERRORS
    elif not has_function_def:
        feedback.append("## ❌ FUNCTION NOT FOUND\n")
        feedback.append(f"**Problem:** Missing or incorrect function name\n")
        feedback.append(f"**Expected:** `def {question['function_name']}({question['parameters']}):`\n")
        feedback.append("**Template:**")
        feedback.append("```python")
        feedback.append(f"def {question['function_name']}({question['parameters']}):")
        feedback.append("    # Your code here (press TAB for indentation)")
        feedback.append("    return result")
        feedback.append("```")
    
    # MISSING RETURN
    elif not has_return:
        feedback.append("## ❌ MISSING RETURN STATEMENT\n")
        feedback.append("**Problem:** Function doesn't return any value\n")
        feedback.append("**Solution:** Use `return` statement to return the result\n")
        feedback.append("```python")
        feedback.append(f"def {question['function_name']}({question['parameters']}):")
        feedback.append("    result = # your calculation")
        feedback.append("    return result  # ✅ Must return the answer")
        feedback.append("```")
    
    # NAME ERRORS
    elif "NameError" in error_msg:
        feedback.append("## ❌ NAME ERROR\n")
        if "not defined" in error_msg:
            # Extract the undefined name
            match = re.search(r"name '(\w+)' is not defined", error_msg)
            if match:
                undefined_name = match.group(1)
                feedback.append(f"**Problem:** Variable or function `{undefined_name}` is not defined\n")
                feedback.append("**Possible causes:**")
                feedback.append(f"- Typo in variable name (check spelling)")
                feedback.append(f"- Variable used before assignment")
                feedback.append(f"- Wrong function name (should be `{question['function_name']}`)")
            else:
                feedback.append("**Problem:** Using undefined variable or function\n")
                feedback.append("- Check spelling of all variables")
                feedback.append("- Make sure variables are assigned before use")
    
    # TYPE ERRORS
    elif "TypeError" in error_msg:
        feedback.append("## ❌ TYPE ERROR\n")
        if "missing" in error_msg and "argument" in error_msg:
            feedback.append(f"**Problem:** Wrong number of parameters\n")
            feedback.append(f"**Expected:** `{question['function_name']}({question['parameters']})`")
        elif "unsupported operand" in error_msg:
            feedback.append("**Problem:** Cannot perform operation on incompatible types\n")
            feedback.append("**Examples:**")
            feedback.append("- Can't add string and number: `'hello' + 5` ❌")
            feedback.append("- Convert first: `'hello' + str(5)` ✅")
            feedback.append("- Or: `int('5') + 5` ✅")
        else:
            feedback.append("**Problem:** Type incompatibility\n")
            feedback.append("**Type conversion functions:**")
            feedback.append("- `int()` - convert to integer")
            feedback.append("- `float()` - convert to decimal")
            feedback.append("- `str()` - convert to string")
            feedback.append("- `list()` - convert to list")
    
    # INDEX ERRORS
    elif "IndexError" in error_msg:
        feedback.append("## ❌ INDEX ERROR\n")
        feedback.append("**Problem:** Trying to access list element that doesn't exist\n")
        feedback.append("**Remember:** Python uses 0-based indexing")
        feedback.append("- List `[10, 20, 30]` has indices: 0, 1, 2")
        feedback.append("- Accessing index 3 causes IndexError\n")
        feedback.append("**Solution:** Check list length first")
        feedback.append("```python")
        feedback.append("if len(my_list) > index:")
        feedback.append("    value = my_list[index]")
        feedback.append("```")
    
    # ZERO DIVISION
    elif "ZeroDivisionError" in error_msg:
        feedback.append("## ❌ DIVISION BY ZERO\n")
        feedback.append("**Problem:** Cannot divide by zero!\n")
        feedback.append("**Solution:** Add check before division")
        feedback.append("```python")
        feedback.append("if denominator != 0:")
        feedback.append("    result = numerator / denominator")
        feedback.append("else:")
        feedback.append("    result = 0  # or handle error")
        feedback.append("```")
    
    # LOGIC ERRORS (some tests pass, some fail)
    elif passed > 0 and passed < total:
        feedback.append("## ⚠️ LOGIC ERROR\n")
        feedback.append(f"**Good news:** Your code works for {passed} out of {total} test cases!")
        feedback.append(f"**Problem:** Logic doesn't handle all cases correctly\n")
        feedback.append("**Check these edge cases:**")
        feedback.append("- 📌 Empty inputs: `[]`, `''`, `0`")
        feedback.append("- 📌 Negative numbers: `-5`, `-10`")
        feedback.append("- 📌 Single element: `[1]`, `'a'`")
        feedback.append("- 📌 Large numbers")
        feedback.append("- 📌 Special values: `None`, empty strings\n")
        feedback.append("**Tip:** Look at the failed test cases below to find the pattern!")
    
    # ALL TESTS FAILED
    else:
        feedback.append("## ❌ ALL TESTS FAILED\n")
        feedback.append("**Let's debug step by step:**\n")
        feedback.append("**1. Check function signature:**")
        feedback.append(f"   ✅ `def {question['function_name']}({question['parameters']}):`\n")
        feedback.append("**2. Check indentation:**")
        feedback.append("   ✅ All code inside function must be indented (press TAB)\n")
        feedback.append("**3. Check return statement:**")
        feedback.append("   ✅ Use `return` to return the result\n")
        feedback.append("**4. Review the problem:**")
        feedback.append(f"   ✅ {question['description']}\n")
        feedback.append("**Basic template:**")
        feedback.append("```python")
        feedback.append(f"def {question['function_name']}({question['parameters']}):")
        feedback.append("    # Step 1: Understand what inputs you have")
        feedback.append("    # Step 2: Process the inputs")
        feedback.append("    # Step 3: Return the result")
        feedback.append("    return result")
        feedback.append("```")
    
    # Category-specific tips
    feedback.append("\n---")
    feedback.append("## 💡 HELPFUL TIPS\n")
    
    if question['category'] == 'Lists':
        feedback.append("**📋 LIST OPERATIONS:**")
        feedback.append("- Check if empty: `if not my_list:` or `if len(my_list) == 0:`")
        feedback.append("- Loop through: `for item in my_list:`")
        feedback.append("- Access elements: `my_list[0]` (first), `my_list[-1]` (last)")
        feedback.append("- Length: `len(my_list)`")
        feedback.append("- Add item: `my_list.append(item)`")
        feedback.append("- Sum all: `sum(my_list)`")
        
    elif question['category'] == 'Strings':
        feedback.append("**📝 STRING OPERATIONS:**")
        feedback.append("- Length: `len(text)`")
        feedback.append("- Loop through: `for char in text:`")
        feedback.append("- Split into words: `text.split(' ')`")
        feedback.append("- Join words: `' '.join(words)`")
        feedback.append("- Uppercase: `text.upper()`, Lowercase: `text.lower()`")
        feedback.append("- Check if character: `char.isalpha()`, `char.isdigit()`")
        
    elif question['category'] == 'Math':
        feedback.append("**🔢 MATH OPERATIONS:**")
        feedback.append("- Division: `/` (decimal), `//` (integer)")
        feedback.append("- Remainder: `%` (modulo operator)")
        feedback.append("- Power: `**` (e.g., `2**3 = 8`)")
        feedback.append("- Loop range: `for i in range(1, n+1):`")
        feedback.append("- Absolute value: `abs(number)`")
        
    elif question['category'] == 'Basics':
        feedback.append("**🎯 PYTHON BASICS:**")
        feedback.append("- Operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`")
        feedback.append("- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`")
        feedback.append("- Logical: `and`, `or`, `not`")
        feedback.append("- If statement: `if condition:` (don't forget colon!)")
        feedback.append("- Always use `return` to return values")
    
    feedback.append("\n**🔍 Still stuck?** Click the '💡 SHOW HINTS' button below!")
    
    return feedback

# ============================================================================
# DEFAULT QUESTIONS
# ============================================================================
DEFAULT_QUESTIONS = {
    # BASICS (5)
    "sum_two": {
        "title": "Sum Two Numbers",
        "difficulty": "Easy",
        "category": "Basics",
        "description": "Write a function that adds two numbers and returns the sum.",
        "function_name": "sum_numbers",
        "parameters": "a, b",
        "test_cases": [
            {"input": "5, 3", "expected": "8"},
            {"input": "10, -5", "expected": "5"},
            {"input": "0, 0", "expected": "0"}
        ],
        "hints": [
            "Use the + operator to add two numbers",
            "Return the result using 'return' keyword",
            "Example: return a + b"
        ],
        "added_by": "System"
    },

    "multiply": {
        "title": "Multiply Numbers",
        "difficulty": "Easy",
        "category": "Basics",
        "description": "Multiply two numbers and return the result.",
        "function_name": "multiply",
        "parameters": "a, b",
        "test_cases": [
            {"input": "5, 3", "expected": "15"},
            {"input": "4, 0", "expected": "0"},
            {"input": "-2, 3", "expected": "-6"}
        ],
        "hints": [
            "Use * operator for multiplication",
            "Return the product directly",
            "Works with negative numbers too"
        ],
        "added_by": "System"
    },

    "is_even": {
        "title": "Check Even Number",
        "difficulty": "Easy",
        "category": "Basics",
        "description": "Return True if number is even, False otherwise.",
        "function_name": "is_even",
        "parameters": "n",
        "test_cases": [
            {"input": "4", "expected": "True"},
            {"input": "7", "expected": "False"},
            {"input": "0", "expected": "True"}
        ],
        "hints": [
            "Use modulo operator %",
            "Even numbers: n % 2 == 0",
            "Return True or False (boolean)"
        ],
        "added_by": "System"
    },

    "absolute": {
        "title": "Absolute Value",
        "difficulty": "Easy",
        "category": "Basics",
        "description": "Return absolute value without using abs().",
        "function_name": "absolute_value",
        "parameters": "n",
        "test_cases": [
            {"input": "-5", "expected": "5"},
            {"input": "3", "expected": "3"},
            {"input": "0", "expected": "0"}
        ],
        "hints": [
            "Check if number is negative: if n < 0",
            "If negative, multiply by -1",
            "If positive, return as is"
        ],
        "added_by": "System"
    },

    "power": {
        "title": "Calculate Power",
        "difficulty": "Easy",
        "category": "Basics",
        "description": "Calculate a^b without using ** or pow().",
        "function_name": "power",
        "parameters": "a, b",
        "test_cases": [
            {"input": "2, 3", "expected": "8"},
            {"input": "5, 2", "expected": "25"},
            {"input": "3, 0", "expected": "1"}
        ],
        "hints": [
            "Use a loop to multiply a by itself b times",
            "Start with result = 1",
            "Special case: any number^0 = 1"
        ],
        "added_by": "System"
    },

    # LISTS (5)
    "list_sum": {
        "title": "Sum of List",
        "difficulty": "Easy",
        "category": "Lists",
        "description": "Calculate sum of all numbers without using sum().",
        "function_name": "list_sum",
        "parameters": "numbers",
        "test_cases": [
            {"input": "[1, 2, 3, 4]", "expected": "10"},
            {"input": "[5, 5, 5]", "expected": "15"},
            {"input": "[]", "expected": "0"}
        ],
        "hints": [
            "Start with total = 0",
            "Loop through list: for num in numbers",
            "Add each number to total",
            "Handle empty list (returns 0)"
        ],
        "added_by": "System"
    },

    "find_max": {
        "title": "Find Maximum",
        "difficulty": "Easy",
        "category": "Lists",
        "description": "Find maximum number without using max().",
        "function_name": "find_max",
        "parameters": "numbers",
        "test_cases": [
            {"input": "[1, 5, 3, 9]", "expected": "9"},
            {"input": "[-1, -5, -3]", "expected": "-1"},
            {"input": "[42]", "expected": "42"}
        ],
        "hints": [
            "Initialize max_val with first element",
            "Loop through remaining elements",
            "Update max_val if current element is larger"
        ],
        "added_by": "System"
    },

    "find_min": {
        "title": "Find Minimum",
        "difficulty": "Easy",
        "category": "Lists",
        "description": "Find minimum number without using min().",
        "function_name": "find_min",
        "parameters": "numbers",
        "test_cases": [
            {"input": "[5, 1, 3, 9]", "expected": "1"},
            {"input": "[-1, -5, -3]", "expected": "-5"},
            {"input": "[42]", "expected": "42"}
        ],
        "hints": [
            "Initialize min_val with first element",
            "Loop through and compare",
            "Update if smaller value found"
        ],
        "added_by": "System"
    },

    "list_average": {
        "title": "Calculate Average",
        "difficulty": "Medium",
        "category": "Lists",
        "description": "Calculate average of numbers in list.",
        "function_name": "list_average",
        "parameters": "numbers",
        "test_cases": [
            {"input": "[2, 4, 6]", "expected": "4.0"},
            {"input": "[10, 20, 30]", "expected": "20.0"},
            {"input": "[100]", "expected": "100.0"}
        ],
        "hints": [
            "Sum all numbers first",
            "Divide by length of list",
            "Return as float (decimal number)"
        ],
        "added_by": "System"
    },

    "remove_duplicates": {
        "title": "Remove Duplicates",
        "difficulty": "Medium",
        "category": "Lists",
        "description": "Remove duplicates from list, preserve order.",
        "function_name": "remove_duplicates",
        "parameters": "numbers",
        "test_cases": [
            {"input": "[1, 2, 2, 3, 3]", "expected": "[1, 2, 3]"},
            {"input": "[5, 5, 5]", "expected": "[5]"},
            {"input": "[1, 2, 3]", "expected": "[1, 2, 3]"}
        ],
        "hints": [
            "Create empty result list",
            "Check if each item already in result",
            "Append only if not seen before"
        ],
        "added_by": "System"
    },

    # STRINGS (5)
    "reverse_string": {
        "title": "Reverse String",
        "difficulty": "Easy",
        "category": "Strings",
        "description": "Reverse a string without using [::-1].",
        "function_name": "reverse_string",
        "parameters": "text",
        "test_cases": [
            {"input": "'hello'", "expected": "olleh"},
            {"input": "'Python'", "expected": "nohtyP"},
            {"input": "'a'", "expected": "a"}
        ],
        "hints": [
            "Start with empty string result",
            "Loop through text backwards",
            "Or concatenate from end to start"
        ],
        "added_by": "System"
    },

    "str_length": {
        "title": "String Length",
        "difficulty": "Easy",
        "category": "Strings",
        "description": "Return string length without using len().",
        "function_name": "str_length",
        "parameters": "text",
        "test_cases": [
            {"input": "'hello'", "expected": "5"},
            {"input": "'ab'", "expected": "2"},
            {"input": "''", "expected": "0"}
        ],
        "hints": [
            "Start counter at 0",
            "Loop through each character",
            "Increment counter for each character"
        ],
        "added_by": "System"
    },

    "count_vowels": {
        "title": "Count Vowels",
        "difficulty": "Medium",
        "category": "Strings",
        "description": "Count vowels (a,e,i,o,u) in string.",
        "function_name": "count_vowels",
        "parameters": "text",
        "test_cases": [
            {"input": "'hello'", "expected": "2"},
            {"input": "'python'", "expected": "1"},
            {"input": "'aeiou'", "expected": "5"}
        ],
        "hints": [
            "Create vowels string: 'aeiouAEIOU'",
            "Loop through text characters",
            "Count if character is in vowels"
        ],
        "added_by": "System"
    },

    "is_palindrome": {
        "title": "Check Palindrome",
        "difficulty": "Medium",
        "category": "Strings",
        "description": "Check if string reads same forwards and backwards.",
        "function_name": "is_palindrome",
        "parameters": "text",
        "test_cases": [
            {"input": "'radar'", "expected": "True"},
            {"input": "'hello'", "expected": "False"},
            {"input": "'level'", "expected": "True"}
        ],
        "hints": [
            "Compare text with its reverse",
            "Or use two pointers from both ends",
            "Move pointers toward center"
        ],
        "added_by": "System"
    },

    "count_words": {
        "title": "Count Words",
        "difficulty": "Medium",
        "category": "Strings",
        "description": "Count words separated by spaces.",
        "function_name": "count_words",
        "parameters": "text",
        "test_cases": [
            {"input": "'hello world'", "expected": "2"},
            {"input": "'one'", "expected": "1"},
            {"input": "'a b c'", "expected": "3"}
        ],
        "hints": [
            "Use split() method",
            "Split by space character",
            "Count elements in resulting list"
        ],
        "added_by": "System"
    },

    # MATH (5)
    "factorial": {
        "title": "Calculate Factorial",
        "difficulty": "Medium",
        "category": "Math",
        "description": "Calculate n! = n × (n-1) × ... × 1",
        "function_name": "factorial",
        "parameters": "n",
        "test_cases": [
            {"input": "5", "expected": "120"},
            {"input": "3", "expected": "6"},
            {"input": "0", "expected": "1"}
        ],
        "hints": [
            "Start result at 1",
            "Loop from 1 to n",
            "Special case: 0! = 1"
        ],
        "added_by": "System"
    },

    "fibonacci": {
        "title": "Fibonacci Number",
        "difficulty": "Medium",
        "category": "Math",
        "description": "Return nth Fibonacci number (0,1,1,2,3,5,8...).",
        "function_name": "fibonacci",
        "parameters": "n",
        "test_cases": [
            {"input": "5", "expected": "5"},
            {"input": "7", "expected": "13"},
            {"input": "0", "expected": "0"}
        ],
        "hints": [
            "Start with a=0, b=1",
            "Loop n times",
            "Update: a, b = b, a+b"
        ],
        "added_by": "System"
    },

    "is_prime": {
        "title": "Check Prime Number",
        "difficulty": "Hard",
        "category": "Math",
        "description": "Check if number is prime (divisible only by 1 and itself).",
        "function_name": "is_prime",
        "parameters": "n",
        "test_cases": [
            {"input": "7", "expected": "True"},
            {"input": "10", "expected": "False"},
            {"input": "2", "expected": "True"}
        ],
        "hints": [
            "Numbers less than 2 are not prime",
            "Check divisibility from 2 to sqrt(n)",
            "If divisible by any, not prime"
        ],
        "added_by": "System"
    },

    "gcd": {
        "title": "Greatest Common Divisor",
        "difficulty": "Hard",
        "category": "Math",
        "description": "Find GCD of two numbers using Euclidean algorithm.",
        "function_name": "gcd",
        "parameters": "a, b",
        "test_cases": [
            {"input": "12, 8", "expected": "4"},
            {"input": "15, 25", "expected": "5"},
            {"input": "7, 13", "expected": "1"}
        ],
        "hints": [
            "While b != 0, calculate remainder",
            "Replace a with b, b with remainder",
            "Return a when b is 0"
        ],
        "added_by": "System"
    },

    "sum_of_squares": {
        "title": "Sum of Squares",
        "difficulty": "Medium",
        "category": "Math",
        "description": "Calculate sum of squares: num1² + num2² + ...",
        "function_name": "sum_of_squares",
        "parameters": "numbers",
        "test_cases": [
            {"input": "[1, 2, 3]", "expected": "14"},
            {"input": "[2, 2]", "expected": "8"},
            {"input": "[0, 5]", "expected": "25"}
        ],
        "hints": [
            "Start total at 0",
            "Loop through numbers",
            "Add num*num to total"
        ],
        "added_by": "System"
    }
}

def get_all_questions():
    """Combine default and custom questions"""
    all_q = DEFAULT_QUESTIONS.copy()
    all_q.update(st.session_state.custom_questions)
    return all_q

def run_code(code, test_input):
    """Execute code with test input"""
    try:
        test_code = code + f"\nprint({test_input})"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(test_code)
            temp_file = f.name

        process = subprocess.run(
            [sys.executable, temp_file], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        os.unlink(temp_file)

        return {
            'success': process.returncode == 0, 
            'output': process.stdout.strip(), 
            'error': process.stderr.strip()
        }
    except subprocess.TimeoutExpired:
        os.unlink(temp_file)
        return {'success': False, 'output': '', 'error': 'Timeout: Code took too long (5 second limit)'}
    except Exception as e:
        return {'success': False, 'output': '', 'error': f'Execution error: {str(e)}'}

def assess_code(code, question_id):
    """Assess code against test cases"""
    questions = get_all_questions()
    question = questions[question_id]
    results = []

    for i, test in enumerate(question['test_cases']):
        func_call = f"{question['function_name']}({test['input']})"
        result = run_code(code, func_call)

        passed = False
        actual_output = ""

        if result['success'] and result['output']:
            actual = result['output'].strip()
            expected = str(test['expected']).strip()

            if actual == expected:
                passed = True
                actual_output = actual
            else:
                try:
                    if eval(actual) == eval(expected):
                        passed = True
                        actual_output = actual
                    else:
                        actual_output = actual
                except:
                    actual_output = actual
        else:
            actual_output = clean_error_message(result['error'])

        results.append({
            'test_num': i + 1, 
            'input': test['input'], 
            'expected': test['expected'],
            'actual': actual_output, 
            'passed': passed
        })

    return results

# ============================================================================
# HEADER
# ============================================================================
st.markdown('<div class="title-text">⚡ AI PROGRAMMING TUTOR ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">// AI-Powered Feedback System //</div>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("## ⚙️ CONTROL PANEL")

    user_name = st.text_input("👤 USERNAME:", st.session_state.user_name, placeholder="Enter your name...")
    if user_name:
        st.session_state.user_name = user_name

    st.markdown("---")
    st.markdown("### 📊 STATS")

    questions = get_all_questions()
    st.metric("🎯 TOTAL", len(questions))
    st.metric("🔧 SYSTEM", len(DEFAULT_QUESTIONS))
    st.metric("🌟 CUSTOM", len(st.session_state.custom_questions))

    solved = len(set([s['question_id'] for s in st.session_state.submission_history if s['score'] == s['total']]))
    st.metric("✅ SOLVED", solved)

    st.markdown("---")

    if st.button("🔄 REFRESH"):
        st.rerun()

    if st.button("🗑️ CLEAR CUSTOM"):
        st.session_state.custom_questions = {}
        st.rerun()

    st.markdown("---")
    st.info("💡 **Tip:** Press TAB key in code editor for indentation!")

# ============================================================================
# MAIN TABS
# ============================================================================
tab1, tab2, tab3 = st.tabs(["💻 SOLVE", "➕ ADD", "📊 STATS"])

# TAB 1: SOLVE CHALLENGES
with tab1:
    st.markdown("## 💻 CHALLENGE ARENA")

    questions = get_all_questions()

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        categories = sorted(list(set([q['category'] for q in questions.values()])))
        selected_cat = st.multiselect("📁 CATEGORY:", categories, default=categories)
    with col2:
        difficulties = ["Easy", "Medium", "Hard"]
        selected_diff = st.multiselect("⚡ DIFFICULTY:", difficulties, default=difficulties)

    filtered = {qid: q for qid, q in questions.items() 
                if q['category'] in selected_cat and q['difficulty'] in selected_diff}

    st.info(f"🎯 {len(filtered)} CHALLENGES AVAILABLE")

    # Display questions
    for qid, q in filtered.items():
        is_custom = qid in st.session_state.custom_questions
        solved = any(s['question_id'] == qid and s['score'] == s['total'] 
                    for s in st.session_state.submission_history)

        icon = "🌟" if is_custom else "🔧"
        status = "✅" if solved else "📝"

        title = f"{status} {icon} {q['title']} [{q['difficulty']}] - {q['category']}"

        with st.expander(title):
            st.markdown(f"**📄 DESCRIPTION:** {q['description']}")
            st.markdown(f"**🔧 FUNCTION:** `{q['function_name']}({q['parameters']})`")

            st.markdown("**🧪 TEST CASES:**")
            for idx, test in enumerate(q['test_cases'], 1):
                st.code(f"Test {idx}: {q['function_name']}({test['input']}) → {test['expected']}", language="python")

            st.info("💡 **Tip:** Press TAB key for indentation (4 spaces)")

            code = st.text_area(
                "💻 YOUR CODE:", 
                height=300, 
                key=f"code_{qid}",
                placeholder=f"def {q['function_name']}({q['parameters']}):\n    # Write your solution here\n    # Press TAB for indentation\n    pass"
            )

            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("🚀 RUN TESTS", key=f"submit_{qid}", type="primary"):
                    if code.strip():
                        with st.spinner("⚡ EXECUTING CODE..."):
                            results = assess_code(code, qid)
                            passed = sum(1 for t in results if t['passed'])
                            total = len(results)

                            st.session_state.submission_history.append({
                                'timestamp': datetime.now(),
                                'question_id': qid,
                                'question_title': q['title'],
                                'score': passed,
                                'total': total,
                                'code': code
                            })

                            st.markdown("---")
                            
                            # Display metrics
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("✅ PASSED", f"{passed}/{total}")
                            with col2:
                                pct = (passed/total*100) if total > 0 else 0
                                st.metric("📊 SCORE", f"{pct:.0f}%")
                            with col3:
                                st.metric("🎯 STATUS", "✅ PASS" if passed == total else "❌ FAIL")

                            # Show test results
                            st.markdown("### 🧪 TEST RESULTS")
                            for test in results:
                                if test['passed']:
                                    st.success(f"✅ **TEST {test['test_num']}:** Input: `{test['input']}` → Output: `{test['actual']}` ✓")
                                else:
                                    st.error(f"❌ **TEST {test['test_num']}:** Input: `{test['input']}` | Expected: `{test['expected']}` | Got: `{test['actual']}`")

                            # AI FEEDBACK (only if not perfect)
                            if passed < total:
                                st.markdown("---")
                                feedback = generate_feedback(code, results, q)
                                
                                for line in feedback:
                                    st.markdown(line)
                                
                                # Show hints after feedback
                                if q.get('hints'):
                                    st.markdown("---")
                                    st.markdown("### 💡 ADDITIONAL HINTS")
                                    for i, hint in enumerate(q['hints'], 1):
                                        st.info(f"**HINT {i}:** {hint}")
                            else:
                                st.balloons()
                    else:
                        st.warning("⚠️ PLEASE WRITE SOME CODE FIRST!")

            with col_b:
                if st.button("💡 SHOW HINTS", key=f"hint_{qid}"):
                    st.markdown("### 💡 HINTS")
                    for i, hint in enumerate(q.get('hints', []), 1):
                        st.info(f"**{i}.** {hint}")

# TAB 2: ADD CUSTOM QUESTIONS
with tab2:
    st.markdown("## ➕ CREATE CHALLENGE")

    with st.form("add_q", clear_on_submit=True):
        st.markdown("### 📝 CHALLENGE INFO")

        col1, col2 = st.columns(2)

        with col1:
            q_id = st.text_input("🆔 ID (unique):", placeholder="my_challenge")
            q_title = st.text_input("📌 TITLE:", placeholder="My Challenge")
            q_difficulty = st.selectbox("⚡ DIFFICULTY:", ["Easy", "Medium", "Hard"])

        with col2:
            q_category = st.text_input("📁 CATEGORY:", placeholder="Math/Lists/Strings/Basics")
            q_func = st.text_input("🔧 FUNCTION NAME:", placeholder="my_function")
            q_params = st.text_input("📥 PARAMETERS:", placeholder="a, b")

        q_desc = st.text_area("📄 DESCRIPTION:", height=100, placeholder="Describe what the function should do...")

        st.markdown("### 🧪 TEST CASES")
        st.warning("⚠️ **IMPORTANT:** Enter inputs WITHOUT parentheses. E.g., '5, 3' not '(5, 3)'")

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            test1_in = st.text_input("INPUT 1:", key="t1i", placeholder="5, 3")
            test2_in = st.text_input("INPUT 2:", key="t2i", placeholder="10, -5")
            test3_in = st.text_input("INPUT 3 (optional):", key="t3i", placeholder="0, 0")
        with col_t2:
            test1_exp = st.text_input("EXPECTED 1:", key="t1e", placeholder="8")
            test2_exp = st.text_input("EXPECTED 2:", key="t2e", placeholder="5")
            test3_exp = st.text_input("EXPECTED 3 (optional):", key="t3e", placeholder="0")

        st.markdown("### 💡 HINTS (Optional)")
        hint1 = st.text_input("HINT 1:", placeholder="Start with...")
        hint2 = st.text_input("HINT 2:", placeholder="Consider...")
        hint3 = st.text_input("HINT 3:", placeholder="Don't forget...")

        submitted = st.form_submit_button("✅ CREATE CHALLENGE", type="primary")

        if submitted:
            if not all([q_id, q_title, q_func, q_params, q_desc, q_category, q_difficulty, test1_in, test1_exp, test2_in, test2_exp]):
                st.error("❌ PLEASE FILL ALL REQUIRED FIELDS!")
            elif q_id in get_all_questions():
                st.error(f"❌ ID '{q_id}' ALREADY EXISTS! Choose a different ID.")
            else:
                test_cases = [
                    {"input": test1_in.strip(), "expected": test1_exp.strip()},
                    {"input": test2_in.strip(), "expected": test2_exp.strip()}
                ]
                if test3_in.strip() and test3_exp.strip():
                    test_cases.append({"input": test3_in.strip(), "expected": test3_exp.strip()})

                hints = [h.strip() for h in [hint1, hint2, hint3] if h.strip()]
                if not hints:
                    hints = ["Try breaking down the problem into smaller steps"]

                new_q = {
                    "title": q_title,
                    "difficulty": q_difficulty,
                    "category": q_category,
                    "description": q_desc,
                    "function_name": q_func,
                    "parameters": q_params,
                    "test_cases": test_cases,
                    "hints": hints,
                    "added_by": st.session_state.user_name or "Anonymous"
                }

                st.session_state.custom_questions[q_id] = new_q

                st.success(f"✅ CHALLENGE '{q_title}' CREATED SUCCESSFULLY!")
                st.info("🔄 GO TO 'SOLVE' TAB TO SEE YOUR NEW CHALLENGE!")
                

# TAB 3: STATISTICS
with tab3:
    st.markdown("## 📊 PERFORMANCE METRICS")

    if st.session_state.submission_history:
        total_attempts = len(st.session_state.submission_history)
        perfect_scores = sum(1 for s in st.session_state.submission_history if s['score'] == s['total'])
        unique_solved = len(set([s['question_id'] for s in st.session_state.submission_history if s['score'] == s['total']]))

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📝 ATTEMPTS", total_attempts)
        with col2:
            st.metric("✅ PERFECT", perfect_scores)
        with col3:
            pct = (perfect_scores/total_attempts*100) if total_attempts > 0 else 0
            st.metric("📊 SUCCESS RATE", f"{pct:.1f}%")
        with col4:
            st.metric("🎯 UNIQUE SOLVED", unique_solved)

        st.markdown("---")
        st.markdown("### 📜 SUBMISSION HISTORY")
        
        for s in reversed(st.session_state.submission_history[-15:]):
            status = "✅" if s['score'] == s['total'] else "❌"
            time_str = s['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            score_str = f"{s['score']}/{s['total']}"
            
            col_a, col_b, col_c = st.columns([3, 1, 2])
            with col_a:
                st.write(f"{status} **{s['question_title']}**")
            with col_b:
                st.write(f"**Score:** {score_str}")
            with col_c:
                st.write(f"🕐 {time_str}")
            
            st.markdown("---")
    else:
        st.info("📈 NO SUBMISSIONS YET! Start solving challenges to see your stats!")
        st.markdown("### 🚀 Get Started")
        st.markdown("1. Go to the **SOLVE** tab")
        st.markdown("2. Choose a challenge")
        st.markdown("3. Write your solution")
        st.markdown("4. Click **RUN TESTS** to see results and AI feedback!")

# Footer
st.markdown("---")
questions_count = len(get_all_questions())
st.markdown(
    f"<p style='text-align: center; color: #00ff88; font-family: Courier; font-size: 1.2rem;'>"
    f"⚡ {questions_count} CHALLENGES // AI-POWERED FEEDBACK // TAB-KEY ENABLED ⚡"
    f"</p>", 
    unsafe_allow_html=True
)