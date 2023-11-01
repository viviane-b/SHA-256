import math

# Message 1: M = 101010
M=101010
l=len(str(M))

# --------------------- Pre-processing ------------------
# 1. Padding

k=(448-(l+1))%512
M=str(M) + "1" + k*"0" + '{:064b}'.format(l)


# 2. Breaking message into blocks
tabM= [None]*(len(M)//512)
for m in range (len(tabM)):
    tabM[m]=[0]*16

N = len(M)//512
for i in range (1, (N+1)):
    for j in range (16):
        tabM[i-1][j]=M[32*j:32*(j+1)]
        # example: M_0^(i) = tabM[i][0], 1 <= i <= N



# 3. Initializing
tabH0=[0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
tabH = tabH0
# ----------------------- Compression function ----------------------------
# Operations, functions
# x, y, z: 32-bits words


def rotR(x, n):     # right binary rotation of n digits of x (32-bits word)
    return ((x>>n) | (x<<(32-n))) % 2**32


def sigma0(x):
    return rotR(x, 7) ^ rotR(x, 18) ^ x>>3

def sigma1(x):
    return rotR(x, 17) ^ rotR(x, 19) ^ rotR(x, 10)

def capSigma0(x):
    return rotR(x, 2) ^ rotR(x, 13) ^ rotR(x, 22)

def capSigma1(x):
    return rotR(x, 6) ^ rotR(x, 11) ^ rotR(x, 25)

def Ch(x, y, z):
    return (x&y) ^ (~x&z)
def Maj(x,y,z):
    return (x&y) ^ (x&z) ^ (y&z)


# Constants
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, \
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, \
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, \
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, \
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, \
     0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, \
     0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, \
     0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]


wordTab=[None]*64
for i in range (1, N):
    for j in range (16):
        wordTab[j]=tabM[i][j]

    for j in range (16, 64):
        wordTab[j]= (sigma1(wordTab[j-2]) + wordTab[j-7] + sigma0(wordTab[j-15]) + wordTab[j-16]) % 2**32

    a = tabH[0]
    b = tabH[1]
    c = tabH[2]
    d = tabH[3]
    e = tabH[4]
    f = tabH[5]
    g = tabH[6]
    h = tabH[7]


    for t in range (64):
        T1 = h + capSigma1(e) + Ch(e, f, g) + K[t] + wordTab[t]
        T2 = capSigma0(a) + Maj(a, b, c)
        h=g
        g=f
        f=e
        e=d+T1
        d=c
        c=b
        b=a
        a=T1+T2

    tabH[0] += a
    tabH[1] += b
    tabH[2] += c
    tabH[3] += d
    tabH[4] += e
    tabH[5] += f
    tabH[6] += g
    tabH[7] += h


# Final hash value
M= ""
for h in tabH:
    M += str(('{:032b}'.format(h)))

print("M= ", M, "\n length=", len(M))



