import requests
from colorama import Fore
from datetime import datetime

def getheaders(token):
    return {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

def get_badges(flags):
    badges = ""
    badges_map = {
        1: "Staff",
        2: "Partner",
        4: "Hypesquad Event",
        8: "Green Bughunter",
        64: "Hypesquad Bravery",
        128: "HypeSquad Brilliance",
        256: "HypeSquad Balance",
        512: "Early Supporter",
        16384: "Gold BugHunter",
        131072: "Verified Bot Developer"
    }

    for flag, badge in badges_map.items():
        if flags & flag:
            badges += badge + ", "
    if not badges:
        badges = "None"
    return badges

def get_creation_date(user_id):
    timestamp = ((int(user_id) >> 22) + 1420070400000) / 1000
    creation_date = datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S UTC')
    return creation_date

def print_banner():
    banner = r'''
      _____ _            ____  _                 _   _____           
     |_   _| |__   ___  | __ )| | ___   ___   __| | | ____|   _  ___ 
       | | | '_ \ / _ \ |  _ \| |/ _ \ / _ \ / _` | |  _|| | | |/ _ \
       | | | | | |  __/ | |_) | | (_) | (_) | (_| | | |__| |_| |  __/
       |_| |_| |_|\___| |____/|_|\___/ \___/ \__,_| |_____\__, |\___|
                                                          |___/  account info tool  
    '''
    print(Fore.CYAN + banner + Fore.RESET)

def info():
    token = input("Enter your Discord token: ")
    print_banner()
    user_response = requests.get('https://discord.com/api/v9/users/@me', headers=getheaders(token))
    
    if user_response.status_code == 200:
        user_data = user_response.json()

        badges = get_badges(user_data['flags'])
        username = user_data['username'] + '#' + user_data['discriminator']
        user_id = user_data['id']
        phone = user_data['phone']
        email = user_data['email']
        language = user_data['locale']
        mfa_enabled = user_data['mfa_enabled']
        avatar_id = user_data['avatar']
        avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.webp'
        creation_date = get_creation_date(user_id)

        print(f'''
{Fore.RESET}{Fore.GREEN}####### Account Info #######{Fore.RESET}
[{Fore.LIGHTMAGENTA_EX}Username{Fore.RESET}]        {username} | {user_id}
[{Fore.LIGHTMAGENTA_EX}Badges{Fore.RESET}]          {badges}
[{Fore.LIGHTMAGENTA_EX}Language{Fore.RESET}]        {language}
[{Fore.LIGHTMAGENTA_EX}Created at{Fore.RESET}]      {creation_date}
[{Fore.LIGHTMAGENTA_EX}Avatar URL{Fore.RESET}]      {avatar_url if avatar_id else ""}
[{Fore.LIGHTMAGENTA_EX}Account Token{Fore.RESET}]   {Fore.RED}{token}{Fore.RESET}
{Fore.RESET}{Fore.GREEN}####### Security Info #######{Fore.RESET}
[{Fore.LIGHTMAGENTA_EX}Email{Fore.RESET}]           {email}
[{Fore.LIGHTMAGENTA_EX}Phone Number{Fore.RESET}]    {phone if phone else ""}
[{Fore.LIGHTMAGENTA_EX}2 Factor{Fore.RESET}]        {mfa_enabled}
        ''')
    else:
        print(f'Failed to retrieve account info. Error {user_response.status_code}.')

info()
