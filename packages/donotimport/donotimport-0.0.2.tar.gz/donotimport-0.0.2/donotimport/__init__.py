#!/usr/bin/env python
# coding:utf-8
# Code by : Yasser BDJ
# E-mail  : yasser.bdj96@gmail.com
"""
#set:usage.py,examples.py,changelog.txt
##################################################################
# USAGE :
#s
import donotimport

#Your code is here without any import to any library
#e
##################################################################
# EXAMPLES :
#s

# Example:1
import donotimport

#For encryption
p1=ashar("123","Example:1").encode()
print(p1)
# OUTPUT:
'''
-If the library is already installed, the result will be:
25#;F7=04-62%12?11<F0[54{89(E5:00O15z1AbA6BABHA2r@204xC5H9Fx2FSCFt98X72)B0}65]BA>77!5F$D9&37_B3+001

-If the library is not installed, an error message will appear:
ashar not exist!
'''
#e
##################################################################
# CHANGELOG :
#s
## 0.0.2
- Fix Bugs.

## 0.0.1
- First public release.
#e
##################################################################
"""
# VALUES :
__version__="0.0.2"
__name__="donotimport"
__author__="Yasser Bdj (Boudjada Yasser)"
__author_email__="yasser.bdj96@gmail.com"
__github_user_name__="yasserbdj96"
__title__="donotimport"
__description__="A simple package to prevent the abusive use of the import statement in Python."
__author_website__=f"https://{__github_user_name__}.github.io/"
__source_code__=f"https://github.com/{__github_user_name__}/{__name__}"
__keywords__=[__github_user_name__,'python']
__keywords__.extend(__title__.split(" "))
__keywords__.extend(__description__.split(" "))
__install_requires__=['']
__Installation__="pip install "+__name__+"=="+__version__
__license__='MIT License'
__copyright__='Copyright © 2008->Present, '+__author__+"."
__license_text__=f'''MIT License

{__copyright__}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

You also agree that if you become very rich you will give me 1% of your wealth.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''
##################################################################
#s
import os
import sys

def rd(script_file):
    with open(script_file,'r') as file:
        data=file.read()
    exec(data)
pkgs=[]
errs=True
while errs==True:
    try:
        for i in range(len(pkgs)):
            try:
                exec(pkgs[i])
            except:
                pass
        os.system('cls' if os.name=='nt' else 'clear')
        rd(sys.argv[0])
        errs=False
    except Exception as err:
        err=str(err)
        if err[0:6]=="name '":
            try:
                exec('import '+err.split("'")[1])
            except:
                print("'"+err.split("'")[1]+"' not exist!")
                exit()
            pkgs.append('import '+err.split("'")[1])
        elif err=="'module' object is not callable":
            pkgs[i]='from '+pkgs[i].split(" ")[1]+' import '+pkgs[i].split(" ")[1]
        else:
            print(err)
            errs=False
exit()
#e