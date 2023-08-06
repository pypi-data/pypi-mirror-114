import re
from bs4 import BeautifulSoup
from slg_utilities import Scraper, FileOperations
import subprocess


def get_transaction_trends_html(league_id=139692):
    s = Scraper()
    return s.get_html(f'https://football.fantasysports.yahoo.com/f1/buzzindex')

def parse_row(row):
    # only for use with transaction trend table
    columns = row.select('td')
    player = columns[0].text.replace('New Player Note').replace('Player Note', '').replace('No new player Notes').replace('\n', '').split('-')[0].strip()
    return {
        'Player': player,
        'Drops': int(columns[1].text),
        'Adds': int(columns[2].text),
        'Trades': int(columns[3].text),
        'Total': int(columns[4].text),
    }


def main(
    add_threshold=100
):
    fo = FileOperations(start_home=True)

    html = get_transaction_trends_html()
    soup = BeautifulSoup(html, features="html.parser")
    rows = soup.select('tr')[1:]

    for row in rows:
        row_data = parse_row(row)
        if int(row_data['Adds']) > add_threshold:
            result = fo.update_json_if_time_elapsed('ff-player-adds.json', row_data['Player'])
            if result:
                # send text message
                subprocess.run(f"slg-send-text-message -m \"{row_data['Player']}\"", shell=True)

if __name__ == "__main__":
    main()
