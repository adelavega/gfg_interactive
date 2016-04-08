## Common functions

## Set up PsiTurk and preload the pages that will be shown after task is done
# dataHandler = PsiTurk(uniqueid, adServerLoc)

## Alternatively set this up for local server hosting using dataHandler.js

dataHandler = DataHandler(uniqueid, experimentname, sessionid)

dataHandler.preloadPages(['postquestionnaire.html', experimentname + '/debriefing.html'])

# Calculates the mean of a numeric array (for feedback)
mean = (numericArray) ->
	sum = numericArray.reduce((a, b) -> a + b)
	avg = sum / numericArray.length

	return avg


# This class simply displays the post questionnaire and 
# collects information from it once button is clocked
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
		  


# Displays debriefing and when button is clicked ends
class Debriefing
	start: (@exitTrial) ->
		$('body').html(dataHandler.getPage(experimentname + '/debriefing.html'))

	buttonClick: ->
		@exitTrial()	


class FinishInstructions
	constructor: ->

	start: (@exitBlock) ->
		dataHandler.finishInstructions()
		@exitBlock()

@dataHandler = dataHandler

@common = {
	Questionnaire
	Debriefing
	FinishInstructions
	mean
}