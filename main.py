import pandas as pd
from pandas import DataFrame
from sleeper_wrapper import League, Players, User

leagues = {
    'ddt': 784490857708589056,
    'wheaton': 784653552386744320,
    'rtdb': 782713514853834752,
}


def get_formatted_rosters(league_id: int) -> DataFrame:
    league = League(league_id)
    rosters = league.get_rosters()
    players = Players().get_all_players()

    formatted_rosters = []

    for roster in rosters:
        owner = User(roster['owner_id']).get_user()['display_name']
        player_list = []
        for player in roster['players']:
            player_list.append(
                (
                    owner,
                    players[player]['full_name'],
                    players[player]['position'],
                )
            )
        formatted_rosters.extend(player_list)

    df = pd.DataFrame(formatted_rosters, columns=['owner', 'name', 'pos'])
    return df


def get_formatted_underdog_adp() -> DataFrame:
    df = pd.read_csv('underdog_adp_08_27_2022.csv')
    df['name'] = df['firstName'] + ' ' + df['lastName']
    df = df[['name', 'adp', 'positionRank', 'slotName']]

    return df


def write_output(players: DataFrame, adp: DataFrame) -> None:
    joined = players.join(adp.set_index('name'), on='name', how='left')
    joined['positionRank'] = joined['positionRank'].str[2:]
    joined.to_csv('output_ddt.csv', index=False)


if __name__ == '__main__':
    players = get_formatted_rosters(leagues['ddt'])
    adp = get_formatted_underdog_adp()
    write_output(players, adp)
