
/* Heavily derived by psiTurk.js
 *
 * 
 * Requires:
 *     jquery
 *     backbone
 *     underscore
 */

/****************
 * Internals    *
 ***************/

// Sets up global notifications pub/sub
// Notifications get submitted here (via trigger) and subscribed to (via on)
Backbone.Notifications = {};
_.extend(Backbone.Notifications, Backbone.Events);


/*******
 * API *
 ******/
//Called from from CStask.js or KTtask.js

//Added session id as well
var DataHandler = function(sessionid) {
	var self = this;
	/****************
	 * TASK DATA    *
	 ***************/
	var TaskData = Backbone.Model.extend({
		urlRoot: "sync/", // Save will PUT to /sync (data obj), with mimetype 'application/JSON'
		id: sessionid,

		defaults: {
			currenttrial: 0,
			data: [],
			eventdata: [],
			questiondata: {},
			useragent: ""
		},
		/*	******* HOW IS THE JSON BUILT UP ???? **********************
			Each function builds up the JSON (key-value pairs)
			initialize - just loads data about window resize etc. [Status = 0]
			addTrialData - 'data' gets populated with each new trial in the instructions phase [Status=1]
			addUnstructuredData - 'questiondata' gets populatedwith the questions only once the user enters the actual experiment phase [Status = 2]
									maybe empty if the user decides to quit at instructions phase itself
			addEvent - Just like addTrialData, 'eventdata' getspopulated with every new event & its details(of coz) as and when the event 'initialized' is triggerd
		*/
		/************************************************
					   SETTER FUNCTIONS
		************************************************/
		initialize: function() {
			this.useragent = navigator.userAgent;
			this.addEvent('initialized', null);
			this.addEvent('window_resize', [window.innerWidth, window.innerHeight]);

			this.listenTo(Backbone.Notifications, '_psiturk_lostfocus', function() { this.addEvent('focus', 'off'); });
			this.listenTo(Backbone.Notifications, '_psiturk_gainedfocus', function() { this.addEvent('focus', 'on'); });
			this.listenTo(Backbone.Notifications, '_psiturk_windowresize', function(newsize) { this.addEvent('window_resize', newsize); });
		},

		//populates the "data" in JSON and appends each new trrial to it
		// New Model -  we need to add each trail as a new row in the table - Category_switch 
		addTrialData: function(trialdata) {
			trialdata = {"sessionid":this.id, "current_trial":this.get("currenttrial"), "dateTime":(new Date().getTime()), "trialdata":trialdata};
			var data = this.get('data');
			data.push(trialdata);
			this.set('data', data);
			this.set({"currenttrial": this.get("currenttrial")+1});		//updates the current trial number
		},

		//set the recieved reponse from the user in  the 'questiondata' key of the JSON
		addUnstructuredData: function(field, response) {
			var qd = this.get("questiondata");
			qd[field] = response;
			this.set("questiondata", qd);
		},

		//if window resized etc then add the data to 'eventdata'
		addEvent: function(eventtype, value) {
			var interval;
			var ed = this.get('eventdata');
			var timestamp = new Date().getTime();

			if (eventtype == 'initialized') {
				interval = 0;
			} else {
				interval = timestamp - ed[ed.length-1]['timestamp'];
			}
			ed.push({'eventtype': eventtype, 'value': value, 'timestamp': timestamp, 'interval': interval});
			this.set('eventdata', ed);
		},
		
		/************************************************
					   GETTER FUNCTIONS
		************************************************/
		getTrialData: function() {
			return this.get('data');	
		},
		
		getEventData: function() {
			return this.get('eventdata');	
		},
		
		getQuestionData: function() {
			return this.get('questiondata');	
		}
	});		//End of Taskdata


	/* *********************************** 
				PUBLIC METHODS
	*********************************** */
	self.preloadImages = function(imagenames) {
		$(imagenames).each(function() {
			image = new Image();
			image.src = this;
		});
	};
	
	//I dont get this :(
	self.preloadPages = function(pagenames) {
		// Synchronously preload pages.
		$(pagenames).each(function() {
			$.ajax({
				url: this,
				success: function(page_html) { self.pages[this.url] = page_html;},
				dataType: "html",
				async: false
			});
		});
	};

	// Get HTML file from collection and pass on to a callback
	self.getPage = function(pagename) {
		if (!(pagename in self.pages)){
		    throw new Error(
			["Attemping to load page before preloading: ",
			pagename].join(""));
		};
		return self.pages[pagename];
	};
	
	
	// Add a line of data with any number of columns
	self.recordTrialData = function(trialdata) {
		taskdata.addTrialData(trialdata);
	};
	
	// Add data value for a named column. If a value already
	// exists for that column, it will be overwritten
	self.recordUnstructuredData = function(field, value) {
		taskdata.addUnstructuredData(field, value);
	};

	self.getTrialData = function() {
		return taskdata.getTrialData();	
	};
		
	self.getEventData = function() {
		return taskdata.getEventData();	
	};
		
	self.getQuestionData = function() {
		return taskdata.getQuestionData();	
	};
	
	// Save data to server
	self.saveData = function(callbacks) {
		taskdata.save(undefined, callbacks);
	};

	self.startTask = function () {
		self.saveData();		

		$.ajax("inexp", {
				type: "POST",
				data: {'sessionid': self.taskdata.id}
		});
		
		if (self.taskdata.mode != 'debug') {  //don't block people from reloading in debug mode
			// Provide opt-out 
			$(window).on("beforeunload", function(){
				self.saveData();
				$.ajax("quitter", {
						type: "POST",
						data: {'sessionid': self.taskdata.id}
				});
				return "By leaving or reloading this page, you opt out of the experiment.  Are you sure you want to leave the experiment?";
			});
		}

	};
	
	// Notify app that participant has begun main experiment
	self.finishInstructions = function(optmessage) {
		Backbone.Notifications.trigger('_psiturk_finishedinstructions', optmessage);
	};
	
	self.teardownTask = function(optmessage) {
		Backbone.Notifications.trigger('_psiturk_finishedtask', optmessage);
	};

	self.completeHIT = function() {
		self.teardownTask();
		$(window).unbind('beforeunload');
		$.ajax("worker_complete", {
			type: "POST",
			data: {'sessionid': self.taskdata.id}
		});

		// https://gfg-dev-2.sph.umich.edu/gfg/lib/interactive_survey_module_handler.php
		// $.ajax("/lib/interactive_survey_module_handler.php", {
		$.ajax("/lib/interactive_survey_module_handler.php", {
			type: "POST",
			data: {
				action: "complete"
		}
		});

		opener.completeInteractiveSurvey()

		window.close()
	}

	// To be fleshed out with backbone views in the future.
	var replaceBody = function(x) { $('body').html(x); };

	self.showPage = _.compose(replaceBody, self.getPage);

	/* initialized local variables */

	var taskdata = new TaskData();
	taskdata.fetch({async: false});
	
	/*  DATA: */
	self.pages = {};
	self.taskdata = taskdata;


	/* Backbone stuff */
	Backbone.Notifications.on('_psiturk_finishedinstructions', self.startTask);
	Backbone.Notifications.on('_psiturk_finishedtask', function(msg) { $(window).off("beforeunload"); });


	$(window).blur( function() {
		Backbone.Notifications.trigger('_psiturk_lostfocus');
	});

	$(window).focus( function() {
		Backbone.Notifications.trigger('_psiturk_gainedfocus');	
	});

	// track changes in window size
	var triggerResize = function() {
		Backbone.Notifications.trigger('_psiturk_windowresize', [window.innerWidth, window.innerHeight]);
	};

	// set up the window resize trigger
	var to = false;
	$(window).resize(function(){
	 if(to !== false)
	    clearTimeout(to);
	 to = setTimeout(triggerResize, 200);
	});

	return self;
};
