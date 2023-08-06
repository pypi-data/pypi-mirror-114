import requests
import sys

name = """\033[1;30;40m
___________________________________________________________
\033[1;36;40m

\033[1;34;40m cutt.ly
\033[1;38;40m _  _ ___ _       __  _  _  __  ___ _____ ___ __  _ ___ ___
\033[1;31;40m| || | _ \ |    /' _/| || |/__\| _ \_   _| __|  \| | __| _ \
\033[1;32;40m| \/ | v / |_   `._`.| >< | \/ | v / | | | _|| | ' | _|| v /
\033[1;37;40m \__/|_|_\___|  |___/|_||_|\__/|_|_\ |_| |___|_|\__|___|_|_\

\033[1;30;40m
 ____________________________________________________________
\033[1;31;40m      creat by [÷] shehan lahiru
\033[1;31;40m      git hub [÷]https://github.com/shehan-9909
\033[1;37;40m

"""
print(name ,"")

def main():
    api_key = "45ab6e1d223dde323d9a0c1c2c08bd5c"

    url = input("enter shortner url :-  ")


    api_url = f"https://cutt.ly/api/api.php?key={api_key}&short={url}"

    data = requests.get(api_url).json()["url"]
    if data["status"] == 7:
        shortened_url = data["shortLink"]
        print("Shortened URL:", shortened_url)
    else:
        print("[!] Error Shortening URL:", data)


if __name__ == "__main__":
    main()
