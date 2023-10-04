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

# Function to get achievements data for a specific game
def get_game_achievements(app_id):
    url = f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={STEAM_API_KEY}&steamid={STEAM_USER_ID}'
    response = requests.get(url)
    data = response.json()
    if 'achievements' in data['playerstats']:
        total_achievements = len(data['playerstats']['achievements'])
        unlocked_achievements = sum(achievement['achieved'] for achievement in data['playerstats']['achievements'])
        completion_percentage = (unlocked_achievements / total_achievements) * 100
        return completion_percentage
    else:
        return 0

# Main function to calculate the average achievement completion percentage
def main():
    games = get_user_games(STEAM_USER_ID, STEAM_API_KEY)
    total_completion_percentage = 0
    num_games_with_achievements = 0

    for game in games:
        app_id = game['appid']
        print(f'Checking game {app_id}...')
        achievement_completion_percentage = get_game_achievements(app_id)
        if achievement_completion_percentage > 0:
            total_completion_percentage += achievement_completion_percentage
            num_games_with_achievements += 1

    if num_games_with_achievements > 0:
        average_completion_percentage = total_completion_percentage / num_games_with_achievements
        print(f'Average achievement completion percentage: {average_completion_percentage:.2f}%')
    else:
        print('No games with achievements found for the user.')

if __name__ == '__main__':
    main()
