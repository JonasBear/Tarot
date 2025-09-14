from TarotReader import TarotReader
import time 
import os

def show_options():
    os.system('clear')
    print("to quit the veil, type in \"-1\", otherwise")
    print("if you wish to see your previous readings, type in \"0\",or else") 
    print("please choose a spread for a peek into your matter: \n")
    time.sleep(2)
    for index, spreads in enumerate(reader.get_spreads(), start = 1):
        print(f"{index}. Name: {spreads['name']}")
        print(f"   Description: {spreads['description']}\n")
    return int(input("So, what's it gonna be? : "))

def print_interpretation(interpretation):
    os.system('clear')
    for index, (position, card_info) in enumerate(interpretation.items(), start=1):
        print((f"{index}. " if len(interpretation)>1 else "") + position)
        print(f"Card Name: {card_info['card']}"+ (", Reversed" if card_info['reverse'] else ""))
        if (card_info['suit'] != None):
            print(f"Suit: {card_info['suit']}")
        print(f"Meaning: {card_info['meaning']}")
        print()

def back_to_menu():
    return int(input("type in \"0\" to show menu and anything else to quit program\n"))
reader = TarotReader()
print("\nWELCOME TO CASPER'S VEIL\n")
time.sleep(1)
input("press \"Enter\" to continue\n")

while (True): 
    prefered_spread = show_options()
    match prefered_spread:
        case -1:
            break
        case 0:
            TarotReader.get_history()
            if (back_to_menu()):
                break
        case default:        
            interpretation = reader.generate_spread(prefered_spread-1)
            print_interpretation(interpretation)
            if (back_to_menu()):
                break