#!/usr/bin/env python
# coding=UTF-8

"""
Check the Python properties.
A Make-like output defined here.
Any Python version is supported this module.
"""

def check_exists(var) :
    """Check the variable. If it exists, return 1, otherwise return 0."""
    
    try :
        eval(var)
    except Exception :
        return 0
    return 1

def check_exists_echo(var, prefix="checking for ", suffix="...", yes=" yes\n",
                      no=" no\n") :
    from sys import stdout
    stdout.write(prefix+var+suffix)
    if check_exists(var) :
        stdout.write(yes)
        return 1
    else :
        stdout.write(no)
        return 0

def check_value(var) :
    class Error :
        __init__ = lambda self: None
    try :
        return eval(var)
    except Exception :
        return Error()

def check_value_echo(var, prefix="checking for ", suffix="...", rr=repr,
                     endfix="\n") :
    from sys import stdout
    stdout.write(prefix+var+suffix)
    res = check_value(var)
    stdout.write(rr(res))
    stdout.write(endfix)
    return res

def check_bool_echo(value, prefix="checking for ", suffix="...", yes=" yes\n",
                    no=" no\n") :
    from sys import stdout
    stdout.write(prefix+value+suffix)
    if eval(value) :
        stdout.write(yes)
        return 1
    else :
        stdout.write(no)
        return 0

def check_run(command) :
    """Check the command. If it run successfully, return 1, otherwise 0."""
    
    try :
        exec(command)
    except Exception :
        return 0
    return 1

def check_run_echo(command, prefix="checking for ", suffix="...", yes=" yes\n",
                   no=" no\n") :
    from sys import stdout
    stdout.write(prefix+command+suffix)
    if check_run(command) :
        stdout.write(yes)
        return 1
    else :
        stdout.write(no)
        return 0

class Check :
    def __init__(self) :
        self.__checks = []
    
    def __getitem__(self, index) :
        return self.__checks[index]
    
    def __delitem__(self, index) :
        del self.__checks[index]
    
    def add_exists(self, var) :
        self.__checks += [("exists", var)]
    
    def add_value(self, var) :
        self.__checks += [("value", var)]
    
    def add_bool(self, value) :
        self.__checks += [("bool", value)]
    
    def add_run(self, value) :
        self.__checks += [("run", value)]
    
    def check(self, echo=0) :
        res = ()
        for i in self.__checks :
            if i[0] == "exists" :
                if echo :
                    res += (check_exists_echo(i[1]),)
                else :
                    res += (check_exists(i[1]),)
            if i[0] == "value" :
                if echo :
                    res += (check_value_echo(i[1]),)
                else :
                    res += (check_value(i[1]),)
            if i[0] == "bool" :
                if echo :
                    res += (check_bool_echo(i[1]),)
                else :
                    res += (not(not(i[1])),)
            if i[0] == "run" :
                if echo :
                    res += (check_run_echo(i[1]),)
                else :
                    res += (check_run(i[1]),)
        return res
