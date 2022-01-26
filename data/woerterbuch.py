import requests

def woerterbuch():
    r = requests.get("https://gist.githubusercontent.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4/raw/36b70dd6be330aa61cd4d4cdfda6234dcb0b8784/wordlist-german.txt")
    data = r.text.split("\n")
    print(len(data))
    print(data[:20])
    return data
