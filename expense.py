from PyInquirer import prompt
import csv

expense_questions = [
    {
        "type":"input",
        "name":"amount",
        "message":"New Expense - Amount: ",
    },
    {
        "type":"input",
        "name":"label",
        "message":"New Expense - Label: ",
    },
]

def users_list():
    str = []
    with open('users.csv', 'r', newline='') as csvfile:
        spamwriter = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for user in spamwriter:
            str.append(user[0])
    return str

def pop_from_list(list, token):
    count = 0
    for user in list:
        if user == token:
            return count
        count += 1

def involved_user(spenders, spender):
    res = []
    res.append(spender)
    
    spenders.pop(pop_from_list(spenders, spender))

    involved = {
        "type":"list",
        "name":"involved",
        "message":"Choose an involved user",
        "choices": spenders + ['Done']
    }
    inv = prompt(involved)

    while (inv["involved"] != "Done"):
        res.append(inv['involved'])
        spenders.pop(pop_from_list(spenders, inv['involved']))
        involved = {
            "type":"list",
            "name":"involved",
            "message":"Choose an involved user",
            "choices": spenders + ['Done']
        }
        inv = prompt(involved)
    return res

def new_expense(*args):
    infos = prompt(expense_questions)

    spenders = users_list()

    users = {
        "type":"list",
        "name":"user",
        "message":"Choose a Spender",
        "choices": spenders
    }
    option = prompt(users)

    user = option['user']

    inv = involved_user(spenders, user)

    divided_sum = int(infos["amount"]) / len(inv)

    with open('expense_report.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([int(infos['amount']), infos['label'], user, inv, divided_sum])
    print("Expense Added !")
    return True


