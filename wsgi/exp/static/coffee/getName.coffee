jQuery ->
	$("body").on('click','button', (event) ->
		if newstatus == "True"
			if $("#name").val().length < 2
				$("#name").parent().addClass('has-error').addClass('has-feedback')
				$("#name").next().removeClass('hidden')
				$("#namealert").removeClass('hidden')
			else
				whereto = 'task?uniqueId=' + uniqueId + '&experimentName=' + event.target.id + '&debug=' + debug + '&name=' + $("#name").val()
				window.location=whereto
		else
			whereto = 'task?uniqueId=' + uniqueId + '&experimentName=' + event.target.id + '&debug=' + debug
			window.location=whereto

		)


# 