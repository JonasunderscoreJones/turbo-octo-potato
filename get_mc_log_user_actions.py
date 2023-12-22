import os
import gzip

toIgnore = ['User Authenticator', 'logged in with entity id', 'Server sent config handshake', 'joined the game', 'protocol version', 'Handshake response', 'lost connection', 'left the game', 'Disconnecting client', 'UUID of player', 'moved too quickly', 'Disconnecting com.mojang.authlib', 'moved wrongly', 'advancement', 'team', '[OPminerMatt (They\'re Very Odd):', '[The One and Only Jonas_Jones:', '[Jonas_Jones', '<Teal_Wolf_25', 'fell from a high place', 'was shot by', 'drowned', 'Assigning ME player id 1', 'has completed the challenge', 'has reached the goal', 'Sent secret to ', 'Received secret request']

# Function to extract and copy lines containing 'Teal_Wolf_25'
def extract_lines_from_gz(input_folder, output_file):
    with open(output_file, 'w') as output:
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.endswith('.gz'):
                    gz_file_path = os.path.join(root, file)
                    with gzip.open(gz_file_path, 'rt') as gz_file:
                        for line in gz_file:
                            if 'Teal_Wolf_25' in line and not isignored(line):
                                output.write(line)


def isignored(line):
    for keyword in toIgnore:
        if keyword in line:
            return True
    return False

# Main function
def main():
    folder_path = input("Enter the path to the folder containing .gz files: ")
    output_file_path = "teal.txt"
    extract_lines_from_gz(folder_path, output_file_path)
    print(f"Lines containing 'Teal_Wolf_25' have been copied to {output_file_path}")

if __name__ == "__main__":
    main()
