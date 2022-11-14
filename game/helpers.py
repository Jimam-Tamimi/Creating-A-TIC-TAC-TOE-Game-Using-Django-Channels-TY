def checkWin(board):
    if board["0"] == board["1"] and board["0"] == board["2"] and board["0"] != "":
        return board["0"]

    elif board["3"] == board["4"] and board["3"] == board["5"] and board["3"] != "":
        return board["3"]

    elif board["6"] == board["7"] and board["6"] == board["8"] and board["6"] != "":
        return board["6"]

    elif board["0"] == board["3"] and board["0"] == board["6"] and board["0"] != "":
        return board["0"]

    elif board["1"] == board["4"] and board["1"] == board["7"] and board["1"] != "":
        return board["1"]

    elif board["2"] == board["5"] and board["2"] == board["8"] and board["2"] != "":
        return board["2"]

    elif board["0"] == board["4"] and board["0"] == board["8"] and board["0"] != "":
        return board["0"]

    elif board["2"] == board["4"] and board["2"] == board["6"] and board["2"] != "":
        return board["2"]


    else:
        return None
    
def isDraw(board):
    for index in board:
        if(board[index]==""):
            return False
    return True