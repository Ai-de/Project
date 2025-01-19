from twilio.rest import Client

def call():
    account_sid = 'AC706f52479b7de304823384e29e518074'
    auth_token = '3aa059f2d3e969fe85153de273e8fbc0'
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        to='+16134007249',  # Phone number you want to call
        from_='+15075027627',  # Your Twilio number
        url='http://demo.twilio.com/docs/voice.xml'
    )
    print(f"911 call initiated: {call.sid}")
