import sqlite3
import random
def introduction():
    print("""1. Create an account
2. Log into account
0. Exit""")
introduction()
while True:
    customer_choice = str(input())
    print()
    
    if customer_choice == "1":
        while True:  # while loop for checking on card number by luhn algorithm
            IIN = 400000
            customer_account_number = random.randint(100000000, 999999999)
            check_digit = random.randint(0, 9)
            Drop_the_last_digit = str(IIN) + str(customer_account_number)
            list_of_Drop_last_digit = [int(x) for x in Drop_the_last_digit]
            for i in range(len(list_of_Drop_last_digit)):
                if i % 2 == 0:  # multiply the odd digits by 2
                    list_of_Drop_last_digit[i] = 2 * list_of_Drop_last_digit[i]
                if list_of_Drop_last_digit[i] > 9:  # subtract 9 to numbers over 9
                    list_of_Drop_last_digit[i] = list_of_Drop_last_digit[i] - 9
            control_number_by_Luhn_algorithm = sum(list_of_Drop_last_digit)  # getting the control number by Luhn algorithm
            if (control_number_by_Luhn_algorithm + check_digit) % 10 == 0:
                card_number = str(IIN) + str(customer_account_number) + str(check_digit)
                PIN = random.randint(1000, 9999)
                ID = random.randint(1, 2147483647)
                #  Create Data Base and Connect at a file named 'card.s3db'
                conn = sqlite3.connect('card.s3db')

                #  Setting up the Cursor
                cur = conn.cursor()

                #  Create The table
                cur.execute("CREATE TABLE if not exists card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")

                #  Inserting Data to the table
                cur.execute(f"INSERT INTO card (id, number, pin, balance) VALUES ({ID}, {card_number}, {str(PIN)}, 0)")

                #  Save(Commit) Changes
                conn.commit()
                break
            else:
                continue

        print("""Your card has been created
Your card number:""")
        print(card_number)
        print("Your card PIN:")
        print(PIN)
        print()
        introduction()
        continue
    def stop():
        print("Bye!")
        
    if customer_choice == "2":
        print("Enter your card number:")
        inter_cared_number = int(input())
        print("Enter your PIN:")
        inter_PIN = int(input())
        print()
        #  Create Data Base and Connect at a file named 'card.s3db'
        conn = sqlite3.connect('card.s3db')

        #  Setting up the Cursor
        cur = conn.cursor()
        #  Selecting card number column and pin column from the table for checking if the card number and pin number is correct and the table inclued this values or not 
        cur.execute('SELECT number, pin FROM card')
        list_of_number_pin = cur.fetchall() ## give us a list of tuple for all card numbers and pin numbers
        if (str(inter_cared_number), str(inter_PIN)) in list_of_number_pin:
            print("You have successfully logged in!")
            print()
            
            while True:
                print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
                customer_selection_after_log = str(input())
                print()
                
                if customer_selection_after_log == "1":
                    #  connect the data base
                    cur = conn.cursor()
                    #  selecting card number columns and balance columns
                    cur.execute("SELECT number, balance FROM card")
                    list_of_number_balance = cur.fetchall()
                    for i in list_of_number_balance:
                        if i[0] == str(inter_cared_number):
                            print(f"Balance: {i[1]}")
                    print()
                elif customer_selection_after_log == "2":
                    print("Enter income:")
                    income_value = int(input())
                    #  connect the data base
                    cur = conn.cursor()
                    # make updating for the table in column named balance
                    cur.execute(f"UPDATE card SET balance = balance + {income_value} WHERE number = {str(inter_cared_number)}")
                    conn.commit()
                    
                    print("Income was added!")
                    print()
                elif customer_selection_after_log == "3":
                    print("Transfer")
                    print("Enter card number:")
                    #  Selecting card number column from the table for checking if the card number is correct and the table inclued this values or not 
                    cur.execute('SELECT number FROM card')
                    list_of_number = cur.fetchall() ## give us a list of tuple for all card numbers
                    card_number_transfer_in_to = str(input())
                    Drop_last_digit_card_transfer = card_number_transfer_in_to[:-1]
                    list_Drop_last_digit_card_transfer = [int(x) for x in Drop_last_digit_card_transfer]
                    for i in range(len(list_Drop_last_digit_card_transfer)):
                        if i % 2 == 0:  # multiply the odd digits by 2
                            list_Drop_last_digit_card_transfer[i] = 2 * list_Drop_last_digit_card_transfer[i]
                        if list_Drop_last_digit_card_transfer[i] > 9:  # subtract 9 to numbers over 9
                            list_Drop_last_digit_card_transfer[i] = list_Drop_last_digit_card_transfer[i] - 9
                    control_number_by_Luhn_algorithm_transfer = sum(list_Drop_last_digit_card_transfer)  # getting the control number by Luhn algorithm
                    if (control_number_by_Luhn_algorithm_transfer + int(card_number_transfer_in_to[-1])) % 10 != 0:
                        print("Probably you made a mistake in the card number. Please try again!")
                        print()
                    elif (control_number_by_Luhn_algorithm_transfer + int(card_number_transfer_in_to[-1])) % 10 == 0 and (card_number_transfer_in_to,) not in list_of_number:
                        print("Such a card does not exist.")
                        print()
                    elif (control_number_by_Luhn_algorithm_transfer + int(card_number_transfer_in_to[-1])) % 10 == 0 and (card_number_transfer_in_to,) in list_of_number:
                        print("Enter how much money you want to transfer:")
                        transfered_money = int(input())
                        #  connect the data base
                        cur = conn.cursor()
                        #  selecting card number columns and balance columns
                        cur.execute(f"SELECT balance FROM card WHERE number = {str(inter_cared_number)}")
                        balance_in_the_account = cur.fetchone()
                        if transfered_money > balance_in_the_account[0]:
                            print("Not enough money!")
                            print()
                        elif transfered_money <= balance_in_the_account[0]:
                            #  connect the data base
                            cur = conn.cursor()
                            # make updating for the table in column named balance
                            cur.execute(f"UPDATE card SET balance = balance + {transfered_money} WHERE number = {card_number_transfer_in_to}")
                            cur.execute(f"UPDATE card SET balance = balance - {transfered_money} WHERE number = {str(inter_cared_number)}")
                            conn.commit()
                            print("Success!")
                            print()
                elif customer_selection_after_log == "4":
                    #  DELETING THE ACCOUNT FROM THE TABLE AT THE DATA BASE
                    cur.execute(f"DELETE FROM card WHERE number = {str(inter_cared_number)}")
                    print("The account has been closed!")
                    print()
                    introduction()
                    break
                elif customer_selection_after_log == "5":
                    print("You have successfully logged out!")
                    print()
                    introduction()
                    break
                elif customer_selection_after_log == "0":
                    exit()
                    
        else:
            print("Wrong card number or PIN!")
            print()
            introduction()
            continue
        # Save (commite) changes
        conn.commit()

    if customer_choice == "0":
        print("Bye!")
        exit()