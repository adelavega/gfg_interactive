import json
from flask import Blueprint, render_template, request, jsonify, current_app, url_for, redirect


#json validator
def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True

m = "{\"currenttrial\":5,\"data\":[{\"uniqueid\":\"77775\",\"current_trial\":0,\"dateTime\":1448874201972,\"trialdata\":{\"block\":\"In this task, we're going to test your ability \\nto quickly and accurately categorize words.\\n\\n\\n \\t\\t\\t \\t\\t\\t\\t\\t This test requires 10-15 minutes of undivided attention.\\n\\n\\n Press \\t\\t\\t\\t\\t\\t to continue or try again later.\",\"rt\":913,\"resp\":\"j\",\"acc\":\"FORWARD\"}},{\"uniqueid\":\"77775\",\"current_trial\":1,\"dateTime\":1448874202533,\"trialdata\":{\"block\":\"You'll see a series of words, one at the time. \\n\\nAbove each word you'll see a symbol, like this: \\n\\n\\n \\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\u2764\\n \\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\thouse\",\"rt\":558,\"resp\":\"j\",\"acc\":\"FORWARD\"}},{\"uniqueid\":\"77775\",\"current_trial\":2,\"dateTime\":1448874203036,\"trialdata\":{\"block\":\"If the symbol is   \u2764  decide if the word is \\nsomething living or non-living.\\n \\nIf the symbol is   \u2725  decide if the word is\\nsmaller or bigger than a soccer ball.\\n\\n\",\"rt\":503,\"resp\":\"j\",\"acc\":\"FORWARD\"}},{\"uniqueid\":\"77775\",\"current_trial\":3,\"dateTime\":1448874203499,\"trialdata\":{\"block\":\"\\nPop quiz!\\n\\n\\nIf you see a  \u2764 , what do you decide about the word shown?\",\"rt\":461,\"resp\":\"j\",\"acc\":1}},{\"uniqueid\":\"77775\",\"current_trial\":4,\"dateTime\":1448874205437,\"trialdata\":{\"block\":\"\\n\\n\\nAnd if you see a  \u2725 ?\\n\\nWhat do you decide about the word shown?\",\"rt\":682,\"resp\":\"f\",\"acc\":1}}],\"eventdata\":[{\"eventtype\":\"initialized\",\"value\":null,\"timestamp\":1448874201001,\"interval\":0},{\"eventtype\":\"window_resize\",\"value\":[1849,971],\"timestamp\":1448874201001,\"interval\":0}],\"questiondata\":{},\"useragent\":\"\",\"experimentName\":\"category_switch\",\"sessionid\":47,\"uniqueId\":\"77775\",\"status\":\"user data saved\"}"
print "m is valid??", is_json(m)
json_obj = json.loads(m)
#resp = {"status": "user data saved"}
#k = json.dumps(resp) 
#print "after json.dumps---------", k
#print "is it valid?? ", is_json(k)

print "---Lets iterate over m, shall we?--"

print "1. dateTime"
for d in json_obj['data']:
	print d['dateTime']

print "2. get into the trialdata"
for d in json_obj['data']:
	print "current_trial: ", d['current_trial']
	td = d['trialdata']
	print "accuracy: ", td['acc']
	print "responsetime: ", td['rt']
	print "Response: ", td['resp']
	print "block: ", td['block']
	print ""
