# printvars.py
from functools import reduce
from typing import Dict, Optional
from colorama import Fore, Back, Style

def _prettyprint(glvars: Dict[str, Dict[str, str]]):
    # print(str(glvars))
    global_vars = glvars.get("*", {})
    missing = get_missing_vars(glvars)
    for envtype in glvars:
        vars = glvars[envtype]
        if envtype != "*":
            vars = {**vars, **global_vars}
        printvars = []
        for v in vars:
            printvars.append(f"{v}='{vars[v]}';")
        printvars = sorted(printvars)
        printheader(envtype)
        print_missing(missing.get(envtype))
        print(f"\n🦁 {Fore.CYAN}{Style.BRIGHT}Exports{Style.NORMAL}\n")
        for p in printvars:
            print(f"export {p}")
        print(f"{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}\n🤖 {Style.BRIGHT}IntelliJ{Style.NORMAL}\n")
        intellij = "".join(printvars)
        print(f"{intellij}{Style.RESET_ALL}")
    print("\n")
    return

def get_missing_vars(glvars: Dict[str, Dict[str, str]]):
    def get_keys(ar: [str], k: str):
        if k != "*":
            return ar + list(glvars[k].keys())
        else:
            return ar

    all_values = set(dict.fromkeys(reduce(get_keys, glvars, [])))
    missingdict = {}
    for envtype in glvars:
        if envtype != "*":
            missingdict[envtype] = all_values - set(glvars[envtype])

    return missingdict

def printheader(envtype):
    if envtype == "*":
        envtype = "🌎 Global (only)"
    else:
        envtype = f"{envtype}"
    print(f"\n{Style.BRIGHT}{Fore.LIGHTYELLOW_EX}*****************************************")
    print(f"Environment: {envtype}")
    print(f"*****************************************{Style.NORMAL}")
    return

def print_missing(missing):
    if missing:
        print(f"\n{Style.BRIGHT}{Fore.LIGHTRED_EX}*****************************************")
        print(f"Missing variables: {','.join(missing)}")
        print(f"*****************************************{Style.NORMAL}")
        return
    return


