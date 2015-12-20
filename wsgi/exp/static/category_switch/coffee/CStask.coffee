# Category-switch task

dataHandler = DataHandler(uniqueid, experimentname)
dataHandler.preloadPages(['postquestionnaire.html', experimentname + '/kt_debriefing.html'])

all_stim = {"living_real": [["marble", "nonliv"], ["oak", "living"], ["lizard", "living"], ["coat", "nonliv"], ["sparrow", "living"], ["goldfish", "living"], ["lion", "living"], ["alligator", "living"], ["pebble", "nonliv"], ["shark", "living"], ["knob", "nonliv"], ["table", "nonliv"], ["shark", "living"], ["bicycle", "nonliv"], ["cloud", "nonliv"], ["marble", "nonliv"], ["cloud", "nonliv"], ["alligator", "living"], ["sparrow", "living"], ["lizard", "living"], ["snowflake", "nonliv"], ["mushroom", "living"], ["lion", "living"], ["pebble", "nonliv"], ["bicycle", "nonliv"], ["table", "nonliv"], ["oak", "living"], ["mushroom", "living"], ["knob", "nonliv"], ["marble", "nonliv"], ["coat", "nonliv"], ["goldfish", "living"], ["snowflake", "nonliv"], ["oak", "living"]], "living_prac": [["alligator", "living"], ["snowflake", "nonliv"], ["bicycle", "nonliv"], ["mushroom", "living"], ["cloud", "nonliv"], ["goldfish", "living"], ["lizard", "living"], ["table", "nonliv"], ["marble", "nonliv"], ["shark", "living"], ["knob", "nonliv"], ["lion", "living"]], "mixed_prac": [["marble", "nonliv"], ["table", "nonliv"], ["alligator", "big"], ["sparrow", "small"], ["snowflake", "small"], ["goldfish", "small"], ["mushroom", "living"], ["cloud", "nonliv"], ["knob", "small"], ["oak", "living"], ["marble", "small"], ["bicycle", "nonliv"], ["lizard", "living"], ["knob", "nonliv"], ["lizard", "small"], ["bicycle", "big"], ["pebble", "nonliv"], ["shark", "big"], ["sparrow", "living"], ["lion", "living"], ["goldfish", "living"], ["lion", "big"], ["table", "big"], ["coat", "big"]], "size_prac": [["pebble", "small"], ["bicycle", "big"], ["sparrow", "small"], ["coat", "big"], ["lion", "big"], ["lizard", "small"], ["snowflake", "small"], ["shark", "big"], ["goldfish", "small"], ["knob", "small"], ["cloud", "big"], ["table", "big"]], "size_real": [["table", "big"], ["knob", "small"], ["pebble", "small"], ["oak", "big"], ["bicycle", "big"], ["coat", "big"], ["shark", "big"], ["lizard", "small"], ["alligator", "big"], ["lion", "big"], ["snowflake", "small"], ["bicycle", "big"], ["shark", "big"], ["lizard", "small"], ["table", "big"], ["mushroom", "small"], ["marble", "small"], ["cloud", "big"], ["oak", "big"], ["knob", "small"], ["pebble", "small"], ["sparrow", "small"], ["goldfish", "small"], ["cloud", "big"], ["mushroom", "small"], ["snowflake", "small"], ["goldfish", "small"], ["knob", "small"], ["table", "big"], ["alligator", "big"], ["sparrow", "small"], ["marble", "small"], ["lion", "big"], ["coat", "big"]], "mixed_real_1": [["marble", "nonliv"], ["sparrow", "living"], ["table", "big"], ["lion", "big"], ["sparrow", "small"], ["table", "nonliv"], ["lion", "big"], ["sparrow", "living"], ["cloud", "nonliv"], ["alligator", "big"], ["lizard", "small"], ["marble", "nonliv"], ["table", "big"], ["pebble", "small"], ["shark", "living"], ["coat", "nonliv"], ["alligator", "living"], ["pebble", "small"], ["lion", "living"], ["snowflake", "nonliv"], ["lizard", "living"], ["marble", "small"], ["bicycle", "big"], ["shark", "big"], ["alligator", "living"], ["lizard", "small"], ["lion", "big"], ["goldfish", "small"], ["alligator", "big"], ["pebble", "nonliv"], ["shark", "big"], ["snowflake", "nonliv"], ["mushroom", "living"], ["snowflake", "small"], ["knob", "small"], ["goldfish", "living"], ["cloud", "big"], ["mushroom", "small"], ["bicycle", "nonliv"], ["shark", "living"], ["knob", "small"], ["marble", "small"], ["oak", "big"], ["snowflake", "small"], ["coat", "big"], ["knob", "nonliv"], ["sparrow", "living"], ["lion", "living"], ["coat", "big"], ["mushroom", "living"], ["table", "nonliv"], ["oak", "living"], ["marble", "nonliv"], ["knob", "nonliv"], ["oak", "big"], ["lizard", "living"], ["mushroom", "small"], ["oak", "living"], ["goldfish", "living"], ["bicycle", "nonliv"], ["sparrow", "small"], ["cloud", "nonliv"], ["pebble", "nonliv"], ["goldfish", "small"], ["table", "big"], ["coat", "nonliv"], ["bicycle", "big"], ["cloud", "big"]], "mixed_real_2": [["oak", "big"], ["coat", "big"], ["goldfish", "living"], ["knob", "nonliv"], ["marble", "nonliv"], ["lizard", "small"], ["goldfish", "small"], ["cloud", "nonliv"], ["oak", "big"], ["table", "nonliv"], ["pebble", "nonliv"], ["coat", "big"], ["shark", "living"], ["table", "nonliv"], ["goldfish", "small"], ["coat", "big"], ["lizard", "small"], ["knob", "nonliv"], ["coat", "nonliv"], ["snowflake", "small"], ["marble", "nonliv"], ["mushroom", "small"], ["table", "big"], ["cloud", "big"], ["alligator", "big"], ["lizard", "living"], ["cloud", "nonliv"], ["sparrow", "small"], ["mushroom", "living"], ["alligator", "living"], ["table", "big"], ["goldfish", "living"], ["cloud", "big"], ["lion", "big"], ["snowflake", "nonliv"], ["shark", "living"], ["sparrow", "living"], ["marble", "small"], ["pebble", "nonliv"], ["knob", "nonliv"], ["alligator", "big"], ["shark", "big"], ["pebble", "small"], ["snowflake", "small"], ["bicycle", "big"], ["lion", "living"], ["oak", "living"], ["goldfish", "living"], ["shark", "big"], ["sparrow", "small"], ["oak", "living"], ["mushroom", "living"], ["lizard", "living"], ["bicycle", "big"], ["marble", "small"], ["alligator", "living"], ["snowflake", "nonliv"], ["lion", "living"], ["pebble", "small"], ["oak", "big"], ["coat", "nonliv"], ["bicycle", "nonliv"], ["knob", "small"], ["sparrow", "living"], ["lion", "big"], ["mushroom", "small"], ["knob", "small"], ["bicycle", "nonliv"]]}

