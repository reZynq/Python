import os
from datetime import date

def line():
    print("-----------------------------------------------------------")

def greeting():
    if not os.path.exists("Bank Account.txt"):
        with open("Bank Account.txt", "w", encoding="utf-8") as file:
            file.write("Spend Account:\n\n")
            file.write("£0.00\n\n")
            file.write("Saving Account:\n\n")
            file.write("£0.00\n\n")

    if not os.path.exists("Transactions.txt"):
        with open("Transactions.txt", "w", encoding="utf-8") as file:
            file.write("Transactions:\n\n")
    if not os.path.exists("Bills.txt"):
        with open("Bills.txt", "w", encoding="utf-8") as file:
            file.write("Bills:\n\n")
    else:
        pass
    line()
    print("Welcome to your Bank Account")
    print("")
    print("1. Deposit money\n2. Withdraw money\n3. View balance\n4. View transactions\n5. Bill\n6. Exit")
    line()

def choice():
    while True:
        print("")
        choice = input("Please enter the option number: ")
        match choice:
            case "1": deposit(); break
            case "2": withdraw(); break
            case "3": balance(); break
            case "4": transactions(); break
            case "5": bill(); break
            case "6": exit()
            case _: print("Not an option, please choose again")

def deposit():
    while True:
        today = date.today()
        print("")
        line()
        account = input("Account (spend or save): ").lower()
        money_deposit = float(input("Enter deposit: "))
        reason = input("Reason: ")
        if account == "spend":
            with open("Bank Account.txt", encoding="utf-8") as file:
                lines = file.readlines()
                money = float(lines[2].replace("£", "").strip())
                lines[2] = f"£{money + money_deposit}\n"
            with open("Bank Account.txt", "w", encoding="utf-8") as file:
                file.writelines(lines)

            with open("Transactions.txt", encoding="utf-8") as file:
                lines = file.readlines()
            with open("Transactions.txt", "w", encoding="utf-8") as file:
                new_line = f"[SPEND] {today}: +£{money_deposit} ({reason})\n"
                lines.insert(2, new_line)
                file.writelines(lines)

            line()
            greeting()
            choice()
            break     

        elif account == "save":
            who = input("Who: ").upper()
            with open("Bank Account.txt", encoding="utf-8") as file:
                lines = file.readlines()
                money = float(lines[6].replace("£", "").strip())
                lines[6] = f"£{money + money_deposit}\n"
            with open("Bank Account.txt", "w", encoding="utf-8") as file:
                file.writelines(lines)

            with open("Transactions.txt", encoding="utf-8") as file:
                lines = file.readlines()
            with open("Transactions.txt", "w", encoding="utf-8") as file:
                new_line = f"[SAVINGS][{who}] {today}: +£{money_deposit} ({reason})\n"
                lines.insert(2, new_line)
                file.writelines(lines)
            line()
            greeting()
            choice()
            break     

        else:
            print("Not an option")
            line()
            greeting()
            choice()

