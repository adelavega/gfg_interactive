## Keep Track Task

# Hides left and right buttons
hideButtons = ->
	$("#leftButton").hide()
	$("#rightButton").hide()

# Sets the text of left and right buttoms
keyText = (text, key) ->
	if key is 'left'
		$("#leftText").html(text)
		$("#leftButton").show()
	else
		$("#rightText").html(text)
		$("#rightButton").show()

fillGrid = (cats) ->
	clearGrid()
	$('.btn-group').parent().addClass('hidden') # Hide irrelevant ones


	# Show again
	$('#responses').show().removeClass('hidden')

	i = 1
	for cat in cats
		cdiv = "#c" + i.toString()
		filt = cdiv + ' > button'

		$(cdiv).parent().removeClass('hidden')
		$(cdiv).prev().html(cat + "&nbsp&nbsp")

		x = 0
		$(filt).each ->
			$(this).html(categories[cat][x])
			x = x + 1
		i = i + 1

closeGrid = (func) ->
	$('#responses').fadeOut()
	setTimeout (=> 
		func()
	) , 500

clearGrid = ->
	# Reset grid before showing again
	$('.resp').removeClass('btn-primary')

stim = {"pracLists": [[["Animals"], ["Cat"], ["Horse", "Mile", "Steel", "Cat", "Green", "Aunt"]]
, [["Metals", "Countries"], ["Steel", "Mexico"], ["Red" ,"Blue" ,"Tin" ,"Cow" ,"Yellow" ,"England" ,"Lion" ,"Meter" ,"Inch" ,"Mexico" ,"Black" ,"Brother" ,"Green" ,"Cat" ,"Yard" ,"Aunt" ,"Uncle" ,"Steel" ,"Horse" ,"Father"]]]}

real_stim = [[["Distances", "Animals", "Countries"], ["Mile", "Cat", "France"], ["Father", "Mexico", "Tin", "Germany", "Platinum", "Green", "Orange", "Tiger", "Mile", "Blue", "Steel", "Cat", "France", "Black", "Aunt"]],  [["Colors", "Metals", "Relatives", "Distances"], ["Blue", "Tin", "Brother", "Meter"], ["Horse", "Russia", "Mexico", "Zinc", "Father", "Canada", "Lion", "France", "Sister", "England", "Brother", "Tin", "Meter", "Blue", "Tiger"]],  [["Animals", "Countries", "Colors", "Metals", "Relatives"], ["Horse", "Russia", "Orange", "Copper", "Mother"], ["Canada", "Russia", "Steel", "Platinum", "Uncle", "Centimeter", "Foot", "Copper", "Meter", "Aunt", "Mother", "Yellow", "Horse", "Orange", "Mile"]],  [["Countries", "Colors", "Metals", "Relatives"], ["Mexico", "Red", "Iron", "Mother"], ["Black", "Mile", "Meter", "Aunt", "Horse", "Mexico", "Steel", "Sister", "Copper", "Red", "Inch", "Dog", "Mother", "Iron", "Foot"]],  [["Relatives", "Distances", "Animals", "Countries", "Colors"], ["Uncle", "Foot", "Cat", "Russia", "Yellow"], ["Germany", "Inch", "Steel", "Blue", "Lion", "Orange", "Zinc", "Yellow", "Cat", "Canada", "Foot", "Russia", "Copper", "Uncle", "Tin"]],  [["Metals", "Relatives", "Distances", "Animals"], ["Platinum", "Father", "Mile", "Cow"], ["Platinum", "Centimeter", "Yard", "France", "Mile", "Horse", "Brother", "Red", "Yellow", "Blue", "Father", "Tiger", "Cow", "Green", "Russia"]], [["Distances", "Animals", "Countries", "Colors", "Metals"], ["Yard", "Dog", "England", "Red", "Zinc"], ["Yard", "France", "Iron", "Black", "Green", "Red", "Tin", "Cow", "Brother", "Aunt", "Dog", "Zinc", "England", "Sister", "Uncle"]]]

categories = {"Animals": ["Dog", "Cat", "Tiger", "Horse", "Lion", "Cow"], "Relatives": ["Sister", "Mother", "Brother", "Aunt", "Father", "Uncle"], "Distances" :["Mile", "Centimeter", "Inch", "Foot", "Meter", "Yard"], "Countries" :["Germany", "Russia", "Canada", "France", "England", "Mexico"], "Metals" :["Zinc", "Tin", "Steel", "Iron", "Copper", "Platinum"], "Colors" :["Red", "Green", "Blue", "Yellow", "Black", "Orange"]}

all_cats = ['Distances', 'Relatives', 'Animals', 'Countries', 'Metals', 'Colors']

stimLength = 2000


## Instruction block
## Will display instructions in @message, and set left and right buttons to said text
## Can optionally take a correct response (if incorrect, will not allow you to advance) & button colors
class Instruction
	constructor: (@message, @leftKey = null, @rightKey = "Continue", @corrResp = null) ->

	# Called by Session. Given exit function
	# Starts timer, displays text, and displays buttons that are not null
	start: (@exitTrial) ->
		@startTime = (new Date).getTime()
		$('#inst').html(@message)
		$('#inst').show()
		
		hideButtons()
		if @leftKey?
			keyText(@leftKey, 'left')

		## Show key picture and text next to it
		keyText(@rightKey, 'right')

	# Record RT, check if response is correct (if applicable), and 
	buttonClick: (button) ->
		rt = (new Date).getTime() - @startTime

		if @corrResp?
			if @corrResp is button
				$('#correct').modal('show')
				setTimeout (=> $('#correct').modal('hide')), 2000
				setTimeout (=> @exitTrial()), 2000
				acc = 1
			else
			## Show incorrect message
				$('#error').modal('show')
				setTimeout (=> $('#error').modal('hide')), 2000
				acc = 0
		else # If there is no correct answer, just record what was pressed
			if button.id is 'leftText' or button.id is 'leftButton'
				acc = 'BACK'
				@exitTrial false
			else if button.id is 'rightText' or button.id is 'rightButton'
				acc = 'FORWARD'
				@exitTrial()

		dataHandler.recordTrialData({'block': @message, 'rt': rt, 'resp': button, 'acc': acc})