instructions = ["In this task, we're going to test your ability \nto quickly and accurately categorize words.\n\n\n
\t\t\t \t\t\t\t\t This test requires 10-15 minutes of undivided attention.\n\n\n

Press \t\t\t\t\t\t to continue or try again later.
"

"You'll see a series of words, one at the time. \n\nAbove each word you'll see a symbol, like this: \n\n\n

\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t#{String.fromCharCode(10084)}\n
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\thouse"

"If the symbol is   #{String.fromCharCode(10084)}  decide if the word is \nsomething living or non-living.\n
\nIf the symbol is   #{String.fromCharCode(10021)}  decide if the word is\nsmaller or bigger than a soccer ball.\n\n",


"\nPop quiz!\n\n\nIf you see a  #{String.fromCharCode(10084)} , what do you decide about the word shown?"

"\n\n\nAnd if you see a  #{String.fromCharCode(10021)} ?\n\nWhat do you decide about the word shown?"


"
For now, let's focus on when you see a  #{String.fromCharCode(10084)}\n\nIf the word describes something...\n\n\n
Non-living, press \t\t\t\t \n\n
Living, press \t\t\t\t \n\n
"

"\n\n\nIf you see a  #{String.fromCharCode(10084)}\n\nwhat key do you press if the word is something living?"

"It's time to practice!\n\nFor this part, \nNON-LIVING things are: \nsnowflake, pebble, marble, knob, bicycle, coat, table, and cloud. \n\nLIVING things are: \nsparrow, mushroom, lizard, goldfish, lion, shark, alligator, and oak. \n\n"

"Remember, respond as quickly as you can\nwithout making mistakes.\n\nIf you make a mistake, you'll see a red circle.\nThe faster you can go while staying accurate, the better!\n\n\nReady to try it?"

"Great. We're done with this practice round.\n\nNow you're going to categorize 34 more words.\nThese will be 'real', not practice words.\n\nRemember to respond as quickly as you can \nwithout making mistakes.
"

"Great, you're done! Now, let's switch gears...\n\nFor now, you'll decide if things are\nsmaller or bigger than a soccer ball.\n\nIf the word describes something...\n\nSmall, press  \n\nBig, press "

"\n\n\nIf you see a #{String.fromCharCode(10021)}, which key do you press for something\nsmaller than a soccer ball?"

"Let's practice!\n\nFor this part, SMALL things are: \nsnowflake, pebble, marble, knob, sparrow, \nmushroom, lizard, and goldfish. \n\nBIG things are: \nbicycle, coat, table, cloud, lion, shark, alligator, and oak. \n\nRemember to respond quickly and accurately!
"

"Great! We're done with this practice round.\n\nNow you're going to categorize 34 more words.\nThese will be 'real', not practice words.\n\nRemember to respond as quickly as you can \nwithout making mistakes.
"

"Now we're going to make it a bit more difficult.\n\nIn this last part, you'll have to switch between both judgments.\n\nRespond according to the symbol above the word. \nIt may be different for every word.\n\nRemember to respond quickly without making mistakes."
"Great, you're done with the practice!\n\nNow you're going to categorize 68 more words.\nThese will be 'real', not practice words.\n\nRemember to respond quickly without making mistakes.\n\nAre you ready?"
"Well done! Go ahead and take a break\n\nNow you're going to categorize 68 more words.\nThese will be 'real', not practice words.\n\nRemember to respond quickly without making mistakes.\n\nAre you ready? This will be the final block!"
]


