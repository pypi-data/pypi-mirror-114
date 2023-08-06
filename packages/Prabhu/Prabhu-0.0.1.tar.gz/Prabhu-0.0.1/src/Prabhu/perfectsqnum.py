def perfectsqnum(num):
    def sqroot(num):
        return int(num**0.5)
    # checking wheather it's a perfect square or not
    def isperfectsquare(num):
        return int(sqroot(num)**2)
    try:
        #num = int(input("Enter a Number: "))
        if num == isperfectsquare(num):
            print(f"{num} is a perfect square ({int(num**0.5)} x {int(num**0.5)})")
        else:
            print(f"nope, {num} is not a perfect square\nThe Nearest Perfect Square is {(int(num**0.5))**2} and {(int(num**0.5)+1)**2} ")
    except:
        print("Invalid Input")
    
    print("\n\nby Prabhu Kiran")