################
# GATES
################

BUFF = lambda a : a
# and
AND = lambda a,b : a == True and b == True
# or
OR = lambda a,b: a == True or b == True
# not
NOT = lambda a : not a

# not and
NAND = lambda a,b : not AND(a,b)
# not or
NOR = lambda a,b : not OR(a,b)
# != 
XOR = lambda a,b : a != b
# ==
XNOR = lambda a,b : a == b

################
# LATCHES
################

# 0,0 hold
# 1,0 set
# 0,1 reset
# 1,1 invalid
class SRNOR():
    def __init__(self, q = True):
        self.s = False
        self.r = False
        self.q = q
        self.nq = not q
    def __str__(self):
        return str(self.q) + ' ' + str(self.nq)
    def __call__(self, s = False, r = False, excited = lambda: None):
        self.s = s
        self.r = r
        excited()
        self.nq = NOR(self.s, NOR(self.r, self.nq))
        self.q = NOR(self.r, self.nq)
        self.s = False
        self.r = False
        if self.q == self.nq:
            print('SRNOR latch invalid state reset')
            self.q = True
            self.nq = False
        #print(self)

# 1,1 hold
# 0,1 set
# 1,0 reset
# 0,0 invalid
class SRNAND():
    def __init__(self, q = True):
        self.s = False
        self.r = False
        self.q = q
        self.nq = not q
    def __str__(self):
        return str(self.q) + ' ' + str(self.nq)
    def __call__(self, s = False, r = False, excited = lambda: None):
        self.s = s
        self.r = r
        excited()
        self.q = NAND(self.s, NAND(self.r, self.q))
        self.nq = NAND(self.r, self.q)
        self.s = False
        self.r = False
        if self.q == self.nq:
            print('SRNAND latch invalid state reset')
            self.q = True
            self.nq = False
        #print(self)

# 0,0 hold
# 1,0 set
# 0,1 reset
# 1,1 reset
class SRANDOR():
    def __init__(self, q = True):
        self.s = False
        self.r = False
        self.q = q
    def __str__(self):
        return str(self.q)
    def __call__(self, s = False, r = False, excited = lambda: None, orexited = lambda: None):
        self.s = s
        self.r = r
        excited()
        sqor = OR(self.s, self.q)
        orexited()
        self.q = AND(sqor, NOT(self.r))
        self.s = False
        self.r = False
        #print(self)

# 0,0 hold
# 1,0 set
# 0,1 reset
# 1,1 toggle
class JKNOR():
    def __init__(self, q = True):
        self.j = False
        self.k = False
        self.q = q
        self.nq = not q
    def __str__(self):
        return str(self.q) + ' ' + str(self.nq)
    def __call__(self, j = False, k = False, excited = lambda: None):
        self.j = j
        self.k = k
        excited()
        if self.j == True and self.k == True:
            self.nq = not self.nq
            self.q = not self.q
        else: 
            self.nq = NOR(self.j, NOR(self.k, self.nq))
            self.q = NOR(self.k, self.nq)
        self.j = False
        self.k = False
        #print(self)

# 1,1 hold
# 0,1 set
# 1,0 reset
# 0,0 toggle
class JKNAND():
    def __init__(self, q = True):
        self.j = False
        self.k = False
        self.q = q
        self.nq = not q
    def __str__(self):
        return str(self.q) + ' ' + str(self.nq)
    def __call__(self, j = False, k = False, excited = lambda: None):
        self.j = j
        self.k = k
        excited()
        if self.j == False and self.k == False:  
            self.q = not self.q
            self.nq = not self.nq
        else: 
            self.q = NAND(self.j, NAND(self.k, self.q))
            self.nq = NAND(self.k, self.q)
        self.j = False
        self.k = False
        #print(self)

################
# FLIP-FLOP
# external timing clock
################

# 0,0 hold
# 1,0 set
# 0,1 reset
# 1,1 invalid
class SRNORff():
    def __init__(self, q = True):
        self.s = False
        self.r = False
        self.q = q
        self.nq = not q
    def __str__(self):
        return str(self.q) + ' ' + str(self.nq)
    def __call__(self, s = False, r = False, edge = lambda: None):
        self.s = s
        self.r = r
        edge()
        self.nq = NOR(self.s, NOR(self.r, self.nq))
        self.q = NOR(self.r, self.nq)
        if self.q == self.nq:
            print('SRNOR latch invalid state reset')
            self.q = True
            self.nq = False
        #print(self)

# 1,1 hold
# 0,1 set
# 1,0 reset
# 0,0 invalid
class SRNANDff():
    def __init__(self, q = True):
        self.s = False
        self.r = False
        self.q = q
        self.nq = not q
    def __str__(self):
        return str(self.q) + ' ' + str(self.nq)
    def __call__(self, s = False, r = False, edge = lambda: None):
        self.s = s
        self.r = r
        edge()
        self.q = NAND(self.s, NAND(self.r, self.q))
        self.nq = NAND(self.r, self.q)
        if self.q == self.nq:
            print('SRNAND latch invalid state reset')
            self.q = True
            self.nq = False
        #print(self)

# 0,0 hold
# 1,0 set
# 0,1 reset
# 1,1 reset
class SRANDORff():
    def __init__(self, q = True):
        self.s = False
        self.r = False
        self.q = q
    def __str__(self):
        return str(self.q)
    def __call__(self, s = False, r = False, edge = lambda: None, orexited = lambda: None):
        self.s = s
        self.r = r
        edge()
        sqor = OR(self.s, self.q)
        orexited()
        self.q = AND(sqor, NOT(self.r))
        #print(self)

# 0,0 hold
# 1,0 set
# 0,1 reset
# 1,1 toggle
class JKNORff():
    def __init__(self, q = True):
        self.j = False
        self.k = False
        self.q = q
        self.nq = not q
    def __str__(self):
        return str(self.q) + ' ' + str(self.nq)
    def __call__(self, j = False, k = False, edge = lambda: None):
        self.j = j
        self.k = k
        edge()
        if self.j == True and self.k == True:
            self.nq = not self.nq
            self.q = not self.q
        else: 
            self.nq = NOR(self.j, NOR(self.k, self.nq))
            self.q = NOR(self.k, self.nq)
        #print(self)

# 1,1 hold
# 0,1 set
# 1,0 reset
# 0,0 toggle
class JKNANDff():
    def __init__(self, q = True):
        self.j = False
        self.k = False
        self.q = q
        self.nq = not q
    def __str__(self):
        return str(self.q) + ' ' + str(self.nq)
    def __call__(self, j = False, k = False, edge = lambda: None):
        self.j = j
        self.k = k
        edge()
        if self.j == False and self.k == False:  
            self.q = not self.q
            self.nq = not self.nq
        else: 
            self.q = NAND(self.j, NAND(self.k, self.q))
            self.nq = NAND(self.k, self.q)
        #print(self)