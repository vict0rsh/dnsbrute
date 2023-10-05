import sys
import threading

import dns.resolver

resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8']

WDLIST = []

try:
    dom = sys.argv[1]
    wdlistpath = sys.argv[2]
    threads = int(sys.argv[3])
except:
    print("\nUsage: python dnsbrute.py domain.com wordlist.txt 3 < (THREADS)\n")
    sys.exit()

try:    
    with open(wdlistpath, "r") as wdlist:
        wdlist = wdlist.read().splitlines()
        for line in wdlist:
            WDLIST.append(line)
except:
    print("<<<<<<<< [ERRO] Você passou a wordlist corretamente?")
    sys.exit()

def check():
    try:
        results = resolver.resolve(dom, "A")
        if results:
            print("\nDomínio {} on-line, iniciando brute-force...\n".format(dom))
            print("Resultados:")
            for result in results:
                print("{} > {}".format(dom,result))
            return 1
        else:
            print("\n[ERRO] Domínio OFFLINE! Encerrando..\n")
            sys.exit()
    except:
        print("\n[ERRO] Domínio offline! Encerrando..\n")
        sys.exit()
        

        
def brutedns():
    while WDLIST:
        subdomain = WDLIST.pop(0) + "." + dom
        try: 
            results = resolver.resolve(subdomain, "A")
            for r in results:
                print("{} > {}".format(subdomain, r))
        except:
            pass
    

r = check()
if r == 1:
    THREADS = []
    for i in range(threads):
        thread = threading.Thread(target=brutedns)
        THREADS.append(thread)
    
    for thread in THREADS:
        thread.start()
    
    for thread in THREADS:
        thread.join()
    
    print("\nWordlist finalizada!")