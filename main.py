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


def get_avatar(token):
    r = requests.get("https://discord.com/api/v9/users/@me", headers={"authorization": token})
    if r.status_code == 200:
        return r.json()["avatar"]
    else:
        return None
    
def get_banner(token):
    r = requests.get("https://discord.com/api/v9/users/@me/banners", headers={"authorization": token})
    if r.status_code == 200:
        return r.json()["banner"]
    else:
        return None
    
def menu():
    a = input("Enter your token to start:\n")
    return a

def main():
    token = menu()
    profile = get_profile(token)
    if profile is None:
        print("Invalid token")
        quit()
    else:
        print(f"Exporting Information on account: {profile['username']}#{profile['discriminator']} | {profile['id']}")
        export_path = os.path.join("exports", f"{profile['username']}#{profile['discriminator']} | {profile['id']}")
        if export_path.startswith("/"):
            export_path = export_path[1:]
        os.makedirs(export_path, exist_ok=True)
        os.makedirs(os.path.join(export_path, "profile"), exist_ok=True)
        os.makedirs(os.path.join(export_path, "dms"), exist_ok=True)
        with open(os.path.join(export_path, "profile", "general.txt"), "w") as f:
            for key, value in profile.items():
                if isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        f.write(f"{key}.{subkey}: {subvalue}\n")
                else:
                    f.write(f"{key}: {value}\n")

        avatar = get_avatar(token)
        if avatar is not None:
            image_url = f"https://cdn.discordapp.com/avatars/{profile['id']}/{avatar}.png"
            r = requests.get(image_url)
            if r.status_code == 200:
                with open(os.path.join(export_path, "profile", "avatar.png"), "wb") as f:
                    f.write(r.content)

        banner = get_banner(token)
        if banner is not None:
            image_url = f"https://cdn.discordapp.com/banners/{profile['id']}/{banner}.png"
            r = requests.get(image_url)
            if r.status_code == 200:
                with open(os.path.join(export_path, "profile", "banner.png"), "wb") as f:
                    f.write(r.content)

        guilds = get_guilds(token)
        guilds_folder = os.path.join(export_path, "guilds")
        os.makedirs(guilds_folder, exist_ok=True)
        for guild in guilds:
            guild_folder = os.path.join(guilds_folder, f"{guild['name']} | {guild['id']}")
            if not guild_folder.startswith(guilds_folder):
                guild_folder = os.path.join(guilds_folder, guild_folder[1:])
            os.makedirs(guild_folder, exist_ok=True)
            with open(os.path.join(guild_folder, "general.txt"), "w") as f:
                for key, value in guild.items():
                    if isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            f.write(f"{key}.{subkey}: {subvalue}\n")
                    else:
                        f.write(f"{key}: {value}\n")
            r = requests.get(f"https://discord.com/api/v9/guilds/{guild['id']}/channels", headers={"authorization": token})
            if r.status_code == 200:
                with open(os.path.join(guild_folder, "channels.txt"), "w") as f:
                    for channel in r.json():
                        f.write(f"{channel['name']}\n")

        os.makedirs(os.path.join(export_path, "friends"), exist_ok=True)
        friends = get_friends(token)
        for friend in friends:
            friend_folder = os.path.join(export_path, "friends", f"{friend['user']['username']}#{friend['user']['discriminator']} | {friend['user']['id']}")
            if not friend_folder.startswith(os.path.join(export_path, "friends")):
                friend_folder = os.path.join(os.path.join(export_path, "friends"), friend_folder[1:])
            os.makedirs(friend_folder, exist_ok=True)
            with open(os.path.join(friend_folder, "information.txt"), "w") as f:
                for key, value in friend.items():
                    if isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            f.write(f"{key}.{subkey}: {subvalue}\n")
                    else:
                        f.write(f"{key}: {value}\n")
if __name__ == "__main__":
    main()

