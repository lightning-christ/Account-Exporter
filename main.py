import requests
import json
import os

def get_profile(token):
    r = requests.get("https://discord.com/api/v9/users/@me", headers={"authorization": token})
    if r.status_code == 200:
        return r.json()
    else:
        return None
    
def get_guilds(token):
    r = requests.get("https://discord.com/api/v9/users/@me/guilds", headers={"authorization": token})
    if r.status_code == 200:
        return r.json()
    else:
        return None
    
def get_channels(token):
    r = requests.get("https://discord.com/api/v9/users/@me/channels", headers={"authorization": token})
    if r.status_code == 200:
        return r.json()
    else:
        return None
    
def get_messages(token, channel_id):
    r = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers={"authorization": token})
    if r.status_code == 200:
        return r.json()
    else:
        return None
    
def get_friends(token):
    r = requests.get("https://discord.com/api/v9/users/@me/relationships", headers={"authorization": token})
    if r.status_code == 200:
        return r.json()
    else:
        return None


def menu():
    a = input("Enter your token to start:\n")
    return a

def main():
    token = menu()
    a = get_profile(token)
    if a is None:
        print("Invalid token")
        quit()
    else:
        print(a)
        print(f"Exporting Information on account: {a['username']}#{a['discriminator']} | {a['id']}")
        folder_name = f"{a['username']}#{a['discriminator']} | {a['id']}"
        export_path = os.path.join("exports", folder_name)
        os.makedirs(export_path, exist_ok=True)
        os.makedirs(os.path.join(export_path, "profile"), exist_ok=True)
        with open(os.path.join(export_path, "profile", "general.txt"), "w") as f:
            for key, value in a.items():
                if isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        f.write(f"{key}.{subkey}: {subvalue}\n")
                else:
                    f.write(f"{key}: {value}\n")
        os.makedirs(os.path.join(export_path, "guilds"), exist_ok=True)
        os.makedirs(os.path.join(export_path, "friends"), exist_ok=True)
        os.makedirs(os.path.join(export_path, "dms"), exist_ok=True)


if __name__ == "__main__":
    main()

