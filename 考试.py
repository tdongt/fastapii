class Solution:
    def canFormSquare(self, planks) :
        # write code here
        zc=0
        for i in planks:
            zc+=i
        print(zc)
        if zc%4==0:bc=zc/4
        else:return False
        sym=0
        sy=[]
        for i in planks:
            if i==bc:
                sym+=1
            else:
                sy.append(i)
        print(sy)
        print(sym)
        print(planks)
        if sym==4:
            return True

        print(sym)
        
a=Solution()
a.canFormSquare([1,1,2,2,2])