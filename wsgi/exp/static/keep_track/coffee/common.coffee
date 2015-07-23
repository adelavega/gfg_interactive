## Common functions

## Set up PsiTurk and preload the pages that will be shown after task is done
# dataHandler = PsiTurk(uniqueId, adServerLoc)

## Alternatively set this up for local server hosting using dataHandler.js

dataHandler = DataHandler(uniqueId, experimentName)

dataHandler.preloadPages([experimentName + '/postquestionnaire.html', experimentName + '/kt_debriefing.html'])

# Calculates the mean of a numeric array (for feedback)
mean = (numericArray) ->
	sum = numericArray.reduce((a, b) -> a + b)
	avg = sum / numericArray.length

	return avg


# This class simply displays the post questionnaire and 
# collects information from it once button is clocked
class Questionnaire
	start: (@exitTrial) ->
		$('body').html(dataHandler.getPage(experimentName + '/postquestionnaire.html'))

	buttonClick: ->
		$("select").each (i, val) ->
		  dataHandler.recordUnstructuredData @id, @value

		dataHandler.recordUnstructuredData 'openended', $('#openended').val()

		dataHandler.saveData()

		@exitTrial()

# Displays debriefing and when button is clicked ends
class Debriefing
	start: (@exitTrial) ->
		$('body').html(dataHandler.getPage(experimentName + '/kt_debriefing.html'))

	buttonClick: ->
		@exitTrial()	

@dataHandler = dataHandler

@common = {
	Questionnaire
	Debriefing
	mean
}