trialLength = 5000
ITI = 350
IBI = 2000

red = '#FF6C47'

# Set up canvas
c = document.getElementById("canvas")
ctx = c.getContext("2d")
width = canvas.width
height = canvas.height

mean = (numericArray) ->
	sum = numericArray.reduce((a, b) -> a + b)
	avg = sum / numericArray.length

	return avg

# Clears canvas
clear_canvas = ->
	ctx.clearRect(0, 0, canvas.width, canvas.height)# 


# Writes multline text onto the canvas, and by default clears
multilineText = (txt, x, y, font, lineheight=30, clear=true, fillColor='black') ->
	clear_canvas() if clear

	ctx.fillStyle = fillColor
	ctx.font = font

	if x is "center"
		ctx.textAlign = "center"
		x = canvas.width/2 
	else
		ctx.textAlign = "start"

	y = canvas.height/2 if y is "center"

	lines = txt.split('\n')
	i = 0
	while i < lines.length
	  ctx.fillText lines[i], x, y + (i * lineheight)
	  i++

drawCircle = (x, y, radius, fillColor=null, edgecolor='black', behind=true) ->
	ctx.arc(x, y, radius, 0, 2 * Math.PI)

	if behind
		ctx.globalCompositeOperation="destination-over"
	else
		ctx.globalCompositeOperation="source-over"
		
	if edgecolor?
		ctx.lineWidth = 4
		ctx.strokeStyle = edgecolor
		ctx.stroke()

	if fillColor?
		ctx.fillStyle = fillColor
		ctx.fill()

	ctx.globalCompositeOperation="source-over"

hideButtons = ->
	$("#leftButton").hide()
	$("#rightButton").hide()


keyText = (text, key, color) ->
	if key is 'left'
		$("#leftText").html(text)
		$("#leftButton").show()
		$("#leftButton").css('background-color',color)
	else
		$("#rightText").html(text)
		$("#rightButton").show()
		$("#rightButton").css('background-color',color)

