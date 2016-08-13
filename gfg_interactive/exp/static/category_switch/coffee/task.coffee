# Category-switch task

trialLength = 5000
ITI = 350
IBI = 3000

red = '#FF6C47'

# Set up canvas
c = document.getElementById("canvas")
ctx = c.getContext("2d")
width = canvas.width
height = canvas.height

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
				setTimeout (=> $('#correct').modal('hide')), 2000
				setTimeout (=> @exitTrial()), 2000
				acc = 1
			else
			## Show incorrect message
				$('#error').modal('show')
				setTimeout (=> $('#error').modal('hide')), 2000
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
		ctx.drawImage(jkey, 88, canvas.height-127, 43, 43)

class LivingKeyMap extends Instruction
	start: (@exitTrial) ->
		super @exitTrial
		ctx.drawImage(fkey, 205, canvas.height-197, 50, 50)
		ctx.drawImage(jkey, 165, canvas.height-130, 50, 50)

class SizeKeyMap extends Instruction
	start: (@exitTrial) ->
		super @exitTrial
		ctx.drawImage(fkey, 165, canvas.height-135, 50, 50)
		ctx.drawImage(jkey, 145, canvas.height-65, 50, 50)

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
		@accs = common.mean(accs)

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

		multilineText("Your average reaction time was: #{common.mean(goodRTs).toString()}ms", 10, 30, "20px Arial")

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
	new common.FinishInstructions
	new PracticeBlock "livingPrac", "Get ready for 12 words!\nRespond quickly without making mistakes", (new PracFeedbackTrial(n[0], n[1]) for n in all_stim['living_prac'])
	new Instruction instructions[9], null, "Continue"
	new Block "livingReal", "Get ready for 34 words!", (new FeedbackTrial(n[0], n[1]) for n in all_stim['living_real'])
	new SizeKeyMap instructions[10], null
	new Instruction instructions[11], " ", " ", "f"
	new Instruction instructions[12], "Back", "Start practice!", null, 'white', '#66FF99'
	new PracticeBlock "sizePrac", "Get ready for 12 words!\n\nRespond quickly without making mistakes", (new PracFeedbackTrial(n[0], n[1]) for n in all_stim['size_prac'])
	new Instruction instructions[13], null, "Start!", null, 'white', '#66FF99'
	new Block "sizeReal", "Get ready for 34 words!\n\nRespond quickly without making mistakes", (new FeedbackTrial(n[0], n[1]) for n in all_stim['size_real'])
	new Instruction instructions[14], null, "Start practice!", null, 'white', '#66FF99'
	new PracticeBlock "mixedPrac", "Get ready for 24 words!\n\nRespond quickly without making mistakes", (new PracFeedbackTrial(n[0], n[1]) for n in all_stim['mixed_prac'])
	new Instruction instructions[15], null, "Start!", null, 'white', '#66FF99'
	new Block "mixedReal1", "Get ready for 54 words!\n\nRespond quickly without making mistakes", (new FeedbackTrial(n[0], n[1]) for n in all_stim['mixed_real_1'])
	new Instruction instructions[16], null, "Start!", null, 'white', '#66FF99'
	new Block "mixedReal2", "Get ready for 54 words!\n\nRespond quickly without making mistakes", (new FeedbackTrial(n[0], n[1]) for n in all_stim['mixed_real_2'])
	new common.Questionnaire
]

currSession = new common.Session(blocks)
fkey.onload = ( -> currSession.start())
jkey.onload = ( -> currSession.start())