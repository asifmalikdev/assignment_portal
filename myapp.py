class Solution():
    def stringToInteger(self, s):
        s.strip()
        if not s:
            return 0
        sign = 1
        index =0
        if s[0]=='-':
            sign=-1
            index = 1
        elif s[0]=='+':
            index =1
        res = 0
        while index <len(s) and s[index].isdigit():
            res = (res *10) + int(s[index])
            index+=1
        return sign*res


obj = Solution()
print('anser is ', obj.stringToInteger('-234hwr'))