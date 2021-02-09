1/20/2021
---

Got as far as finding my components and am working on downloading a set of the stock symbols to begin my search through
the reddit threads. This isn't working for some reason (probably the url is wrong). Overall, it seems like a fun little
project. 


1/25/2021
---

I punted and just added today's list of tickers as a CSV. It should work well enough for now.

I've now managed to get a sorted list of scored tickers. The problem I'm discovering is picking out the symbols from the
text when so many symbols are single letters. Solved it using the "$" some people use

1/29/2021
---

Added a bunch of functionality to this system. It now saves the data frames it produces as CSVs for easy 
consumption. It uses yfinance to calculate the share prices. It determines the correct portfolio makeup, leaving a 
little cash to cover the inevitable volatility. 

2/3/2021
---

Several unfinished parts make the code look kind of janky. I might consider cleaning this up until I can get these things
done better.


2/6/2021
---

Got a lot of this working and found an awesome website where I can trade with a well-supported API https://alpaca.markets/community

Found a good way to run this on my droplet https://www.tecmint.com/cron-vs-anacron-schedule-jobs-using-anacron-on-linux/

Also thought it might be a good idea to store all the history in one file (appending each new look as we go). That'll 
make it easier to graph the history of this algo.  


2/8/21
---

It may make more sense to work off of the 


Todo
---

- [x] Calculate a % of portfolio based on the score
- [x] Check the share price of each ticker
- [x] Determine how many full shares of each we can buy
- [x] Create a way to save yesterdays portfolio
- [x] Determine the buys and sells we need to get there orders.csv
- [ ] Actually make the trades using Alpaca (I'll need a separate account for this)
- [ ] Write a quick post explaining the code and the motivation behind it

- [x] Make a simple HTML page from the table
- [ ] Write a Systemd task to run the script at all times
- [ ] Add timing to the script, so it updates once a day when trading is open (anacron job)

- [ ] Take this back in time
- [ ] Chart the trends over time (Top 10 and their score over the last year)
- [ ] Track portfolio performance over time

- [ ] Get a live updating list of tickers
- [ ] Add a score factor for original poster karma?
