from bit import Key
from bit.format import bytes_to_wif
import multiprocessing
from multiprocessing import Pool
import atexit
from time import time
from datetime import timedelta, datetime

def seconds_to_str(elapsed=None):
    if elapsed is None:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    else:
        return str(timedelta(seconds=elapsed))


def log(txt, elapsed=None):
    colour_cyan = '\033[36m'
    colour_reset = '\033[0;0;39m'
    colour_red = '\033[31m'
    print('\n ' + colour_cyan + '  [TIMING]> [' + seconds_to_str() + '] ----> ' + txt + '\n' + colour_reset)
    if elapsed:
        print("\n " + colour_red + " [TIMING]> Elapsed time ==> " + elapsed + "\n" + colour_reset)


def end_log():
    end = time()
    elapsed = end-start
    log("End Program", seconds_to_str(elapsed))


start = time()
atexit.register(end_log)
log("Start Program")
print("Loading Puzzle TXT Please Wait and Good Luck...")  
filename ='puzzle.txt'
with open(filename) as f:
    add = f.read().split()
add = set(add)
       

x=int(input("'start range Min 1-115792089237316195423570985008687907852837564279074904382605163141518161494335 -> "))
y=int(input("stop range Max 115792089237316195423570985008687907852837564279074904382605163141518161494336 -> "))

# Add type hints and initialize variables properly
cores = 1  # type: int
r = 0      # type: int

def seek(r):
    F = []
    P = x
    while P<y:
            P+=1
            ran = P    
            key1 = Key.from_int(ran)
            wif = bytes_to_wif(key1.to_bytes(), compressed=False) #Uncompressed WIF
            wif2 = bytes_to_wif(key1.to_bytes(), compressed=True) #compressed WIF
            key2 = Key(wif)
            caddr = key1.address #Legacy compressed address
            uaddr = key2.address #Legacy uncompressed address
            myhex = "%064x" % ran
            private_key = myhex[:64]
            # Replace file handling with context manager
            if caddr in add:
                print (seconds_to_str(), "Nice One Found!!!",ran, caddr, wif2, private_key) #Legacy compressed address
                s1 = str(ran)
                s2 = caddr
                s3 = wif2
                s4 = private_key
                with open("CompressedWinner.txt", "a") as f:
                    f.write(f"{s1}:{s2}:{s3}:{s4}\n")
                continue
            
            if uaddr in add:
                print (seconds_to_str(), "Nice One Found!!!",ran, uaddr, wif, private_key) #Legacy uncompressed address
                s1 = str(ran)
                s2 = uaddr
                s3 = wif
                s4 = private_key
                with open("UncompressedWinner.txt", "a") as f:
                    f.write(f"{s1}:{s2}:{s3}:{s4}\n")
                continue
            else:
                colour_cyan = '\033[36m'
                colour_reset = '\033[0;0;39m'
                colour_red = '\033[31m'
                print (colour_cyan + seconds_to_str() + colour_red + " -----Sequential Search for Bitcoin Puzzle Wallets----- " + colour_cyan + myhex, end='\r'  + colour_reset) # Running Display Output



#CPU Control Command
# Add proper process cleanup
if __name__ == '__main__':
    try:
        jobs = []
        for r in range(cores):
            p = multiprocessing.Process(target=seek, args=(r,))
            jobs.append(p)
            p.start()
        
        # Wait for all processes to complete
        for job in jobs:
            job.join()
    except KeyboardInterrupt:
        # Handle graceful shutdown
        for job in jobs:
            job.terminate()
