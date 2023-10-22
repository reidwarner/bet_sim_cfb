from bs4 import BeautifulSoup
import requests
import json
from .models import Game


def data_scrape():

    # Web Scraper
    url = "https://www.lines.com/betting/ncaaf/odds"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    script = doc.find_all('script')[5].text.strip()

    # game_data is a json file. The relevant fields are ['name'], ['location']['name'], ['awayTeam']['name'],
    # ['homeTeam']['name'], ['startDate']
    game_data = json.loads(script)

    # odds is a list with a bunch of the betting values staggered in the following way: P/S away, P/S payout away, P/S home,
    # P/S payout home, etc.
    odds = doc.find_all('div', {'class': "odds-list-val"})
    teams = doc.find_all('div', {'class': "odds-list-team-title"})
    game_date_times = doc.find_all('div', {'class': "odds-list-section-title"})

    # Loop through to establish all of our variable and add them to the database
    data_dict = {}
    j = 0
    k = 0

    for i in range(0, len(odds), 6):
        # gets team (index 0) and record (index -1)
        team_away = teams[j].text.strip()[:-6].strip()
        team_home = teams[j + 1].text.strip()[:-6].strip()
        game = f'{team_away} vs. {team_home}'
        game_time = game_date_times[k].text.strip()[:-9].strip()
        j += 2
        k += 1

        ps_away = odds[i].text.rsplit('(')
        ps_line_away = ps_away[0].strip()
        ps_payout_away = "(" + ps_away[1].strip()

        ps_home = odds[i + 1].text.rsplit('(')
        ps_line_home = ps_home[0].strip()
        ps_payout_home = "(" + ps_home[1].strip()

        ou_away = odds[i + 2].text.rsplit('(')
        ou_line_away = ou_away[0].strip()
        ou_payout_away = "(" + ou_away[1].strip()

        ou_home = odds[i + 3].text.rsplit('(')
        ou_line_home = ou_home[0].strip()
        ou_payout_home = "(" + ou_home[1].strip()

        ml_away = odds[i + 4].text
        ml_home = odds[i + 5].text

        data_dict[game] = {'date and time': game_time,
                           'away team': team_away,
                           'home team': team_home,
                           'spread away': ps_line_away,
                           'spread away payout': ps_payout_away,
                           'spread home': ps_line_home,
                           'spread home payout': ps_payout_home,
                           'total points away': ou_line_away,
                           'total points away payout': ou_payout_away,
                           'total points home': ou_line_home,
                           'total points home payout': ou_payout_home,
                           'money line away': ml_away,
                           'money line home': ml_home,
                           }

    # Populate the game database
    for key in data_dict:
        game = Game(teams=key,
                  game_date_time=data_dict[key]['date and time'],
                  team_away=data_dict[key]['away team'],
                  team_home=data_dict[key]['home team'],
                  spread_away=data_dict[key]['spread away'],
                  spread_away_payout=data_dict[key]['spread away payout'],
                  spread_home=data_dict[key]['spread home'],
                  spread_home_payout=data_dict[key]['spread home payout'],
                  total_points_away=data_dict[key]['total points away'],
                  total_points_away_payout=data_dict[key]['total points away payout'],
                  total_points_home=data_dict[key]['total points home'],
                  total_points_home_payout=data_dict[key]['total points home payout'],
                  money_line_away=data_dict[key]['money line away'],
                  money_line_home=data_dict[key]['money line home'],
                  )
        game.save()
