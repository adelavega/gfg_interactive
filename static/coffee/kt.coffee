## Keep Track Task

instructions = ["
In this task, you'll see one word at a time from various categories.<br><br>
Your job will be to remember the last word from some of those categories. <br><br>

Let's see how it works!"

"The words you'll see belong to six categories.<br>
Take a second to familiarize yourself with them. "

"You'll be told which categories to pay attention to before you see any words. The categories will stay on the screen, so don't worry about memorizing them. <br><br>
For example, you may be asked to keep track of only words that are <strong>animals</strong>.<br><br>

In this case, you'll want to ignore words from other categories, like <i>countries<i> or <i>metals</i>."

"
Above the categories you'll see one word at a time for two seconds each.<br><br>
For example, you might see the word 'Tiger' followed by 'Yard' and then 'Horse'. <br><br>
If you were asked to keep track of <strong>animals</strong>, the correct answer would be 'Horse', because it was the last animal word we showed you."

"Let's see a short example!<br><br>

You'll see six words in a row.<br><br>	

Keep track of only words that are <strong>animals</strong>. <br><br>
Ignore words from other categories.<br><br>"

"The last Animal word was 'Cat'.  <br><br>
Is that what you saw?<br><br> If you are confused watch that again, otherwise let's learn how to input your responses."

"You'll see a grid with all of the possible words in the categories you were asked to keep track of, like this:<br><br><br><br><br>

To respond, just click on the word you thought was the last of each category. "

"Try entering, 'Cat', the correct answer of the example"

"Good job.
<br><br>Let's do a longer example, this time with two categories.<br><br>
Remember to pay attention to the categories and only keep track of the <i>last</i> 
item from each category"

"Great! You're done with the practice. <br><br>
We're now going to show you 14 more lists<br><br>
You will be asked to keep track of 3 or 4 categories. Pay a lot of attention, this task can get fairly difficult!"

]

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

real_stim = [[["Distances", "Animals", "Countries"], ["Mile", "Cat", "France"], ["Cow", "Germany", "Zinc", "Blue", "Canada", "Mile", "Mother", "Father", "Cat", "Uncle", "Orange", "Sister", "France", "Copper", "Aunt"]], [["Colors", "Metals", "Relatives", "Distances"], ["Black", "Steel", "Father", "Centimeter"], ["Sister", "Brother", "Lion", "Canada", "Meter", "Germany", "Iron", "France", "Foot", "Father", "Black", "Centimeter", "Dog", "Steel", "Horse"]], [["Animals", "Countries", "Colors", "Metals"], ["Tiger", "Mexico", "Blue", "Tin"], ["Yellow", "Mile", "England", "Red", "Sister", "Tiger", "Inch", "Tin", "Mexico", "Centimeter", "Meter", "Yard", "Foot", "Blue", "Father"]], [["Relatives", "Distances", "Animals"], ["Aunt", "Inch", "Lion"], ["Dog", "Platinum", "Iron", "Horse", "Russia", "Aunt", "Green", "Yard", "Inch", "Lion", "Tin", "Yellow", "Steel", "Red", "England"]], [["Countries", "Colors", "Metals"], ["Russia", "Orange", "Platinum"], ["Brother", "Zinc", "Green", "Russia", "Copper", "Horse", "Centimeter", "Platinum", "Tiger", "Meter", "Cat", "Mile", "Orange", "Aunt", "Lion"]], [["Relatives", "Distances", "Animals"], ["Uncle", "Mile", "Cow"], ["Tin", "Foot", "Black", "England", "Uncle", "Red", "Mile", "Mexico", "Lion", "Yellow", "Tiger", "Cow", "Steel", "Orange", "Russia"]], [["Countries", "Colors", "Metals", "Relatives"], ["Germany", "Blue", "Zinc", "Mother"], ["Tin", "Yellow", "Foot", "Germany", "Aunt", "Sister", "Cow", "Tiger", "Lion", "Mother", "Blue", "Iron", "Zinc", "Dog", "Inch"]]]
categories = {"Animals": ["Dog", "Cat", "Tiger", "Horse", "Lion", "Cow"], "Relatives": ["Sister", "Mother", "Brother", "Aunt", "Father", "Uncle"], "Distances" :["Mile", "Centimeter", "Inch", "Foot", "Meter", "Yard"], "Countries" :["Germany", "Russia", "Canada", "France", "England", "Mexico"], "Metals" :["Zinc", "Tin", "Steel", "Iron", "Copper", "Platinum"], "Colors" :["Red", "Green", "Blue", "Yellow", "Black", "Orange"]}

