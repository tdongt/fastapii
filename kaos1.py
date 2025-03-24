class TreeNode:
     def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

#
# Note: 类名、方法名、参数名已经指定，请勿修改
#
#
# 
# @param root TreeNode类  
# @return int整型二维数组
#
class Solution:
    def levelOrder(self, root) :
        # write code here
        if not root:
            return []
        res = []
        queue = [root]
        while queue:
            tmp = []
            for i in range(len(queue)):
                node = queue.pop(0)
                tmp.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            res.append(tmp)
        return res
a=Solution()
b=TreeNode(8)
b.left=TreeNode(17)
b.right=TreeNode(21)
b.left.left=TreeNode(18)
b.left.right=TreeNode(None)
b.right.left=TreeNode(None)
b.right.right=TreeNode(6)
print(type(b))
print(a.levelOrder(b))