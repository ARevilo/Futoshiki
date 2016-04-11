# This is a cell in a Futoshiki, consisting of x, y coordinates (column and row) and a value. 
# All parameters are integers between 1..5, values can also be 0 indicating that the value is still unknown.

class cell:
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val
        self.options = [1,2,3,4,5]

    def getRow(self):
        return self.row
    
    def setRow(self, row):
        self.row = row
        
    def getCol(self):
        return self.col
    
    def setCol(self, col):
        self.col = col
        
    def getVal(self):
        return self.val
    
    def setVal(self, val):
        self.val = val  
        
    def clone(self): 
        return cell(self.row, self.col, self.val)

    def removeOption(self,option):
        for i in option:
            try:
                self.options.remove(i)
            except ValueError:
                pass

    def getOptions(self):
        if self.val!=0:
            return [self.val]
        else: return self.options