class Session
	constructor: (@blocks) ->
		hideButtons()
		@blockNumber = 0
		@max_blocks = @blocks.length
		@imgs_loaded = 0
		
	start: ->
		@imgs_loaded++
		if @imgs_loaded is 2
			@nextBlock()

	nextBlock: ->
		@currBlock = @blocks[@blockNumber]
		if @blockNumber >= @max_blocks
			@endSession()
		else
			@blockNumber++
			@currBlock.start ((arg1) => @exitBlock arg1)
			
	prevBlock: ->
		if @blockNumber > 1
			@blockNumber = @blockNumber - 2

		@currBlock = @blocks[@blockNumber]

		@blockNumber++
		@currBlock.start ((arg1) => @exitBlock arg1)

	exitBlock: (next = true) ->
		dataHandler.saveData()
		if next
			@nextBlock()
		else
			@prevBlock()
	
	endSession: ->
		dataHandler.completeHIT()
		

	keyPress: (e) ->
		code = e.charCode || e.keyCode
		input = String.fromCharCode(code).toLowerCase()

		if input == "j"
			$('rightButton').click()
		
		@currBlock.keyPress input

	buttonClick: ->
		@currBlock.buttonClick()

class Questionnaire
	start: (@exitTrial) ->
		$('body').html(dataHandler.getPage('postquestionnaire.html'))

	buttonClick: ->

		any_blank = false
		$("select").each (i, val) ->
			if @value == "NONE"
				any_blank = true

		if any_blank
			console.log("Some blank")
			$("#noqs").removeClass("hidden")

		else
			$("select").each (i, val) ->
				dataHandler.recordUnstructuredData @id, @value

			dataHandler.recordUnstructuredData 'openended', $('#openended').val()
			dataHandler.saveData()
			@exitTrial()

class Debriefing
	start: (@exitTrial) ->
		$('body').html(dataHandler.getPage('debriefing.html'))

	buttonClick: ->
		@exitTrial()

class Instruction
	constructor: (@message, @left_key = null, @right_key = "Continue", @corrResp = null, @left_color = 'white', @right_color = 'white') ->

	start: (@exitTrial) ->
		@startTime = (new Date).getTime()
		multilineText(@message, 10, 30, "25px Arial", 33)
		
		hideButtons()
		if @left_key?
			keyText(@left_key, 'left', @left_color)

		## Show key picture and text next to it
		keyText(@right_key, 'right', @right_color)

	keyPress: (key) ->
		rt = (new Date).getTime() - @startTime

		if @corrResp?
			if @corrResp is key
				$('#correct').modal('show')
				setTimeout (=> $('#correct').modal('hide')), 1250
				setTimeout (=> @exitTrial()), 1250
				acc = 1
			else
			## Show incorrect message
				$('#error').modal('show')
				setTimeout (=> $('#error').modal('hide')), 1250
				acc = 0
		else
			if key is 'f'
				acc = 'BACK'
				@exitTrial false
			else if key is 'j'
				acc = 'FORWARD'
				@exitTrial()

		dataHandler.recordTrialData({'block':@message, 'rt': rt, 'resp': key, 'acc':acc})


class Slide1 extends Instruction
	start: (@exitTrial) ->
		super @exitTrial
		multilineText("#{String.fromCharCode(9888)}", 0, 185, "80px Arial", 30, false, fillColor='red')
		ctx.drawImage(jkey, 88, canvas.height-267, 43, 43)

class LivingKeyMap extends Instruction
	start: (@exitTrial) ->
		super @exitTrial
		ctx.drawImage(fkey, 205, canvas.height-337, 50, 50)
		ctx.drawImage(jkey, 165, canvas.height-270, 50, 50)

class SizeKeyMap extends Instruction
	start: (@exitTrial) ->
		super @exitTrial
		ctx.drawImage(fkey, 165, canvas.height-275, 50, 50)
		ctx.drawImage(jkey, 145, canvas.height-205, 50, 50)

class FinishInstructions
	constructor: ->

	start: (@exitBlock) ->
		dataHandler.finishInstructions()
		@exitBlock()


class Block
	constructor: (@condition, @message, @trials) ->
		@trialNumber = 0
		@max_trials = @trials.length
		@data = []

	start: (@exitBlock) ->
		# Show ready message
		hideButtons()
		multilineText(@message, "center", "center", "35px Arial", 75)

		setTimeout (=> @nextTrial()), IBI

	nextTrial: ->
		@currTrial = @trials[@trialNumber]
		if @trialNumber >= @max_trials
			@trialNumber++
			@endBlock()
		else
			@trialNumber++
			@currTrial.show ((arg1) => @logTrial arg1)

	endBlock: ->
		@exitBlock()

	logTrial: (trialData) ->
		# Save data to server (or big data file)
		dataHandler.recordTrialData({'block':@condition, 'rt': trialData[0], 'resp': trialData[1], 'acc':trialData[2]})

		# Save data locally in block
		@data.push(trialData)

		@nextTrial()

	keyPress: (key) ->
		@currTrial.logResponse(key)