def withdraw():
    today = date.today()
    print("")
    line()
    account = input("Account (spend or save): ").lower()
    money_withdrawal = float(input("Enter withdrawal: "))
    reason = input("Reason: ")
    if account == "spend":
        with open("Bank Account.txt", encoding="utf-8") as file:
            lines = file.readlines()
            money = float(lines[2].replace("£", "").strip())
            if (money < money_withdrawal) or (money_withdrawal <= 0):
                print("You cannot withdraw this amount")
                withdraw()
            else:
                lines[2] = f"£{money - money_withdrawal}\n"
                with open("Bank Account.txt", "w", encoding="utf-8") as file:
                    file.writelines(lines)

                with open("Transactions.txt", encoding="utf-8") as file:
                    lines = file.readlines()
                with open("Transactions.txt", "w", encoding="utf-8") as file:
                    new_line = f"[SPEND] {today}: -£{money_withdrawal} ({reason})\n"
                    lines.insert(2, new_line)
                    file.writelines(lines)
                line()
                greeting()
                choice()

    elif account == "save":
        with open("Bank Account.txt", encoding="utf-8") as file:
            lines = file.readlines()
            money = float(lines[6].replace("£", "").strip())
            if (money < money_withdrawal) or (money_withdrawal <= 0):
                print("You cannot withdraw this amount")
                withdraw()
            else:               
                lines[6] = f"£{money - money_withdrawal}\n"
                with open("Bank Account.txt", "w", encoding="utf-8") as file:
                    file.writelines(lines)
                with open("Transactions.txt", encoding="utf-8") as file:
                    lines = file.readlines()
                with open("Transactions.txt", "w", encoding="utf-8") as file:
                    new_line = f"[SAVINGS] {today}: -£{money_withdrawal} ({reason})\n"
                    lines.insert(2, new_line)
                    file.writelines(lines)
                line()
                greeting()
                choice()      
    else:
        print("Not an option")
        withdraw()

def balance():
    account = input("Account (spend or save): ").lower()
    if account == "save":
        with open("Bank Account.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            print(f"[SAVING] You have {lines[6]}")
            go_back = input("Go Back (yes/no): ").lower()
            if go_back == "yes":
                line()
                greeting()
                choice()
            else:
                print("Thank you for using this bank")
    elif account == "spend":
        with open("Bank Account.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            print(f"[SPENDING] You have {lines[2]}")
            go_back = input("Go Back (yes/no): ").lower()
            if go_back == "yes":
                line()
                greeting()
                choice()
            else:
                print("Thank you for using this bank")
        
    else:
        print("Not an option")
        balance()

def transactions():
    with open("Transactions.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        count = 0
        for i in lines:
            count += 1
        count -= 2
        print(f"You have {count} transactions")
        number = int(input("How many transactions do you want to read: "))
        print("")
        line()
        if number > count:
            print("Error, too many transactions")
            line()
            print("")
            transactions()
        else:
            number += 2
            for lines1 in range(2, number):
                print(lines[lines1], end="")
            print("")
            line()
            print("")

            go_back = input("Go Back (yes/no): ")
            if go_back == "yes":
                line()
                greeting()
                choice()
            else:
                print("Thank you for using this bank")

def bill():
    today = date.today()
    print("")
    line()
    print("")
    print("1. Add a bill\n2. Remove a bill\n3. View your bills")
    print("")
    number = int(input("Enter your choice: "))
    if number == 1:
        payer = input("Who is paying the bill: ")
        recipient = input("Who is recieving the bill: ")
        amount = input("How much is the bill: ")
        with open("Bills.txt", encoding="utf-8") as file:
            lines = file.readlines()
        with open("Bills.txt","w", encoding="utf-8") as file:
            new_line = f"[BILL] {today}: {payer} owes {recipient} £{amount}\n"
            lines.insert(2, new_line)
            file.writelines(lines)
        print("")
        line()
        greeting()
        choice()

    elif number == 2:
        n = int(input("Which bill do you want to remove: "))
        with open("Bills.txt", encoding="utf-8") as file:
            lines = file.readlines()
        del lines[n+1]
        with open("Bills.txt", "w", encoding="utf-8") as file:
            file.writelines(lines)
        print("")
        line()
        greeting()
        choice()

    elif number == 3:
        with open("Bills.txt", encoding="utf-8") as file:
            lines = file.readlines()
            count = 0
            for n in lines:
                count += 1
            for i in range(2,count):
                print(lines[i], end="")

        go_back = input("Go Back (yes/no): ").lower()
        if go_back == "yes":
            print("")
            line()
            greeting()
            choice()
        else:
            print("Thank you for using this bank")

    else:
        print("Not an option")
        print("")
        bill()

if __name__ == "__main__":
    greeting()
    choice()
else:
    print("Error 404")
