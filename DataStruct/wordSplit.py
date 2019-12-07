#!/usr/bin/env python
# coding=utf-8

class Solution:
    def wordBreak(self,s,wordDict):
        lenWord = len(s)
        begin = 0
        def deepFind(begin):
            if begin >= len(s):
                return True
            for end in range(begin+1,len(s)+1):
                split_s = s[begin:end]
                if split_s in wordDict:
                    judge = deepFind(end)
                    return judge
            return False


class Solution2:
    import functools
    wordDict = set(wordDict)
    if not wordDict:return not s
    #找最长单词的长度
    max_len = max(map(len,wordDict))
    @functools.lru_cache(None)
    def helper(s):
        #递归终止条件
        if not s:
            return True
        for i in range(len(s)):
            #判断是否满足条件
            if i < max_len and s[:i+1] in wordDict and helper(s[i+1:]):
                return True
        return False
    return helper(s)

class Solution3:
    def wordBreak(self,s,wordDict):
        n =len(s)
        if not wordDict:
            return not s
        dp = [False] * (n+1)
        dp[0]=True
        for i in range(1, n+1):
            for j in range(i-1,-1,-1):
                if dp[j] and s[j:i] in wordDict:
                    dp[i] = True
                    break
        return dp[-1]
        

