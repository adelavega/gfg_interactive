## Common functions

## Set up PsiTurk and preload the pages that will be shown after task is done
psiTurk = PsiTurk(uniqueId, adServerLoc)
psiTurk.preloadPages(['postquestionnaire.html', 'debriefing.html'])

# Calculates the mean of a numeric array (for feedback)
mean = (numericArray) ->
	sum = numericArray.reduce((a, b) -> a + b)
	avg = sum / numericArray.length

	return avg


# This class simply displays the post questionnaire and 
# collects information from it once button is clocked
class Questionnaire
	start: (@exitTrial) ->
		$('body').html(psiTurk.getPage('postquestionnaire.html'))

	buttonClick: ->
		$("select").each (i, val) ->
		  psiTurk.recordUnstructuredData @id, @value
		  console.log([@id, @value])

		psiTurk.recordUnstructuredData 'openended', $('#openended').val()

		@exitTrial()

# Displays debriefing and when button is clicked ends
class Debriefing
	start: (@exitTrial) ->
		$('body').html(psiTurk.getPage('debriefing.html'))

	buttonClick: ->
		@exitTrial()	

@psiTurk = psiTurk

@common = {
	Questionnaire
	Debriefing
	mean
}