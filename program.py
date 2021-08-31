from praw.models import MoreComments
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import requests
import praw
import json
import time
import sys

url = "https://coinmarketcap.com/currencies/golem-network-tokens/"

pageRequest = urlopen(url)
pageResponse = pageRequest.read()
pageRequest.close()

soup = BeautifulSoup(pageResponse, "html.parser")

golemPrice = soup.find("div", class_="sc-16r8icm-0 kjciSH priceTitle___1cXUG").text

golemResult = golemPrice.find(".")

remove = lambda x, unwanted : ''.join([ c for i, c in enumerate(x) if i != unwanted])
remove(golemPrice, golemResult + 2)
# TODO this fucking shit

# log function
def log(text):
    if debug: #ensures that we want logs before logging
        print(text)


# get config
# refer to this page if you dont understand what youre looking for https://www.reddit.com/wiki/api
json_file = open("config.json")
variables = json.load(json_file)
json_file.close()

debug = variables['debug']
canPost = variables['canPost']

log("client_id " + variables['client_id'])
log("client_secret " + variables['client_secret'])  
log("user_agent " + variables['user_agent'])
log("username " + variables['username'])
log("password " + variables['password'])
        
# reddit instance init
reddit = praw.Reddit(
    client_id=variables['client_id'],
    client_secret=variables['client_secret'],
    user_agent=variables['user_agent'],
    username=variables['username'],
    password=variables['password']
    )


log("Reddit initialized")

log(golemPrice)
log(golemResult)

# data retrieval

# !average [data]
response = requests.get("https://api.stats.golem.network/v1/network/historical/pricing/average").json()
length = len(response)

average_averageStart = response[length - 1]['start']
average_averageCpuHour = response[length - 1]['cpuh']
average_averagePerHour = response[length - 1]['perh']

# !earnings [data]
response = requests.get("https://api.stats.golem.network/v1/network/earnings/24").json()
earnings_dayEarnings = response['total_earnings']

# !online [data]
response = requests.get("https://api.stats.golem.network/v1/network/online/stats").json()
online_onlineProviders = response['online']

# !topRequestors [data]
response = requests.get("https://api.stats.golem.network/v1/requestors").json()

topRequestors_top1amount = response[0]["tasks_requested"]
topRequestors_top2amount = response[1]["tasks_requested"]
topRequestors_top3amount = response[2]["tasks_requested"]
topRequestors_top4amount = response[3]["tasks_requested"]
topRequestors_top5amount = response[4]["tasks_requested"]

# !price [data]
# TODO - get the DAAAAAAAAAATAAAAAAAAAAAAAAAAAAAAAAA from coinmarketcap.com yes, and get GLM yes yes very big yes i like boobies


# !stats [data]
response = requests.get("https://api.stats.golem.network/v1/network/online/stats").json()
stats_onlineProviders = response["online"]
response = requests.get("https://api.stats.golem.network/v1/network/provider/average/earnings").json()
stats_averageEerningsPerTask = response["average_earnings"]
#response = requests.get("")

response = requests.get("https://faucet.golem.network/tools/reddit")


# response formed message

# !help [responses]
helpResponse = ["Here's a list of all commmands:\n" + 
                "      !help " + "shows this message\n" +
                "      !full " + "!average + !earnings + !online, all in one command\n" +
                "      !average" + "shows average start price, cpu/hour and price per hour\n" +
                "      !earnings " + "shows day earnings (24h)\n" + 
                "      !online " + "shows online provider at the momement\n" +
                "      !topRequestors " + "top 5 list of requestors\n" +
                "      !exchanges " + "shows the current status of exchanges in regards to token migration\n" +
                "      !price " + "shows price of GLM (usd, btc, marketcap, 24h, 7d, and much more)\n" +
                "      !stats " + "shows data for testnet and mainnet\n" +
                "      !wallets " + "gives a list of wallets integrating GLM\n" +
                "Type !help [command] for more info on a command."]

# !full [responses]
fullResponse = ["Average Start " + str(average_averageStart) + " GLM\n" + 
                "Average CPU/hour " + str(average_averagePerHour) + " GLM\n" + 
                "Average per hour " + str(average_averagePerHour) + " GLM\n" + 
                "Day Earnings(24h) " + str(earnings_dayEarnings) + " GLM\n" +
                "Online Providers " + str(online_onlineProviders) + " providers\n"
                "Type !help [command] for more info on a command."]


