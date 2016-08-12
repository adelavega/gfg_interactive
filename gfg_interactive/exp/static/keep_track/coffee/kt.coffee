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
	$('#responses').hide()
	func()

clearGrid = ->
	# Reset grid before showing again
	$('.resp').removeClass('btn-primary')

stim = {"pracLists": [[["Animals"], ["Cat"], ["Horse", "Mile", "Steel", "Cat", "Green", "Aunt"]], [["Metals", "Countries"], ["Steel", "Mexico"], ["Red" ,"Blue" ,"Tin" ,"Cow" ,"Yellow" ,"England" ,"Lion" ,"Meter" ,"Inch" ,"Mexico" ,"Black" ,"Brother" ,"Green" ,"Cat" ,"Yard" ,"Aunt" ,"Uncle" ,"Steel" ,"Horse" ,"Father"]]]}

real_stim = [[["Distances", "Animals", "Countries"], ["Mile", "Cat", "France"], ["Father", "Mexico", "Tin", "Germany", "Platinum", "Green", "Orange", "Tiger", "Mile", "Blue", "Steel", "Cat", "France", "Black", "Aunt"]],  [["Colors", "Metals", "Relatives", "Distances"], ["Blue", "Tin", "Brother", "Meter"], ["Horse", "Russia", "Mexico", "Zinc", "Father", "Canada", "Lion", "France", "Sister", "England", "Brother", "Tin", "Meter", "Blue", "Tiger"]],  [["Animals", "Countries", "Colors", "Metals", "Relatives"], ["Horse", "Russia", "Orange", "Copper", "Mother"], ["Canada", "Russia", "Steel", "Platinum", "Uncle", "Centimeter", "Foot", "Copper", "Meter", "Aunt", "Mother", "Yellow", "Horse", "Orange", "Mile"]],  [["Countries", "Colors", "Metals", "Relatives"], ["Mexico", "Red", "Iron", "Mother"], ["Black", "Mile", "Meter", "Aunt", "Horse", "Mexico", "Steel", "Sister", "Copper", "Red", "Inch", "Dog", "Mother", "Iron", "Foot"]],  [["Relatives", "Distances", "Animals", "Countries", "Colors"], ["Uncle", "Foot", "Cat", "Russia", "Yellow"], ["Germany", "Inch", "Steel", "Blue", "Lion", "Orange", "Zinc", "Yellow", "Cat", "Canada", "Foot", "Russia", "Copper", "Uncle", "Tin"]],  [["Metals", "Relatives", "Distances", "Animals"], ["Platinum", "Father", "Mile", "Cow"], ["Platinum", "Centimeter", "Yard", "France", "Mile", "Horse", "Brother", "Red", "Yellow", "Blue", "Father", "Tiger", "Cow", "Green", "Russia"]]]

categories = {"Animals": ["Cat", "Cow", "Dog",  "Horse", "Lion",  "Tiger"], "Relatives": ['Aunt', 'Brother', 'Father', 'Mother', 'Sister', 'Uncle'], "Distances" :['Centimeter', 'Foot', 'Inch', 'Meter', 'Mile', 'Yard'], "Countries" :['Canada', 'England', 'France', 'Germany', 'Mexico', 'Russia'], "Metals" :['Copper', 'Iron', 'Platinum', 'Steel', 'Tin', 'Zinc'], "Colors" :['Black', 'Blue', 'Green', 'Orange', 'Red', 'Yellow']}

all_cats = ['Distances', 'Relatives', 'Animals', 'Countries', 'Metals', 'Colors']

if debug is "True"
	window.stimLength = 50
else
	window.stimLength = 2000

stimLength = window.stimLength
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

		keyText(@rightKey, 'right')

	# Record RT, check if response is correct (if applicable), and 
	buttonClick: (button) ->
		rt = (new Date).getTime() - @startTime

		if @corrResp?
			if @corrResp is button
				$('#correct').modal('show')
				setTimeout (=> $('#correct').modal('hide')), 2000
				hideButtons()
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
				hideButtons()
				@exitTrial false
			else if button.id is 'rightText' or button.id is 'rightButton'
				acc = 'FORWARD'
				hideButtons()
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
			hideButtons()
			closeGrid(@exitTrial false)
		else if button.id is 'rightText' or button.id is 'rightButton'
			if not @correct
				hideButtons()
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
			hideButtons()
			closeGrid(@exitTrial)
			$('#correct').modal('show')
			setTimeout (=> $('#correct').modal('hide')), 1500
			$('#errortext').html("Incorrect! Try again.")
		else
			@showError()

	showError: ->
		if @nClicks >= @triesBeforeHint
			$('#errortext').html("Hint: The correct words are " + @correct.join(', '))

		$('#error').modal('show')
		setTimeout (=> $('#error').modal('hide')), 1800

class Block
	constructor: (@condition, @message, trial_structure, @message2 = ' ') ->
		@trialNumber = 0
		@categories = trial_structure[0]
		@target_words = trial_structure[1]
		@words = (new Word(word, stimLength) for word in trial_structure[2])
		@max_trials = @words.length
		
		upper_cats = [cat.toUpperCase() for cat in @categories]
		@catText = upper_cats[0].join("&nbsp&nbsp&nbsp&nbsp")

	# When block starts, hide buttons, show message, and after IBI start first trial
	start: (@exitBlock) ->
		# Show ready message
		hideButtons()
		$('#inst').html(' ')
		$('#topText').html(@message)
		$('#bottomText').html(@message2)

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
		$('#inst').html("Please enter the last word of each category.")

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
	constructor: (@condition, @message, trial_structure, @message2 = 'Keep track of the last word from each category') ->
		super @condition, @message, trial_structure, @message2
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