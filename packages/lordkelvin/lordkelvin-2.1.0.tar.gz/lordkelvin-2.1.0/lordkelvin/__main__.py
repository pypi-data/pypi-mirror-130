'''
High level python EVM interface

Usage:
  lordkelvin ( r | rundocker ) [<args>...]
  lordkelvin ( g | ganache  )
  lordkelvin ( b | balance  )  [ -q ] [ -j | +j ] <address>
  lordkelvin ( s | save     )  [ -q ] [ -j | +j ]               <contract> [--as=<x>] <address>
  lordkelvin ( d | deploy   )  [ -q ] [ -j | +j ] [--v=<value>] [--u=<unit>] <contract> [--as=<x>] [<args>...]
  lordkelvin ( t | transact )  [ -v ] [ -j | +j ] [--v=<value>] [--u=<unit>] <contract> <function> [<args>...]
  lordkelvin ( c | call     )  [ -q ] [ -j | +j ]               <contract> <function> [<args>...]
  lordkelvin ( a | address  )  [ -q ] [ -j | +j ]               <contract>
  lordkelvin -h | --help
  lordkelvin --version

Options:
  -h --help     Show this screen.
  -q            quiet mode
  -v            verbose mode
  +j            JSON on
  -j            JSON off
  --version     Show version.
'''
def _f(x):
    if x == 'true':
        return True
    if x == 'false':
        return False
    if x == 'null':
        return None
    if x.startswith('@@'):
        return _f(open(f'out/{x[2:]}.cta').read().strip())
    if x.startswith('@'):
        return _f(open(       x[1:]      ).read().strip())
    if x.startswith('~'):
        try:    return   -int(x[1:])
        except: pass
        try:    return -float(x[1:])
        except: pass
        pass
    try:    return   int(x)
    except: pass
    try:    return float(x)
    except: pass
    return x
def println(result, _json, quiet=False):
    if quiet:   pass        # do nothing
    elif _json: print(json.dumps(result))
    else:       print(result)
    return
def main():
    import os, sys, eth_account, docopt, json, lordkelvin as lk
    from functools import partial
    A = docopt.docopt(__doc__, version=lk.__version__)
    if      A['ganache'] or A['g']:
        a = ['bash', '-c', 'ganache-cli | tee g.log']
        os.execvp(a[0], a)
    elif  A['rundocker'] or A['r']:
        if  os.system('docker build . -t lk'):
            raise exit(1)
        p = os.path.realpath('.')
        a = f'docker run --rm -it -w{p} -v{p}:{p} --name lk lk'.split()
        os.execvp(a[0], a + A['<args>'])
        pass
    v = A['-v']
    q = A['-q']
    j = bool(A['+j'])
    nname  = A['--as']
    name   = A['<contract>']
    func   = A['<function>']
    value  = A['--v'] or 0
    unit   =   'wei'
    w3 = lk.w3_connect(None, onion=1)
    if not w3.isConnected():
        print('no connection')
        raise exit(1)
    if nname:
        lk.link_contract(name, nname)
        name = nname
        pass
    def execf(f, j, q):
        println(f(*[_f(x) for x in A['<args>']],
                  value = w3.toWei(value,unit)), j, q)
        pass
    if     A['deploy'] or A['d']:
        q = not v
        execf(partial(lordkelvin.deploy_contract, name),        j, q)
    elif A['transact'] or A['t']:
        q = not v
        execf(lk.wrap_contract(name).__getattr__(func), j, q)
    elif     A['call'] or A['c']:
        execf(lk.wrap_contract(name).__getattr__(func), j, q)
    elif     A['save'] or A['s']: lk.save_cta(name, A['<address>'])
    elif  A['address'] or A['a']: println(lk.cta(name),  j, q)
    elif  A['balance'] or A['b']: println(lk.balance(A['<address>']), j)
    else:
        print('dunno what to do', A)
        raise exit(1)
    pass
    
if __name__=='__main__': main()
