# Introduction

As a long-term player of Clash Royale, it seemed like a good challenge to develop a simple tool to analyse some metrics about the game.
For this exercise, I set the goal of deciding on three key metrics that I wanted to track. First, to measure the users’ time spent in the app, I decided to get the number of matches that the users played. Second, I look at the number of cards the users obtain per day to measure the player’s progress in the game.
In summary, the KPIs are:

- Number of matches played per day
-	Number of cards obtained per day

# Technical Set up

The first step challenge to solve was getting the data. Fortunately, Clash Royale has a public API that only requires registration on their website. After getting an API key and reading the documentation, I set up a simple SQLite database with the structure shown in Table 1. Then, I wrote a script that calls the API daily and saves the new records in the database to fill the fields. For simplicity reasons, I only tracked the daily stats of 5 players. Having done that, extracting meaningful conclusions was only a couple of SQL queries away.

[Table 1]

# Matches played per day
The most straightforward and most important metric for the team behind a game is people’s time playing it each day. In that sense, the publicly available record of the matches played works as a proxy for it, given that each game takes between three and five minutes. Now, while daily matches are essential, it is also helpful to look at moving averages to get a sense of trends that are not sensitive to random variations in a day. In this case, I take a three-day moving average because my data collection process began just a week ago, and I do not have enough data yet to use longer, more sensible timeframes to average. 

I choose to focus on only those two simple metrics, but many other things can be looked at with just this information. For example, one could see the change in total time spent per player over more extended periods of time or seasonal patterns beyond the weekend spike. Figure 1 shows the results of these two metrics at the latest update of this document.

[Figure 1]

In more technical terms, to produce this chart, given that, in my database, each row of the battle_log table corresponds to a match played by a user, I had to create a table with the total count of games per day, which I then subquery to be able to compute the moving average over three days.

```sql
SELECT date,
       matches,
       AVG(matches) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS three_day_mean
FROM (SELECT battleTime AS date,
             COUNT(*) AS matches
      FROM battle_log
      GROUP BY battleTime)
```
# Player’s progress
