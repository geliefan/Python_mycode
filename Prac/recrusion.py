def guess(x):
    response = input("Is the number " + str(x) + "? Enter Y/N:\n")
    if response == "Y":
        print("YAY!  I got it!")
        return response
    else:
        print("BOO. . . Ok, I'll keep trying.")
        response = input("Is the number greater than or less than " + str(x) + "?Enter        G/L:\n")
    while  response != "G" and reponse != "L":
        print("Sorry, that isn't a valid response/")
        response = input("Pleae try again. Enter G/L:\n")
    return response

def binarySearch(bottom,top):
    if bottom == top: #base case
        return bottom

    elif guess(top+bottom/2) == "G":
        top = top + bottom
        return binarySearch(middle,top)

    elif guess == "L":
        top = (top/2)
        return binarySearch(bottom,top)

    binarySearch(bottom,top)
