import praw
from praw.models import MoreComments
import requests
import json

# log function
def log(text):
    if debug: #ensures that we want logs before logging
        print(text)

# get config
# refer to this page if you dont understand what youre looking for https://www.reddit.com/wiki/api
json_file = open("config.json")
variables = json.load(json_file)
json_file.close()
    
log("client_id " + variables['client_id'])
log("client_secret " + variables['client_secret'])
log("user_agent " + variables['user_agent'])
log("username " + variables['username'])
log("password " + variables['password'])

debug = variables['debug']
canPost = variables['canPost']
        
# reddit instance init
reddit = praw.Reddit(
    client_id=variables['client_id'],
    client_secret=variables['client_secret'],
    user_agent=variables['user_agent'],
    username=variables['username'],
    password=variables['password']
    )
log("Reddit initialized")

# data retrieval
response = requests.get("https://api.stats.golem.network/v1/network/historical/pricing/average").json()

length = len(response)

avgStart = response[length - 1]['start']
avgCpu = response[length - 1]['cpuh']
avgPerH = response[length - 1]['perh']

response = requests.get("https://api.stats.golem.network/v1/network/earnings/24").json()

dayEarnings = response['total_earnings']

response = requests.get("https://api.stats.golem.network/v1/network/online/stats").json()

providers = response['online']

response = requests.get("https://api.stats.golem.network/v1/requestors").json()

top1amount = response[0]
top2amount = response[1]
top3amount = response[2]
top4amount = response[3]
top5amount = response[4]

log("length " + str(length))
log("avgStart " + str(avgStart))
log("avgCpu " + str(avgCpu))
log("avgPerH " + str(avgPerH))
log("dayEarnings " + str(dayEarnings))
log("providers " + str(providers))
log("top 5 providers " + "\n\ntop 1: " + str(top1amount) + "\n\ntop 2: " + str(top2amount) + "\n\ntop 3: " + str(top3amount) + "\n\ntop 4: " + str(top4amount) + "\n\ntop 5: " + str(top5amount))
log("OOGA BOOGA!\n\nAverage Start " + str(avgStart) + "\nAverage CPU/hour " + str(avgCpu) + "\nAverage per hour " + str(avgPerH) + "\nDay Earnings(24h) " + str(dayEarnings) + "\nOnline Providers " + str(providers) + "\n\n[Command List](https://siasky.net/AADsQBY2Bguqfitm2cMGaLrdIJ0ObWOtZignAF45f_Of-w)")
log("AAAaaaaAAAAaa!!!\n\nAverage Start " + str(avgStart) + "\nAverage CPU/hour " + str(avgCpu) + "\nAverage per hour " + str(avgPerH) + "\n\n[Command List](https://siasky.net/AADsQBY2Bguqfitm2cMGaLrdIJ0ObWOtZignAF45f_Of-w)")
log("very money such wow\n\nDay Earnings(24h) " + str(dayEarnings) + "\n\n[Command List](https://siasky.net/AADsQBY2Bguqfitm2cMGaLrdIJ0ObWOtZignAF45f_Of-w)")
log("Now this is a lot!\n\nOnline Providers " + str(providers) + "\n\n[Command List](https://siasky.net/AADsQBY2Bguqfitm2cMGaLrdIJ0ObWOtZignAF45f_Of-w)")
# reddit shenanigans
subreddit = reddit.subreddit("GolemProject")

# comment logic
for submission in subreddit.new(limit=1):
    log(submission.title)
    # TODO SUBMISSION TITLE LOGIC
    for comment in submission.comments:
        if hasattr(comment,"body"):
            comment_lower = comment.body.lower()
            log("------------------")
            log(comment_lower)
            if "!topRequestors" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
            if canPost:
                log("bot wasnt here")
                log("----- REPLY -----")
                log("SHEEEEEEEEEEEEEEEEESH" + "\n\nTop 5 providers by amount are:" + "\n\ntop 1: " + str(top1amount) + "\n\ntop 2: " + str(top2amount) + "\n\ntop 3: " + str(top3amount) + "\n\ntop 4: " + str(top4amount) + "\n\ntop 5: " + str(top5amount) + "\n\n[Command List](https://siasky.net/AADsQBY2Bguqfitm2cMGaLrdIJ0ObWOtZignAF45f_Of-w)")
                comment.reply("SHEEEEEEEEEEEEEEEEESH" + "\n\nTop 5 providers by amount are:" + "\n\ntop 1: " + str(top1amount) + "\n\ntop 2: " + str(top2amount) + "\n\ntop 3: " + str(top3amount) + "\n\ntop 4: " + str(top4amount) + "\n\ntop 5: " + str(top5amount) + "\n\n[Command List](https://siasky.net/AADsQBY2Bguqfitm2cMGaLrdIJ0ObWOtZignAF45f_Of-w)")
            if "!full" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
                if canPost:
                    log("bot wasnt here")
                    log("----- REPLY -----")
                    log("OOGA BOOGA!\n\nAverage Start " + str(avgStart) + " GLM" + "\n\nAverage CPU/hour " + str(avgCpu) + " GLM" + "\n\nAverage per hour " + str(avgPerH) + " GLM" + "\n\nDay Earnings(24h) " + str(dayEarnings) + " GLM" + "\n\nOnline Providers " + str(providers))
                    comment.reply("OOGA BOOGA!\n\nAverage Start " + str(avgStart) + " GLM" + "\n\nAverage CPU/hour " + str(avgCpu) + " GLM" + "\n\nAverage per hour " + str(avgPerH) + " GLM" + "\n\nDay Earnings(24h) " + str(dayEarnings) + " GLM" + "\n\nOnline Providers " + str(providers) + "\n\n[Command List](https://siasky.net/AADsQBY2Bguqfitm2cMGaLrdIJ0ObWOtZignAF45f_Of-w)")
                canPost = 1
            if "!average" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
                if canPost:
                    log("bot wasnt here")
                    log("----- REPLY -----")
                    comment.reply("AAAaaaaAAAAaa!!!\n\nAverage Start " + str(avgStart) + " GLM" + "\n\nAverage CPU/hour " + str(avgCpu) + " GLM" + "\n\nAverage per hour " + str(avgPerH) + " GLM" + "\n\n[Command List](https://siasky.net/AADsQBY2Bguqfitm2cMGaLrdIJ0ObWOtZignAF45f_Of-w)")
                canPost = 1
            if "!earnings" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
                if canPost:
                    log("bot wasnt here")
                    log("----- REPLY -----")
                    comment.reply("very money such wow\n\nDay Earnings(24h) " + str(dayEarnings) + " GLM" + "\n\n[Command List](https://siasky.net/AADsQBY2Bguqfitm2cMGaLrdIJ0ObWOtZignAF45f_Of-w)")
                canPost = 1
            if "!online" in comment_lower:
                for reply in comment.replies:
                    if "golem-stat-bot" == reply.author.name:
                        canPost = 0
                if canPost:
                    log("bot wasnt here")
                    log("----- REPLY -----")
                    comment.reply("Now this is a lot!\n\nOnline Providers " + str(providers) + "\n\n[Command List](https://siasky.net/AADsQBY2Bguqfitm2cMGaLrdIJ0ObWOtZignAF45f_Of-w)")
                canPost = 1
                
log("Done! Quitting ...")