class PracticeBlock extends Block
	endBlock: ->
		@feedback()

	feedback: ->
		# get accuracy from data
		accs = ((if typeof n[2] == 'string' then 0 else n[2]) for n in @data)
		@accs = mean(accs)

		multilineText("You got #{Math.round(@accs*100.toString(), )}% of trials correct", 10, 60, "30px Arial")

		if @accs < 0.75
			multilineText("You need to get at least 75% right to continue", 10, 130, "25px Arial", 20, false)
			
			keyText("Try again", 'left')
			
			@done = false
		else
			multilineText("Good job, let's continue", 10, 130, "25px Arial", 20, false)
			keyText("Okay, continue", 'right')

			@done = true

	keyPress: (key) ->
		if @trialNumber > @max_trials
			if @done
				if key is 'j'
					@exitBlock()
			else if key is 'f'
				#Dont forget to log trials -add
				@restartBlock()

		else super key

	restartBlock: ->
		trial.reset() for trial in @trials
			
		@trialNumber = 0
		## Save old data -- add this
		@data = []
		hideButtons()

		# Log that practice was restarted
		dataHandler.recordTrialData({'block':@condition, 'rt': 'REST', 'resp': 'REST', 'acc': @accs})

		@nextTrial()

class RTFeedbackBlock extends Block
	endBlock: ->
		@feedback()
		setTimeout (=> @exitBlock()), IBI

	feedback: ->
		# Exclude NAs
		goodRTs = n[0] for n in @data
		goodRTs.splice(goodRTs.indexOf('NA'), 1) while goodRTs.indexOf('NA') > -1

		multilineText("Your average reaction time was: #{mean(goodRTs).toString()}ms", 10, 30, "20px Arial")

class Trial
	constructor: (@item, @corrResp) ->
		@rt = 'NA'
		@resp = 'NA'
		@acc = 'NA'
		@flag = true

	reset: ->
		@rt = 'NA'
		@resp = 'NA'
		@acc = 'NA'
		@flag = true
	show: (@exitTrial)  ->
		clear_canvas()

		# Set upper text to judgment type
		multilineText(@processJudgment(@corrResp), "center", canvas.height/2 - 75, "40px Arial")

		setTimeout (=>
			@flag = false

			# Set middle center text to stimuli
			multilineText(@item, "center", "center", "35px Arial", 20, false)

			# Log trial start time
			@startTime = (new Date).getTime()
			setTimeout (=> @endTrial()), trialLength

			), ITI


	processJudgment: (judgment) ->
		if judgment is "living" or judgment is "nonliv"
			symbol = String.fromCharCode(10084) 
		else
			symbol = String.fromCharCode(10021)

		symbol

	endTrial: ->
		if @flag is false
			@flag = true
			if @acc is 'NA'
				multilineText("You took too long!", "center", canvas.height/2+140, "30px Arial", lineheight = 20, clear=false)
				drawCircle(canvas.width/2, canvas.height/2-40, 100, fillColor = 'lightyellow')
			else
				drawCircle(canvas.width/2, canvas.height/2-40, 100, fillColor = 'lightyellow')

			setTimeout (=> @exitTrial([@rt, @resp, @acc])), ITI

	logResponse: (resp) ->
		if @flag is false
			@rt = (new Date).getTime() - @startTime
			@resp = resp

			if resp is "f"
				if @corrResp is "nonliv" or @corrResp is "small"
					@acc = 1
				else
					@acc = 0
			else if resp is "j"
				if @corrResp is "living" or @corrResp is "big"
					@acc = 1
				else
					@acc = 0
			else
				@acc = 'other'

			@endTrial()