all_cats = ['Distances', 'Relatives', 'Animals', 'Countries', 'Metals', 'Colors']

stimLength = 2000

## Global session class
## Iterates through blocks and other events such as instructions
class Session
	constructor: (@blocks) ->
		hideButtons()
		@blockNumber = 0
		@max_blocks = @blocks.length
		@imgs_loaded = 0
		
	start: ->
		psiTurk.finishInstructions()

		# This ensures that the images for the two buttons are loaded
		# Could probably be done better
		@imgs_loaded++
		if @imgs_loaded is 2
			@nextBlock()

	# Go to next block
	nextBlock: ->
		@currBlock = @blocks[@blockNumber]
		if @blockNumber >= @max_blocks
			@endSession()
		else
			@blockNumber++

			# Start the next block
			# When block ends, call exitBlock with argument
			# Argument is whether to continue or go back (instructions)
			$('.tasktext').html(' ')
			@currBlock.start ((arg1) => @exitBlock arg1)

	# Go back a block	
	prevBlock: ->
		if @blockNumber > 1
			@blockNumber = @blockNumber - 2

		@currBlock = @blocks[@blockNumber]

		@blockNumber++
		@currBlock.start ((arg1) => @exitBlock arg1)

	# This gets called when block is over.
	# Saves data and goes back or forward
	exitBlock: (next = true) ->
		# psiTurk.saveData()
		if next
			@nextBlock()
		else
			@prevBlock()
	
	# Ends it all
	endSession: ->
		psiTurk.completeHIT()
		
	# Handles button clocks (mostly for questionnaires)
	buttonClick: (e) ->
		@currBlock.buttonClick(e)

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
				setTimeout (=> $('#correct').modal('hide')), 1250
				setTimeout (=> @exitTrial()), 1250
				acc = 1
			else
			## Show incorrect message
				$('#error').modal('show')
				setTimeout (=> $('#error').modal('hide')), 1250
				acc = 0
		else # If there is no correct answer, just record what was pressed
			if button.id is 'leftText' or button.id is 'leftButton'
				acc = 'BACK'
				@exitTrial false
			else if button.id is 'rightText' or button.id is 'rightButton'
				acc = 'FORWARD'
				@exitTrial()

		psiTurk.recordTrialData({'block': @message, 'rt': rt, 'resp': button, 'acc': acc})

class InstGrid
	constructor: (@message, @categories=all_cats, @disabled=true, @correct=false, @leftKey = "Back", @rightKey = "Continue") ->
		@maxClicks = @correct.length
		console.log(@correct.length)


	start: (@exitTrial) ->
		fillGrid(@categories)

		$('#inst').html(@message)
		$('#inst').show()

		hideButtons()
		if @leftKey
			console.log(@leftKey)
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
			setTimeout (=> $('#correct').modal('hide')), 1250

		else
			@showError()

	showError: ->
			$('#error').modal('show')
			setTimeout (=> $('#error').modal('hide')), 1250

class Block
	constructor: (@condition, @message, trial_structure) ->
		@trialNumber = 0
		@categories = trial_structure[0]
		@target_words = trial_structure[1]
		@words = (new Word(word, 2000) for word in trial_structure[2])
		@max_trials = @words.length
		@catText = @categories.join("&nbsp&nbsp")
		

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
		) ,stimLength

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
			closeGrid(@exitBlock)
			psiTurk.recordTrialData({'block': @condition, 'target_words': @target_words, 'input_words': @data})
		else  
			$(button).siblings().removeClass('btn-primary')
			$(button).toggleClass('btn-primary')

			console.log(@maxClicks)
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
	Session
	Instruction
	InstGrid
	Block
	PracBlock
	Word
	instructions
	stim
	all_cats
	real_stim
}