from twilio.rest import Client
import keys

client = Client(keys.account_sid, keys.auth_token)

message = client.messages.create(
        body = "hey",
        from_ = keys.twilio_number,
        to = "+16266221237"
    )