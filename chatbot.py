from flask import Flask,jsonify,request
import json 
import requests

page_access_token=''
app=Flask(__name__)
@app.route('/',methods=['GET'])
def handle_verification():
    print("handler")
    if(request.args.get('hub.verify_token',''))=="my_pass":
        print("verified")
        return request.args.get('hub.challenge','')
    else:
        print("not verified")
        return "Error! not verified"


@app.route("/",methods=['POST'])
def handle_messges():
    payload=request.get_data()
    print(payload)
    for sender,message in messaging_events(payload):
        print("%s:%s"%(sender,message))
        send_message(PAT,sender,message)
    return "ok"

def messaging_events(payload):
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      yield event["sender"]["id"], "I can't echo this"

        
def send_message(token,recipient,message):
  reponse=requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token":token},
    data=json.dumps(
      {"recipient":{"id":recipient}},
      {"message":{"text":message.decode("unicode_escape")}
      }),
    headers={"Content-type":"application/json"})
  if(r.status_code!=requests.codes.ok):
    print(r.text)


