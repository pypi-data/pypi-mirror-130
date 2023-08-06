#pyhdls 0.0.1
class tree:
    def __init__(self, n):
        self.left = None 
        self.right = None 
        if n == 1:
            return 
        else:
            right = n//2
            left = n - right 
            self.left = tree(left)
            self.right = tree(right)
            return 
    def show(self):
        print(self.left, self.right)
        if self.left != None:
            self.left.show() 
        if self.right != None:
            self.right.show()
