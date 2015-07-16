## Common functions

## Set up PsiTurk and preload the pages that will be shown after task is done
dataHandler = DataHandler(uniqueId, experimentName)

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
		$("select").each (i, val) ->
		  dataHandler.recordUnstructuredData @id, @value
		  console.log([@id, @value])

		dataHandler.recordUnstructuredData 'openended', $('#openended').val()

		@exitTrial()

# Displays debriefing and when button is clicked ends
class Debriefing
	start: (@exitTrial) ->
		$('body').html(dataHandler.getPage('debriefing.html'))

	buttonClick: ->
		@exitTrial()	

@dataHandler = dataHandler

@common = {
	Questionnaire
	Debriefing
	mean
}