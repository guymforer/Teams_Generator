import random, export, notify

def calculate_total_skill(team):
    return sum(list(team.keys()))

def create_teams(num_teams, participants,total_skills):
    if len(participants) % num_teams != 0:
        print("Number of participants is not divisible by the number of teams.")
        return []

    random.shuffle(participants)

    while True:
        random.shuffle(participants)

        teams = [participants[i:i + len(participants)//num_teams] for i in range(0, len(participants), len(participants)//num_teams)]
        average_skill = total_skills / num_teams
        teams_skills =[]

        for team in teams:
            total = 0
            for player in team:
                total += int(sum(player.values()))

            teams_skills.append(total)

        if all(average_skill - 1 <= total_skill <= average_skill + 1 for total_skill in teams_skills):
            break

    return teams


def main():
    #num_teams = int(input("Enter the number of teams: "))
    total_skill = 0

    #export.export_participants()

    file_path = "participants.txt"
    participants = []
    with open(file_path, 'r') as file:
        for line in file:
            name, skill_level = line.strip().split(',')
            total_skill += int(skill_level)
            participants.append(({name:int(skill_level)}))
    
    if len(participants) == 12:
        num_teams = 3
    elif len(participants) == 16:    
        num_teams = 4

    teams = create_teams(num_teams, participants, total_skill)
    
    message_body = 'The generated teams are: \n' 

    for i, team in enumerate(teams):
        result_dict = {key: value for d in team for key, value in d.items()}
        keys_list = list(result_dict.keys())
        message_body = message_body + f"Team {i + 1}: {keys_list} \n"
            
    print(message_body)

    notify.send_message(message_body);    

if __name__ == "__main__":
    main()
