#!/usr/bin/env python
# coding=UTF-8

def checking_bash() :
    import os
    if not os.path.isfile("/bin/bash") :
        raise OSError

checking_bash()

def detect_onekey(allow_ctrlc=1) :
    """Detect a key pressing. Return the string of the key."""
    
    import os
    pressing = os.system(r"""bash -c read\ -srn1\ \;\ if\ \[\ \'x\$REPLY\'\ =\ \'x\'\ \]\ \;\ then\ exit\ 0\ \;\ fi\ \;\ if\ \[\ \'x\$REPLY\'\ =\ \'x\ \'\ \]\ \;\ then\ exit\ 32\ \;\ fi\ \;\ exit\ \$\(printf\ \'%d\'\ \\\'\"\$REPLY\"\)""")
    if pressing == 2 :
        if allow_ctrlc :
            return "\x03" # ^C
        else :
            raise KeyboardInterrupt
    else :
        return chr(int(pressing/256))

def detect_escape(allow_ctrlc=1) : # POSIX only
    """Detect Escape sequence(\\033). Return the string of whole sequence
(contains \\033). If it is not an escape sequence, returns ""."""
    
    res = ""
    if detect_onekey(allow_ctrlc) != "\033" :
        return res
    else :
        res += "\033"
        pl = detect_onekey(allow_ctrlc)
        res += pl
        if pl == "]" :
            while pl != "\x04" :
                pl = detect_onekey(allow_ctrlc)
                res += pl
        elif pl == "[" :
            pl = "0"
            while pl in "0123456789" :
                pl = detect_onekey(allow_ctrlc)
                res += pl
        return res

def detect_keys(keys,allow_ctrlc=1) :
    """Detect more keys pressing."""
    
    res = ""
    for i in range(keys) :
        res += detect_onekey(allow_ctrlc)
    return res
