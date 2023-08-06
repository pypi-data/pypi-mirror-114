class Tape:
    reg=[0]
    ptr=0
    i=0
    def __init__(self):
        pass
    def __del__(self):
        pass
    def __setitem__(self,key,val):
        self.reg[key]=val
    def __call__(self,arg):
        self.exce(arg)
    __getitem__=lambda self,key:self.reg[key]
    __len__=lambda self:len(self.reg)
    def do(self,op,ins):
        if op==">":
            if (self.ptr+1)==len(self.reg):
                self.reg.append(0)
            self.ptr+=1
        elif op=="<":
            if self.ptr!=0:self.ptr-=1
        elif op=="+":
            self.reg[self.ptr]+=1
        elif op=="-":
            if self.reg[self.ptr]!=0:self.reg[self.ptr]-=1
        elif op==".":
            print(chr(self.reg[self.ptr]),end="")
        elif op==",":
            self.reg[self.ptr]=abs(int(input()))
        elif op=="*":
            self.reg=[0];self.ptr=0
        elif op=="?":
            print("ptr:{}".format(self.ptr))
        elif op=="[":
            loop=ins[self.i+1:].split("]")[0]
            while self.reg[self.ptr]:
                for each in loop:
                    self.do(each,loop)
            self.i=ins.find("]",self.i)
        elif op=="&":
            print(int(self.reg[self.ptr]),end="")
    def exce(self,ins):
        self.i=0
        while self.i<len(ins):
            self.do(ins[self.i],ins)
            self.i+=1
    def complete(self,lhs,rhs):
        if len(lhs)>len(rhs):
            for i in range(len(lhs)-len(rhs)):
                rhs.reg.append(0)
        elif len(lhs)<len(rhs):
            for i in range(len(rhs)-len(lhs)):
                lhs.reg.append(0)
    def __add__(self,other):
        temp=Tape()
        self.complete(self,other)
        for i in range(len(self)):
            temp(">")
            temp[i]=self[i]+other[i]
        return temp
    def __sub__(self,other):
        temp=Tape()
        self.complete(self,other)
        for i in range(len(self)):
            temp(">")
            temp[i]=abs(self[i]-other[i])
        return temp
    def __mul__(self,other):
        temp=Tape()
        self.complete(self,other)
        for i in range(len(self)):
            temp(">")
            temp[i]=self[i]*other[i]
        return temp
    def __truediv__(self,other):
        temp=Tape()
        self.complete(self,other)
        for i in range(len(self)):
            temp(">")
            temp[i]=int(self[i]/other[i])
        return temp
    def __mod__(self,other):
        temp=Tape()
        self.complete(self,other)
        for i in range(len(self)):
            temp(">")
            temp[i]=self[i]%other[i]
        return temp
    def __repr__(self):
        return str(self.reg)