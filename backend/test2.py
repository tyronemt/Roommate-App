import datetime
# from twilio.rest import Client
# import keys

# client = Client(keys.account_sid, keys.auth_token)

# message = client.messages.create(
#         body = "hey",
#         from_ = keys.twilio_number,
#         to = "+16266228628"
#     )

x = datetime.datetime.now()
today = datetime.date.today()
for i in range(7):
    later = today + datetime.timedelta(days=i+1)
    print(later.day)