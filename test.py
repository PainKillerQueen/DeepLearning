import numpy as np
from typing import List




class Model1() :
    def __init__(self, INPUT_NODE_NUM, L1_NODE_NUM, L2_NODE_NUM):
        self.INPUT_NODE_NUM = INPUT_NODE_NUM
        self.L1_NODE_NUM = L1_NODE_NUM
        self.L2_NODE_NUM = L2_NODE_NUM

        # Define Input
        self.X = np.zeros(INPUT_NODE_NUM)
        # Define L1
        self.W1 = np.random.rand(INPUT_NODE_NUM,L1_NODE_NUM)
        self.B1 = np.random.rand(L1_NODE_NUM)
        self.L1 = np.zeros(L1_NODE_NUM)
        # Define L2
        self.W2 = np.random.rand(L1_NODE_NUM,L2_NODE_NUM)
        self.B2 = np.random.rand(L2_NODE_NUM)
        self.L2 = np.zeros(L2_NODE_NUM)

        self.alpha = np.zeros(L2_NODE_NUM)

        # Define Answer
        self.Y = np.zeros(L2_NODE_NUM)

        
    def Calc(self) :
        # L1 calculation
        for i in range(self.L1_NODE_NUM):
            for j in range(self.INPUT_NODE_NUM):
                self.L1[i]+=self.W1[j][i]*self.X[j]
            self.L1[i]+=self.B1[i]
            self.L1[i]=self.ReLU(self.L1[i])

        # L2 calculation
        for i in range(self.L2_NODE_NUM) :
            for j in range(self.L1_NODE_NUM) :
                self.alpha[i]+=self.W2[j][i]*self.L1[j]
            self.alpha[i]=self.B2[i]
        softMax_partion_sum = sum(np.exp(self.alpha))
        softMax = lambda i : np.exp(self.alpha[i])/softMax_partion_sum
        for i in range(self.L2_NODE_NUM) : self.L2[i] = softMax(i)

    def setInput(self, x : List[int])->None:
        if (len(x) != self.INPUT_NODE_NUM) :
            print("Error!")
            return
        for i in range(self.INPUT_NODE_NUM):
            self.X[i] = x[i]

        # setAnswer
        self.Y.fill(0)
        decimal = sum(bit * (2 ** i) for i, bit  in enumerate(reversed(self.X)))
        if(decimal<self.L2_NODE_NUM) : self.Y[int(decimal)] = 1

    def update(self, eta):
        # W2
        for i in range(self.L1_NODE_NUM):
            for j in range(self.L2_NODE_NUM):
                self.W2[i][j] -= eta*(self.Y[j]-self.L2[j])*self.L1[i]
        # B2
        for j in range(self.L2_NODE_NUM):
            self.B2[j] -= eta*(self.Y[j]-self.L2[j])

        self.Calc()



        return

    def ReLU(self,x) :
        if x<0: return 0
        else  : return x

    def print_info(self):
        print("--------input--------\n",self.X)
        print("-------- L 1 --------\n","--- w1 ---\n",self.W1,"\n--- b1 ---\n",self.B1,"\n--- L1 ---\n",self.L1,"\n")
        print("-------- L 2 --------\n","--- w2 ---\n",self.W2,"\n--- b2 ---\n",self.B2,"\n--- L2 ---\n",self.L2,"\n")
        print("--------output--------\n",self.Y)


# main

class CMD() :
    def __init__(self):
        self.buffer = []
        self.command_log = []
        self.test = Model1(4,5,10)
    def Listen(self,line:str):
        self.command_log.append(line)
        for i in line.split(' '):
            self.buffer.append(i)
        match self.buffer[0]:
            case "set":
                self.test.setInput([int(x) for x in self.buffer if x.isdigit()])
            case "calc":
                self.test.Calc()
            case "print":
                self.test.print_info()
            case "exit" : return 0
            case _: return 100
        return 100

    def start(self) :
        while self.Listen(input()):self.buffer.clear()


cmd = CMD()
cmd.start()


