from django.db import models


#Game Class
class Game(models.Model):
    #Setup Model
    teams = models.CharField(max_length=200)
    game_date_time = models.CharField(max_length=200)
    team_away = models.CharField(max_length=200)
    team_home = models.CharField(max_length=200)
    spread_away = models.CharField(max_length=10)
    spread_away_payout = models.CharField(max_length=10)
    spread_home = models.CharField(max_length=10)
    spread_home_payout = models.CharField(max_length=10)
    total_points_away = models.CharField(max_length=10)
    total_points_away_payout = models.CharField(max_length=10)
    total_points_home = models.CharField(max_length=10)
    total_points_home_payout = models.CharField(max_length=10)
    money_line_away = models.CharField(max_length=10)
    money_line_home = models.CharField(max_length=10)


