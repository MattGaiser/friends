import logging
import os
import csv
from flask import Flask
from flask_ask import Ask, request, session, question, statement
from difflib import SequenceMatcher


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

STATUSON = ['on', 'high']
STATUSOFF = ['off', 'low']


def returnEventData(x):
    with open('events.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        i = 0
        for row in reader:
            if (i != (x) or i == 0):
                i = i + 1
                continue
            else:
                return row


@ask.launch
def launch():
    speech_text = 'Hi there. Here is what you can do today. '
    row = returnEventData(1)
    speech_text = speech_text + \
        "You could go to the {} at {} from {} to {}.  ".format(
            row[0], row[1], row[2], row[3])
    row = returnEventData(2)
    speech_text = speech_text + \
        "You could go to the {} at {} from {} to {}.  ".format(
            row[0], row[1], row[2], row[3])
    row = returnEventData(3)
    speech_text = speech_text + \
        "You could go to the {} at {} from {} to {}.  Does option 1, option 2, or option 3 interest you?".format(
            row[0], row[1], row[2], row[3])

   # while (x < 3):
        # row = returnEventData(x)
       # speech_text = speech_text + "You could go to the {} at {} from {} to
       # {}".format( row[0], row[1], row[2], row[3])
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('optionchosen', mapping={'option': 'option'})
def Option_Intent(option, room):
	print(int(option))
	row = returnEventData(int(option))
	print(row)
	return statement(
    'Great,  {} it is. You should leave 22 minutes early to get to {} on time by car or Taxi.'.format(
        row[0],
         row[1]))

@ask.intent('moreinfo', mapping={'option': 'option'})
def Info_Intent(option, room):
	print(int(option))
	row = returnEventData(int(option))
	print(row)
	return statement(
    'Here is what organizers have to say about {}. {} '.format(row[0],row[6]))


@ask.intent('repeatoption', mapping={'option': 'option'})
def Info_Intent(option, room):
	print(int(option))
	row = returnEventData(int(option))
	print(row)
	return statement("You could go to the {} at {} from {} to {}. Here is the organizers statement. {} ".format( row[0], row[1], row[2], row[3], row[6]))

def similar(a,b):
	return SequenceMatcher(None,a,b).ratio()
	
@ask.intent('accessibility', mapping={'option': 'option', 'amentity':'amentity'})
def Option_Intent(option, amentity, room):
	print(int(option))
	row = returnEventData(int(option))
	x = -1
	print("the amenity is" + amentity)
	if (similar(amentity, "wheelchair") > 0.6):
		x = 7
	elif (similar(amentity, "elevator") > 0.6):
		x = 8
	elif (similar(amentity, "parking") > 0.6):
		x = 9
	elif (similar(amentity, "transit") > 0.6):
		x = 10
	elif (similar(amentity, "taxi") > 0.6):
		x = 11
	elif (similar(amentity, "washroom") > 0.6):
		x = 12
	else:
		x = -1
	returnText = "Sorry, I am not sure if that is available."
	if (x > 0):
		if (row[x] == "Yes"):
			returnText = "Yes, {} is available at {}".format(amentity, row[1])
		elif(row[x] == "No"):
			returnText = "No, unfortunately it is not available."
		else: 
			returnText = "There are special conditions which prevent me from knowing. Contact the organizer."
	speech_text = returnText
	return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('morechoices')
def More_Intent():
	speech_text = 'Hmm. Here are a few more options for you to consider. '
	row = returnEventData(4)
	speech_text = speech_text + "You could go to the {} at {} from {} to {}.  ".format( row[0], row[1], row[2], row[3])
	row = returnEventData(5)
	speech_text = speech_text + "You could go to the {} at {} from {} to {}.  ".format( row[0], row[1], row[2], row[3])
	row = returnEventData(6)
	speech_text = speech_text + "You could go to the {} at {} from {} to {}.  Does option 4, option 5, or option 6 interest you?".format( row[0], row[1], row[2], row[3])
	return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent('GpioIntent', mapping={'status': 'status'})
def Gpio_Intent(status, room): 
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    if status in STATUSON:
        GPIO.output(17, GPIO.HIGH)
        return statement('turning {} lights'.format(status))
    elif status in STATUSOFF:
        GPIO.output(17, GPIO.LOW)
        return statement('turning {} lights'.format(status))
    else:
        return statement('Sorry, I couldnt accomplish that.')


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'I help you connect with your community. Here are some things which you can do today'
    return question(speech_text).reprompt(
        speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