class InstGrid
	constructor: (@message, @categories=all_cats, @disabled=true, @correct=false, @leftKey = "Back", @rightKey = "Continue") ->
		@maxClicks = @correct.length
		@nClicks = 0
		@triesBeforeHint = 2



	start: (@exitTrial) ->
		fillGrid(@categories)

		$('#inst').html(@message)
		$('#inst').show()

		hideButtons()
		if @leftKey
			keyText(@leftKey, 'left')

		if @rightKey
			keyText(@rightKey, 'right')

		if @correct != false
			keyText('Submit', 'right')
			$('#rightButton').addClass('disabled')
			$('#rightButton').removeClass('btn-success')


	reset: ->
		clearGrid()

	buttonClick: (button) ->
		if button.id is 'leftText' or button.id is 'leftButton'
			closeGrid(@exitTrial false)
		else if button.id is 'rightText' or button.id is 'rightButton'
			if not @correct
				closeGrid(@exitTrial)
			else
				@checkResponses()
		else  
			if not @disabled
				$(button).siblings().removeClass('btn-primary')
				$(button).toggleClass('btn-primary')

				if $('.resp.btn-primary').length == @maxClicks
					$('#rightButton').removeClass('disabled')
					$('#rightButton').addClass('btn-success')
				else if $('.resp.btn-primary').length != @maxClicks
					$('#rightButton').addClass('disabled')
					$('#rightButton').removeClass('btn-success')


	checkResponses: ->
		@nClicks += 1

		responses = $('.resp.btn-primary').map( ->
                 $(this).text()
              ).get()

		# Check if all respones are correct
		# Otherwise complain and reset
		allCorr = true
		for resp in responses
			if resp in @correct == false
				allCorr = false

		if allCorr
			closeGrid(@exitTrial)
			$('#correct').modal('show')
			$('#errortext').html("Try again")
			setTimeout (=> $('#correct').modal('hide')), 1250

		else
			@showError()

	showError: ->
		if @nClicks >= @triesBeforeHint
			$('#errortext').html("The correct words are " + @correct.join(', '))

		$('#error').modal('show')
		setTimeout (=> $('#error').modal('hide')), 1500

class Block
	constructor: (@condition, @message, trial_structure) ->
		@trialNumber = 0
		@categories = trial_structure[0]
		@target_words = trial_structure[1]
		@words = (new Word(word, 2000) for word in trial_structure[2])
		@max_trials = @words.length
		
		upper_cats = [cat.toUpperCase() for cat in @categories]
		@catText = upper_cats[0].join("&nbsp&nbsp")

		

	# When block starts, hide buttons, show message, and after IBI start first trial
	start: (@exitBlock) ->
		# Show ready message
		hideButtons()
		$('#topText').html(@message)

		setTimeout (=> 
			$('#topText').html(" ")
			$('#bottomText').html(@catText)
			setTimeout (=>
				@nextTrial()), stimLength
		) ,stimLength * 2

	nextTrial: ->
		@currTrial = @words[@trialNumber]
		if @trialNumber >= @max_trials
			@trialNumber++
			@getResponses()
		else
			@trialNumber++
			@currTrial.show (=> @nextTrial())

	getResponses: ->
		$('#bottomText').html(" ")
		$('#topText').html(" ")
		$('#inst').html("Please enter the last word of each category")

		keyText('Submit', 'right')

		fillGrid(@categories)
		@maxClicks = @categories.length
		$('#rightButton').addClass('disabled')
		$('#rightButton').removeClass('btn-success')


	buttonClick: (button) ->
		if button.id is 'rightText' or button.id is 'rightButton'
			responses = $('.resp.btn-primary').map( ->
                 $(this).text()
              ).get()

			closeGrid(@exitBlock)
			dataHandler.recordTrialData({'block': @condition, 'target_words': @target_words, 'input_words': responses})
		else  
			$(button).siblings().removeClass('btn-primary')
			$(button).toggleClass('btn-primary')

			if $('.resp.btn-primary').length == @maxClicks
				$('#rightButton').removeClass('disabled')
				$('#rightButton').addClass('btn-success')
			else if $('.resp.btn-primary').length != @maxClicks
				$('#rightButton').addClass('disabled')
				$('#rightButton').removeClass('btn-success')

		
	
class PracBlock extends Block
	constructor: (@condition, @message, trial_structure, speed=3500) ->
		super @condition, @message, trial_structure
		@words = (new Word(word, speed) for word in trial_structure[2])
	getResponses: ->
		$('#bottomText').html(" ")
		$('#topText').html(" ")
		@exitBlock()

# A word class. Shows a word, and waits two seconds. 
class Word
	constructor: (@word, @stimLength=stimLength) ->

	show: (@exitTrial)  ->
		$('#topText').html(@word)
		setTimeout (=> @exitTrial()), @stimLength

@kTrack = {
	InstGrid
	Block
	PracBlock
	Word
	Instruction
	stim
	all_cats
	real_stim
}