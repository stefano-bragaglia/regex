# regex
Parsing RegEx's in Python
    
    brew install graphviz     # or install "dot" in any other way
    
    git clone https://github.com/stefano-bragaglia/regex.git
    
    cd regex
    
    virtualenv --python=python3.7 .env
    
    source .env/bin/activate
    
    pip install --pre pybuilder
    
    pyb install_dependencies
    
    pyb install 
    
    dotregex.py
    
    ls -al
    
Then, see the `.png`s just generated.

Notes:
* Dashed mean (potentially) *optional*
* Green means (potentially) *repeated*
* Blue means *greedy*
* Red means *negated*
* Sequence of atoms with arity 1 are collapsed

Reference:
* https://docs.python.org/3.8/library/re.html
* https://kean.github.io/post/lets-build-regex
* https://stackoverflow.com/questions/7657130/how-to-get-the-ast-of-a-regular-expression-string/21419351

Other potentially interesting projects:
* https://github.com/nicholaslocascio/deep-regex
* https://github.com/sdht0/automata-from-regex
* https://github.com/swisskyrepo/Vulny-Code-Static-Analysis

* https://github.com/DarkmatterVale/regex4dummies
* https://github.com/krzysiekfonal/grammaregex
* https://github.com/ramtinms/tokenquery
* https://github.com/madisonmay/CommonRegex