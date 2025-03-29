import requests, os, dotenv

# Load the environment variables
dotenv.load_dotenv()

STEAM_API_KEY = os.getenv('STEAM_API_KEY')
STEAM_USER_ID = os.getenv('STEAM_USER_ID')

# Function to get a list of games for the given Steam user
def get_user_games(steam_user_id, api_key):
    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_user_id}&format=json'
    response = requests.get(url)
    print(response)
    data = response.json()
    if 'games' in data['response']:
        return data['response']['games']
    else:
        return []

# Function to get the total hours played for a specific game
def get_game_playtime(app_id):
    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={STEAM_USER_ID}&format=json'
    response = requests.get(url)
    data = response.json()

    total_playtime = 0
    if 'games' in data['response']:
        for game in data['response']['games']:
            if game['appid'] == app_id:
                total_playtime = game.get('playtime_forever', 0)  # Playtime in minutes
                break

    return total_playtime / 60  # Convert from minutes to hours

# Main function to calculate the overall hours played across all games
def main():
    games = get_user_games(STEAM_USER_ID, STEAM_API_KEY)
    total_playtime = 0

    for game in games:
        app_id = game['appid']
        print(f'Checking game {app_id}...')
        game_playtime = get_game_playtime(app_id)
        total_playtime += game_playtime

    print(f'Total hours played across all games: {total_playtime:.2f} hours')

if __name__ == '__main__':
    main()
