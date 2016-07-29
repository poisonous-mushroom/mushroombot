#!/usr/bin/python
import cfg, commands, json, requests, sys, time, telepot

def makeJson(content):
    return { "document":{ "type":"PLAIN_TEXT", "content": content }}

def makeHeaders():
    return {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + commands.getoutput('gcloud auth print-access-token')}

def cmd_sentiment(arg):
    '''Returns sentiment polatiry and magnitute from Google Cloud Natural Language API. Takes phrase as an argument'''
    r=requests.post('https://language.googleapis.com/v1beta1/documents:analyzeSentiment', headers = makeHeaders(), json = makeJson(arg))
    return 'Polarity: {0}, magnitude: {1}'.format(str(r.json()['documentSentiment']['polarity']), str(r.json()['documentSentiment']['magnitude']))

def cmd_entities(arg):
    '''Returns JSON response from Google Cloud Natural Language API. Takes argument'''
    r=requests.post('https://language.googleapis.com/v1beta1/documents:analyzeEntities', headers = makeHeaders(), json = makeJson(arg))
    return r.text

def cmd_count(expr):
    '''Solves simple math problems. Takes arithmetic expression as argument'''
    if expr == '14/88': # ja-ja, an easter egg
        return 'Ein Kampf, Ein Sieg!'
    if '/' in expr and '.' not in expr:
        expr = expr.replace('/', './')
    try:
        return 'Counting: '+expr.replace('./', '/')+' = '+str(eval(expr))
    except:
        return 'Something went wrong, check your input: '+expr
    
def cmd_momma(arg=None):
    '''Gives random your momma joke. No arg needed.'''
    r = requests.get('http://api.yomomma.info/')
    return json.loads(r.text)['joke']

def cmd_coordinates(address):
    '''Gives coordinates of geographic locations. Takes location name as argument'''
    r = requests.get('http://maps.googleapis.com/maps/api/geocode/json?address='+address.replace(' ','%20')+'&sensor=false')
    return 'Lat: {0}, lng: {1}'.format(
        str(json.loads(r.text)['results'][0]['geometry']['location']['lat']),
        str(json.loads(r.text)['results'][0]['geometry']['location']['lng']))

def cmd_bible(arg=None):
    '''Gives random bible quote. No arg needed.'''
    return requests.get('http://www.ourmanna.com/verses/api/get/?format=text&order=random').text

def cmd_help(arg=None):
    '''Shows this help'''
    retval=''
    for i in cmdList:
        retval+=i.replace('cmd_','/')+' - '+globals()[i].__doc__+'\n'
    return retval

cmdList = [i for i in dir() if callable(globals()[i]) and i.startswith('cmd_')] # stores all defined commands

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        cmdArray = msg['text'].split(' ', 1) # 0 - command, 1 - arg if any
        cmdArray[0] = cmdArray[0].replace('/', 'cmd_')
        if cmdArray[0] in cmdList:
            if len(cmdArray) > 1:
                bot.sendMessage(chat_id, globals()[cmdArray[0]](cmdArray[1]))
            else:
                bot.sendMessage(chat_id, globals()[cmdArray[0]]())
        else:
            print 'Oops! Bot command '+cmdArray[0]+' is not recognized'

bot = telepot.Bot(config.BOT_TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(20)