# !average [responses]
averageResponse = ["Average Start " + str(average_averageStart) + " GLM\n" + 
                   "Average CPU/hour " + str(average_averageCpuHour) + " GLM\n" + 
                   "Average per hour " + str(average_averagePerHour) + " GLM\n" + 
                   "Type !help or !help [command] for more info on commands"]

# !earnings [responses]
earningsResponse = ["Day Earnings(24h) " + str(earnings_dayEarnings) + " GLM\n" + 
                    "Type !help or !help [command] for more info on commands"]

# !online [responses]
onlineResponse = ["Online Providers " + str(online_onlineProviders) + " providers\n" + 
                  "Type !help [command] for more info on a command."]

# !topRequestors [responses]
topRequestorsResponse = ["Top 5 providers by amount are:" + "\n" + 
                         "     Top 1: " + str(topRequestors_top1amount) + " provider\n" + 
                         "     Top 2: " + str(topRequestors_top2amount) + " provider\n" + 
                         "     Top 3: " + str(topRequestors_top3amount) + " provider\n" + 
                         "     Top 4: " + str(topRequestors_top4amount) + " provider\n" + 
                         "     Top 5: " + str(topRequestors_top5amount) + " provider\n" + 
                         "Type !help or !help [command] for more info on commands"]

# !exchanges [responses]
exchangesResponse = ["Here's the current status of exchanges in regards to the token migration!\n" +
                     "Exodus | Finished |\n" +
                     "Coinswitch Kuber | Finished | https://cs-india-support.coinswitch.co/en/support/solutions/articles/35000170583-update-on-golem-gnt-token-swap-to-glm\n" +
                     "Crypto.com | Finished | https://blog.crypto.com/crypto-com-supports-the-golem-gnt-to-erc-20-migration/\n" +
                     "WazirX | Finished | https://support.wazirx.com/hc/en-us/articles/900003804566\n" +
                     "Bithumb | Finished | https://cafe.bithumb.com/view/board-contents/1641329\n" +
                     "CEX.IO | Finished | https://blog.cex.io/news/cex-io-will-support-golem-token-migration-gnt-to-glm-23216\n" +
                     "Bittrex | Finished | https://bittrex.zendesk.com/hc/en-us/articles/360054009692-Bittrex-support-for-the-Golem-GNT-swap-and-ticker-change-to-GLM-\n" +
                     "Bitso | Declined | https://blog-en.bitso.com/announcement-bitso-will-delist-golem-gnt-on-2021-01-21-76cbd8831f32\n" +
                     "Coinbase Pro | Acknowledged |\n" +
                     "OKEx | In Progress | https://www.okex.com/markets/spot-info/glm-usdt\n" +
                     "Crex 24 | Declined | https://twitter.com/Crex_24/status/1360552427586519047\n" +
                     "Bitrue | Finished | https://twitter.com/BitrueOfficial/status/1367385202398392323\n" +
                     "Bitvavo | Finished |\n" +
                     "Upbit | Finished | https://upbit.com/service_center/notice?id=1605\n" +
                     "Bitfinex | Finished | http://bitfinex.com/posts/561\n" +
                     "HitBTC | Finished | https://twitter.com/hitbtc/status/1331169352406560768\n" +
                     "Huobi | Finished | https://support.hbfile.net/hc/zh-cn/articles/900004665703\n" +
                     "Poloniex | Finished | https://support.poloniex.com/hc/en-us/articles/360057062814\n" +
                     "Binance | Finished | https://www.binance.com/en/support/announcement/a41ae46cd3ef4a76b502730e6e5baaee\n" +
                     "HitBTC | Finished | https://hitbtc.com/glm-to-btc\n" +
                     "CoinEx | Finished |\n" +
                     "Cointree | Finished | https://support.cointree.com/hc/en-us/articles/360002242015-7-December-2020-GNT-to-GLM-token-swap\n" +
                     "Gate.io | Finished | https://us.gate.io/en/help/annlist/18487\n" +
                     "Type !help or !help [command] for more info on commands"]

