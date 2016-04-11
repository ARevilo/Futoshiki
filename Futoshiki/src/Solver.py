# Template for the algorithm to solve a Futoshiki. Builds a recursive backtracking solution
# that branches on possible values that could be placed in the next empty cell. 
# Initial pruning of the recursion tree - 
#       we don't continue on any branch that has already produced an inconsistent solution
#       we stop and return a complete solution once one has been found

import pygame, Snapshot, Cell, Futoshiki_IO

def solve(snapshot, screen):
    ##display current snapshot
    pygame.time.delay(200)
    Futoshiki_IO.displayPuzzle(snapshot, screen)
    pygame.display.flip()
    global changeWasMade
    changeWasMade = False

    if checkConsistency(snapshot) == False: return False
    if isComplete(snapshot): return True

    doPreCheck(snapshot)
    if changeWasMade:
        print len(snapshot.unsolvedCells())
        solve(snapshot,screen)
        if isComplete(snapshot) and checkConsistency(snapshot): return True
    else:
        print "take a guess"
        for option in snapshot.unsolvedCells()[0].getOptions():
            newSnapshot = snapshot.clone()
            newSnapshot.unsolvedCells()[0].setVal(option)
            if checkConsistency(newSnapshot):
                try:
                    success = solve(newSnapshot, screen)
                    if success: return True
                except IndexError: pass


    #return False






#else: return False

    ## if current snapshot not complete ...
    ## get next empty cell

    # for each value in the cells possibles list:
    #    newsnapshot = ....clone current snapshot and update the cell with the value
    ##                                          if new snapshot is consistent, perform recursive call to solve
    #    if checkConsistency(newsnapshot):
    #       success = solve(newsnapshot, screen)
    #       if success: return True
    
    ## if we get to here no way to solve from current snapshot
    # return False


# Check whether a snapshot is consistent, i.e. all cell values comply
# with the Futoshiki rules (each number occurs only once in each row and column,
# no "<" constraints violated).



def doPreCheck(snapshot):

    constrainMinMax(snapshot)
    checkForcedPosition(snapshot)
    checkOptions(snapshot)



def checkConsistency(snapshot):

    for i in range(5):
        rowValues = []
        colValues = []
        for y in snapshot.cellsByCol(i):
            colValues.append(y.getVal())
        for x in snapshot.cellsByRow(i):
            rowValues.append(x.getVal())
        for value in [1,2,3,4,5]:
            if rowValues.count(value) > 1 or colValues.count(value) > 1:
                return False

    for x,y in snapshot.getConstraints():
        smallerCell = snapshot.cells[x[0]][x[1]]
        largerCell = snapshot.cells[y[0]][y[1]]
        if (smallerCell.getVal() > 0 and largerCell.getVal() > 0) and not (smallerCell.getVal() < largerCell.getVal()):
            return False

    for cell in snapshot.unsolvedCells():
        if len(cell.getOptions()) == 0:
            return False

    return True






# Check whether a puzzle is solved.
# return true if the Futoshiki is solved, false otherwise

def isComplete(snapshot):
    if len(snapshot.unsolvedCells()) == 0:
        return True

def changeMade():
    global changeWasMade
    changeWasMade = True

def checkOptions(snapshot):

    for cell in snapshot.unsolvedCells():
        rowValues = []
        colValues = []
        for y in snapshot.cellsByCol(cell.getCol()):
            colValues.append(y.getVal())
        for x in snapshot.cellsByRow(cell.getRow()):
            rowValues.append(x.getVal())

        cell.removeOption(rowValues)
        cell.removeOption(colValues)

        if len(cell.getOptions()) == 1:
            cell.setVal(cell.getOptions()[0])
            checkOptions(snapshot)
            changeMade()



def constrainMinMax(snapshot):
    checkOptions(snapshot)
    for x,y in snapshot.getConstraints():

        smallerCell = snapshot.cells[x[0]][x[1]]
        largerCell = snapshot.cells[y[0]][y[1]]
        if largerCell.getVal() == 0:
            tooLow = [option for option in largerCell.getOptions() if option <= smallerCell.getOptions()[0]]
            largerCell.removeOption(tooLow)
        if smallerCell.getVal() == 0:
            tooHigh = [option for option in smallerCell.getOptions() if option >= largerCell.getOptions()[-1]]
            smallerCell.removeOption(tooHigh)

        #if len(tooLow) > 0 or len(tooHigh) > 0:
            #changeMade()



def checkForcedPosition(snapshot):
    checkOptions(snapshot)
    for line in range(5):
        unsolvedByRow = [cell for cell in snapshot.cellsByRow(line) if cell in snapshot.unsolvedCells()]
        for cell in unsolvedByRow:
            thisCell = cell
            otherCells = [cell for cell in snapshot.cellsByRow(line) if cell != thisCell]
            otherCellOptions = []
            for cell in otherCells:
                for option in cell.getOptions():
                    otherCellOptions.append(option)
            for option in thisCell.getOptions():
                if option not in otherCellOptions:
                    thisCell.setVal(option)
                    changeMade()
                    break
        unsolvedByCol = [cell for cell in snapshot.cellsByCol(line) if cell in snapshot.unsolvedCells()]
        for cell in unsolvedByCol:
            thisCell = cell
            otherCells = [cell for cell in snapshot.cellsByCol(line) if cell != thisCell]
            otherCellOptions = []
            for cell in otherCells:
                for option in cell.getOptions():
                    otherCellOptions.append(option)
            for option in thisCell.getOptions():
                if option not in otherCellOptions:
                    thisCell.setVal(option)
                    changeMade()
                    break



