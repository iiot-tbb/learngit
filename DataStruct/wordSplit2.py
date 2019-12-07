#!/usr/bin/env python
# coding=utf-8

class Solution:
    def wordBreak(self,s,wordDict):
        len_s=len(s)
        sentence_list = []
        senslice=""
        if len_s == 0:
            return len_s
        def deepSeek(sentence_slice=None,begin=0):
            if begin >= len_s:
                sentence_list.append(sentence_slice)
                sentence_slice =None
                return
            #print("fdf")
            for end in range(begin+1,len_s+1):
                if s[begin:end] in wordDict:
                    lens = len(sentence_slice)
                    if sentence_slice != "":
                        sentence_slice+=" "
                    sentence_slice += s[begin:end]
                    deepSeek(sentence_slice,end)
                    sentence_slice =sentence_slice[:lens]

                if end == len_s:
                    print(sentence_slice)
                    print("reach the end")
                    sentence_slice=""
        deepSeek(senslice)
        print(sentence_list)
        return sentence_list

class Solution2:
    def wordBreak(self,s:str,wordDict:list)-> list:
        if not s:
            return []
        _len,wordDict = len(s),set(wordDict) #转换成字典用于0（1）判断in
        _min,_max = 2147483647,-2147483648
        for word in wordDict:
            _min = min(_min,len(word))
            _max = max(_max,len(word))

        def dfs(start): #返回s[start:]能由字典构成的所有句子
            if start not in memo:
                res = []
                for i in range(_min,min(_max,_len - start) +1): 剪枝，只考虑从最小长度到最大长度查找字典
                    if s[start:start+i] in wordDict: #找到了
                        res.extend(list(map(lambda x : s[start:start+i]+' '+x,dfs(start+i)))) #添加
                memo[start] = res #加入记忆
            return memo[start]

        memo = {_len:['']} #初始化记忆存储
        return list(map(lambda x:x[:-1],dfs(0)))#去掉末尾多出来的一个空格
    


if __name__ == "__main__":
    #Solv = Solution()
    #s= "pineapplepenapple"
    #s = "catsanddog"
    #wordDict = ["apple","pen","applepen","pine", "pineapple"]
    #wordDict = {"cat", "cats","and","sand","dog"}
    #Solv.wordBreak(s,wordDict)
    print(0x7fffffff)
    print(0xffffffff)