# !price [responses]
priceResponse = ["Here's the the data about the golem price.\n" + 
                 #"Current Price (USD): " + str(glmPriceUSD) + "\n" + 
                 #"Current Price (BTC): " + str(glmPriceBTC) + "\n" + 
                 #"Marketcap: " + str(glmMarketcap) + "\n" + 
                 #"Marketcap rank: " + str(glmMarketcapRank) + "\n" + 
                 #"ATH: " + str(ATH) + "\n" + 
                 #"Change (30d): " + str(glmChange30d) + "\n" + 
                 #"Change (24h): " + str(glmChange24h) + "\n" + 
                 #"Change (7d): " + str(glmChange7d) + "\n" + 
                 #"Change (1y): " + str(glmChange1y) + "\n" + 
                 "Type !help or !help [command] for more info on commands"]

# !stats [responses]
statsResponse = ["This data is for both testnet and mainnet\n" +
                 #"Providers computing right now: " + str(providersComputing) + "\n" + 
                 #"Earnings (1h): " + str(earnings1h) + "\n" + 
                 #"Average Earnings per Task: " + str(averageEarningPerTask) + "\n" + 
                 "*graph incoming*" + "\n" +
                 "Type !help or !help [command] for more info on commands"]

# !wallets [responses]
walletsResponse = ["Here's the current status of wallets integrating GLM!\n" +
                   "MyCrypto | Finished | https://app.mycrypto.com/migrate/golem\n" +
                   "MyEtherWallet | Finished | https://myetherwallet.com/\n" +
                   "Ledger Live | Finished\n" +
                   "Exodus | Finished | https://support.exodus.io/article/1512-golem-faqs-learn-more-about-glm\n" +
                   "Freewallet | Finished | https://freewallet.org/blog/gnt-glm-migration\n" +
                   "Type !help or !help [command] for more info on commands"]


log("!help\n" + str(helpResponse) + "\n")
log("!full\n" + str(fullResponse) + "\n")
log("!average\n" + str(averageResponse) + "\n")
log("!earnings\n" + str(earningsResponse) + "\n")
log("!online\n" + str(onlineResponse) + "\n")
log("!topRequestors\n" + str(topRequestorsResponse) + "\n")
log("!exchanges\n" + str(exchangesResponse) + "\n")
log("!price\n" + str(priceResponse) + "\n")
log("!stats\n" + str(statsResponse) + "\n")
log("wallets\n" + str(walletsResponse) + "\n")

# reddit shenanigans
subreddit = reddit.subreddit("golemstatbot")

# comment logic
for submission in subreddit.new(limit=1):
    log(submission.title)
    for comment in submission.comments:
        if hasattr(comment,"body"):
            comment_lower = comment.body.lower()
            log("------------------")
            log(comment_lower)

            # command [!quit]
            if "!quit" in comment_lower:
                if "adnssc" | "figureprod" == reply.author.name:
                    sys.exit("bot is terminated")

            # command [!help]
            if "!help" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
                if canPost:
                    log(" ")
                    log(helpResponse)
                    comment.reply(helpResponse)
                    comment.reply("hi")
                canPost = 1

            # command [!full]
            if "!full" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
                if canPost:
                    log(" ")
                    log(fullResponse)
                    comment.reply(fullResponse)
                canPost = 1

            # command [!average]
            if "!average" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
                if canPost:
                    log(" ")
                    log(averageResponse)
                    comment.reply(averageResponse)
                canPost = 1
            
            # command [!earnigns]
            if "!earnings" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
                if canPost:
                    log(" ")
                    log(earningsResponse)
                    comment.reply(earningsResponse)
                canPost = 1

            # command [!online]
            if "!online" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
                if canPost:
                    log(" ")
                    log(onlineResponse)
                    comment.reply(onlineResponse)
                canPost = 1

            # command [!topRequestors]
            if "!topRequestors" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
                if canPost:
                    log(" ")
                    log(topRequestorsResponse)
                    comment.reply(topRequestorsResponse)
                canPost = 1

            # command [!exchanges]
            if "!exchanges" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
                if canPost:
                    log(" ")
                    log(exchangesResponse)
                    comment.reply(exchangesResponse)
                canPost = 1

            # command [!price]
            if "!price" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
                if canPost:
                    log(" ")
                    log(priceResponse)
                    comment.reply(priceResponse)
                canPost = 1

            # command [!stats]
            if "!stats" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
                if canPost:
                    log(" ")
                    log(statsResponse)
                    comment.reply(statsResponse)
                canPost = 1
            
            # command [!wallets]
            if "!wallets" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
                if canPost:
                    log(" ")
                    log(walletsResponse)
                    comment.reply(walletsResponse)
                canPost = 1

log("i like woman")