class FeedbackTrial extends Trial
	endTrial: ->
		if @flag is false
			@flag = true

			switch @acc
				when 0
					# clear_canvas()
					drawCircle(canvas.width/2, canvas.height/2-40, 100, red)
					thisITI = ITI
				when 'NA'
					# clear_canvas()
					drawCircle(canvas.width/2, canvas.height/2-40, 100, red)
					thisITI = ITI
				when 1
					clear_canvas()
					thisITI = ITI
				when 'other'
					# clear_canvas()
					multilineText("Use only the F or J keys!", "center", canvas.height/2+140, "30px Arial", lineheight = 20, clear=false)
					drawCircle(canvas.width/2, canvas.height/2-40, 100, red)
					thisITI = ITI

			setTimeout (=> @exitTrial([@rt, @resp, @acc])), thisITI

class PracFeedbackTrial extends Trial
	endTrial: ->
		if @flag is false
			@flag = true
			switch @acc
				when 0
					# clear_canvas()
					drawCircle(canvas.width/2, canvas.height/2-40, 100, red)
					thisITI = ITI
				when 'NA'
					# clear_canvas()
					multilineText("You took too long!", "center", canvas.height/2+140, "30px Arial", lineheight = 20, clear=false)
					drawCircle(canvas.width/2, canvas.height/2-40, 100, red)
					thisITI = ITI
				when 1
					clear_canvas()
					thisITI = ITI
				when 'other'
					# clear_canvas()
					multilineText("Use only the F or J keys!", "center", canvas.height/2+140, "30px Arial", lineheight = 20, clear=false)
					drawCircle(canvas.width/2, canvas.height/2-40, 100, red)
					thisITI = ITI

			setTimeout (=> @exitTrial([@rt, @resp, @acc])), thisITI
			

jQuery ->
	$(document).keypress (event) ->
		currSession.keyPress(event)

	$("body").on('click','button',  ->
		currSession.buttonClick())

blocks = [
	new Slide1 instructions[0]
	new Instruction instructions[1], "Back"
	new Instruction instructions[2], "Back"
	new Instruction instructions[3], "Bigger or smaller than soccer ball", "Living or non-living", "j"
	new Instruction instructions[4], "Bigger or smaller than soccer ball", "Living or non-living", "f"
	new LivingKeyMap instructions[5], "Back"
	new Instruction instructions[6], " ", " ", "j"
	new Instruction instructions[7]	
	new Instruction instructions[8], "Back", "Start practice!", null, 'white', '#66FF99'
	new FinishInstructions
	new PracticeBlock "livingPrac", "Get ready for 12 words!", (new PracFeedbackTrial(n[0], n[1]) for n in all_stim['living_prac'])
	new Instruction instructions[9], null, "Continue"
	new Block "livingReal", "Get ready for 34 words!", (new FeedbackTrial(n[0], n[1]) for n in all_stim['living_real'])
	new SizeKeyMap instructions[10], null
	new Instruction instructions[11], " ", " ", "f"
	new Instruction instructions[12], "Back", "Start practice!", null, 'white', '#66FF99'
	new PracticeBlock "sizePrac", "Get ready for 12 words!", (new PracFeedbackTrial(n[0], n[1]) for n in all_stim['size_prac'])
	new Instruction instructions[13], null, "Start!", null, 'white', '#66FF99'
	new Block "sizeReal", "Get ready for 34 words!", (new FeedbackTrial(n[0], n[1]) for n in all_stim['size_real'])
	new Instruction instructions[14], null, "Start practice!", null, 'white', '#66FF99'
	new PracticeBlock "mixedPrac", "Get ready for 24 words!", (new PracFeedbackTrial(n[0], n[1]) for n in all_stim['mixed_prac'])
	new Instruction instructions[15], null, "Start!", null, 'white', '#66FF99'
	new Block "mixedReal1", "Get ready for 68 words!", (new FeedbackTrial(n[0], n[1]) for n in all_stim['mixed_real_1'])
	new Instruction instructions[16], null, "Start!", null, 'white', '#66FF99'
	new Block "mixedReal2", "Get ready for 68 words!", (new FeedbackTrial(n[0], n[1]) for n in all_stim['mixed_real_2'])
	new Questionnaire
]

currSession = new Session(blocks)

fkey = new Image()
jkey = new Image()

fkey.onload = ( -> currSession.start())
jkey.onload = ( -> currSession.start())

fkey.src = "static/img/f_key.png"
jkey.src = "static/img/j_key.png"