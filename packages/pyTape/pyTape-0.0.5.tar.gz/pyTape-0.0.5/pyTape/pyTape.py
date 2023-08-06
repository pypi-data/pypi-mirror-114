class Tape:
    reg=[0]
    ptr=0
    i=0
    loop=[]
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
            if (self.ptr+1)==len(self):
                self.reg.append(0)
            self.ptr+=1
        elif op=="<":
            if self.ptr!=0:self.ptr-=1
        elif op=="+":
            self[self.ptr]+=1
        elif op=="-":
            if self[self.ptr]!=0:self[self.ptr]-=1
        elif op==".":
            print(chr(self[self.ptr]),end="")
        elif op==",":
            self[self.ptr]=abs(int(input()))
        elif op=="*":
            self.reg=[0];self.ptr=0
        elif op=="?":
            print("ptr:{}".format(self.ptr))
        elif op=="[":
            if self[self.ptr]!=0:
                self.loop.append(self.i)
            else:
                trim=0
                for i in range(self.i,len(ins)):
                    if ins[i]=="[":
                        trim+=1
                    elif ins[i]=="]":
                        trim-=1
                    if trim==0:
                        self.i=i
                        break
        elif op=="]":
            self.i=self.loop.pop()-1
        elif op=="&":
            print(int(self.reg[self.ptr]),end="")
        elif op=="!":
            self.ptr=self.reg[self.ptr]
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