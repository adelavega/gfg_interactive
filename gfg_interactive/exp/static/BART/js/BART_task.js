
function popAnimation() {
    $("#balloon-image").css({opacity: '0'});
    $("#token-text").text('0 Tokens');
    $('#task-container')
        .animate({backgroundColor: '#ff7272'}, 100);
    $('#result-text').text('Popped!').css({color: '#72090C'})
        .animate({opacity: '1'});
    $('#task-container')
        .animate({backgroundColor: 'white'});
    $('#cash-box').animate({backgroundColor: '#B3B3B3'});
}

function resetBalloon() {
    $('#cash-box').animate({backgroundColor:'#7bb37e'});
    $('#cash-text').html('Cash In');
    $("#token-text").text( '0 Tokens');
    $("#balloon-image")
        .css({
            top: '65%',
            left: '50%',
            height: '100px',
            width: '75px'
        })
        .animate({opacity: '1'});
    $("#result-text")
        .animate({opacity: '0'});
}

function cashDisplay() {
    $("#balloon-image").css({opacity: '0'});
    $('#task-container')
        .animate({backgroundColor: '#41B96B'}, 100);
    $('#result-text').text('cashed in').css({color: 'green'})
        .animate({opacity: '1'});
    $('#task-container')
        .animate({backgroundColor: 'white'});
    $('#cash-box').animate({backgroundColor:'#B3B3B3'});
}

BART_TUTORIAL = function() {
    Bart_tutorial = (function () {
        function BART_tutorial() {
            this.lastClick = new Date().getTime();
            console.log(this.lastClick);
            this.flashinterval = null;
            this.status = null;
            this.tokens = 0;
            this.popPoint = 10;
            this.active = true;
            this.popList = [4, 40, 12, 20, 32, 48, 52, 1, 60, 24, 64, 28, 8, 56, 36, 44, 16];
            this.autotrial = 0;
            this.maxSize = 0;
            this.isDown = false;
            this.barValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        }

        BART_tutorial.prototype.onboarding = function () {
            this.changeStatus('onboarding');
            this.displayInstruction(
                '<strong> Welcome to the BART </strong>' +
                '<br><br> Throughout this task, you will be presented with 30 balloons, one at a time.' +
                '<br><br> You will be asked to inflate these balloons. Every time you choose to inflate the balloon,' +
                ' it will grow slightly and you will receive one token. '
            );
        };

        BART_tutorial.prototype.learntopump = function () {
            this.changeStatus('learntopump');
            $('#continue-instruction').hide();
            this.displayInstruction(
                "To inflate the balloon click or tap anywhere in the upper white space of this container.<br><br>Go ahead and pump as many times as you'd like."
            );
            $('#pump-text').delay(1000).animate({opacity: '1'});
        };

        BART_tutorial.prototype.watchrangeIntro = function () {
            this.changeStatus('onboardWatch');
            this.displayInstruction(
                "We'd like you to now watch several balloons grow to their maximum sizes, to get a feel for what sorts" +
                " of balloons you might encounter. <br><br> Click or tap on this box to view these balloons inflate."
            );
        };

        BART_tutorial.prototype.watchrange = function (required) {

            var self = this;
            var tokens = 0;
            var popat = this.popList[required];
            console.log(popat);
            window.setTimeout(function () {
                resetBalloon();
            }, 1000);

            if (this.autotrial == required) {
                window.setTimeout(function () {
                    var interv = setInterval(function () {
                        tokens++;
                        $("#balloon-image").animate({height: '+=3.25px', width: '+=3px', top: '-=1px'}, 50);
                        $("#token-text").text(String(tokens) + ' Tokens');
                        if (tokens == popat) {
                            $('#progress').css({width: (1+required) * 6.25.toString() + '%'});
                            clearInterval(interv);
                            popAnimation();
                            self.incrementAuto();
                            if (required < self.popList.length - 1) {
                                self.watchrange(required + 1);
                            } else {
                                $('#continue-instruction').show();
                                self.displayInstruction(
                                    "now that you've seen what sorts of balloons you might encounter in this task," +
                                    " we'd like to ask you to tell us where you think the balloon is most likely to pop."
                                );
                                self.changeStatus('maxRating');
                            }
                        }
                    }, 120)
                }, 1500)
            }
        };

        // Trial helper
        BART_tutorial.prototype.incrementAuto = function () {
            this.autotrial++;
        };

        BART_tutorial.prototype.changeStatus = function (status) {
            this.status = status;
        };



        BART_tutorial.prototype.maxRating = function () {
            this.changeStatus('inputMax');
            this.displayInstruction('Before we move on. Please tell us what you think the largest a balloon can grow to is.');
            $('#instructions-box').delay(200).append('<input type="number" id="maxSize" /> <input type="submit" onclick="tutorial.submitMax()" />');
        };


        BART_tutorial.prototype.distribution = function () {
            $('#balloon-image').hide();
            $('#token-text').hide();
            $('#cash-box').hide();
            $('#result-text').hide();
            $('#instructions-box').animate({opacity: '0'}).hide();
            $('#chart').css({visibility: 'visible'}).delay(200).animate({opacity: '1'});
            $('#chart-border').css({visibility: 'visible'}).delay(200).animate({opacity: '1'});

            for (var i = 0; i < 20; i++) {
                var barHTML = "<div id=bar-" + i.toString() + " class='chart-bar'></div>";
                var actionHTML = "<div onmousemove='tutorial.moveInChart(this)' onclick='tutorial.clickInChart(this)' id=action-" + i.toString() + " class='chart-action'></div>";
                $('#chart')
                    .append(barHTML)
                    .append(actionHTML);
                $('#bar-' + i.toString()).css({left: (i * 5).toString() + '%'});
                $('#action-' + i.toString()).css({left: (i * 5).toString() + '%'});
            }
            $('#chart').append(
                "<p style='position: absolute; bottom: -50px; left: 96%'>" + this.maxSize + "</p>" +
                "<p style='position: absolute; bottom: -50px; left: 2%'> 0 </p>" +
                "<h3 style='position:absolute; bottom: -80px; left: 40%;'>  Size (in pumps)</h3>" +
                "<h3 style='position:absolute; bottom: 50%; left:-150px; -webkit-transform: rotate(-90deg);-moz-transform: rotate(-90deg);-ms-transform: rotate(-90deg);-o-transform: rotate(-90deg);transform: rotate(-90deg);'> number of balloons </h3>" +
                "<div id='chart-instruct' onclick='tutorial.startDistribute()'  style=' top: 5px; position: absolute; padding: 10px; text-align: center; left: 5%; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);border-radius:10px; background-color: whitesmoke;border: 2px solid black;'> Please distribute at least 500 balloons to where you believe the balloons in this task are most likely to pop. <br><br>You can click/tap and drag to draw your distribution. Once you have distributed 500 or more balloons you may continue.<br><br>" +
                "<p id='chart-continue' style='font-size: 80%; margin-bottom: -20px; color: #616161;'> click this box to begin this task </p>" +
                "</div>" +
                "<h2 id='distribution-counter' style='position: absolute; top: -100px; width: 100%; text-align: center'> 0 </h2>" +
                "<div onclick='tutorial.removeChart()' id='chart-next' style='position: absolute; left: 90%; top: 110%; background-color: whitesmoke; border: 2px solid black;  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);border-radius:10px; visibility: hidden; padding: 10px;'>Continue</div>"
            );

        };

        BART_tutorial.prototype.startDistribute = function () {
            var self = tutorial;
            $('#chart-instruct').animate({opacity: '0'}, function () {
                $('#chart-instruct').hide();
                self.changeStatus('distributeGo');
            })
        };

        BART_tutorial.prototype.moveInChart = function (e) {
            if (tutorial.status == 'distributeGo') {
                if (tutorial.isDown) {
                    var selfID = e.id;
                    var chartBar = $('#bar-' + selfID.split('-')[1]);
                    var actionY = event.pageY - $('#chart').offset().top;
                    var barHeight = Math.floor(100 - ((actionY / parseInt($('#chart').css('height'), 10)) * 100));

                    chartBar.css({height: barHeight.toString() + '%'});
                    tutorial.barValues[parseInt(selfID.split('-')[1])] = barHeight;
                    tutorial.updateChartText();
                }
            }
        };

        BART_tutorial.prototype.clickInChart = function (e) {
            if (tutorial.status == 'distributeGo') {
                var selfID = e.id;
                var chartBar = $('#bar-' + selfID.split('-')[1]);
                var actionY = event.pageY - $('#chart').offset().top;
                var barHeight = Math.floor(100 - ((actionY / parseInt($('#chart').css('height'), 10)) * 100));

                chartBar.css({height: barHeight.toString() + '%'});
                tutorial.barValues[parseInt(selfID.split('-')[1])] = barHeight;
                tutorial.updateChartText();
            }
        };

        BART_tutorial.prototype.updateChartText = function () {
            var count = 0;
            for (var i = 0; i < tutorial.barValues.length; i++) {
                count += tutorial.barValues[i];
            }
            console.log(count);
            $('#distribution-counter').text(count.toString());
            if (count >= 500) {
                $('#chart-next').css({visibility: 'visible'})
            } else {
                $('#chart-next').css({visibility: 'hidden'})
            }
        };

        BART_tutorial.prototype.submitMax = function () {
            tutorial.changeStatus('Distribution');
            tutorial.displayInstruction('Now you will make a distribution');
            tutorial.maxSize = parseInt($('#maxSize')[0].value);
            $('input').hide().remove();
        };

        BART_tutorial.prototype.removeChart = function () {
            $('#chart').animate({opacity: '0'}, function () {
                $('#chart').remove();
            });
            $('#chart-border').animate({opacity: '0'}, function () {
                $("#chart-border").remove();
            });
            resetBalloon();
            $('#balloon-image').show();
            $('#token-text').show();
            $('#cash-box').show();
            $('#result-text').show();
            $('#pump-box').show();
            $('#continue-instruction').hide();
            $('#instructions-box').animate({opacity: '0'}).show();
            tutorial.changeStatus('learntocash');
            tutorial.displayInstruction(
                "To save your tokens before a balloon pops, you may choose to 'cash in'.<br><br>To cash in, touch anywhere " +
                "inside of the green 'cash in' box at the bottom of this container.<br><br> Go ahead and pump this balloon" +
                " to 10 tokens and cash in."
            );
            tutorial.active = true;
            tutorial.tokens = 0;
        };

        BART_tutorial.prototype.displayInstruction = function (message) {
            var message = message;
            $('#instructions-box').animate({opacity: '0'}, 750, function () {
                $('#instructions-text').html(message);
            }).animate({opacity: '1'}, {duration: 750});
        };

        BART_tutorial.prototype.checkTime = function () {
            clearInterval(this.flashinterval);
            this.lastClick = new Date().getTime();
            var lastClick = this.lastClick;
            this.flashinterval = window.setInterval(function () {
                if (new Date().getTime() - lastClick > 7500) {
                    $('#pump-text')
                        .finish()
                        .animate({opacity: '1'})
                        .delay(500)
                        .animate({opacity: '0'});
                }
            }, 2000)
        };



        return BART_tutorial;

    })();


    BART_task = (function() {
        function BART_task(){
            this.flashinterval = null;
            this.proceed = false;
            this.trial = 0;
            this.tokens = 0;
            this.active = false;
        }

        BART_task.prototype.newTrial = function() {
            if (this.trial <= 29) {
                this.trial++;
                this.tokens = 0;
                this.popPoint = Math.floor((Math.random() * 63) + 1);
                resetBalloon();
                this.active = true;
                this.proceed = false;
            }
        };


        BART_task.prototype.checkTime = function () {
            clearInterval(this.flashinterval);
            this.lastClick = new Date().getTime();
            var lastClick = this.lastClick;
            this.flashinterval = window.setInterval(function () {
                if (new Date().getTime() - lastClick > 7500) {
                    $('#pump-text')
                        .finish()
                        .animate({opacity: '1'})
                        .delay(500)
                        .animate({opacity: '0'});
                }
            }, 2000)
        };


        return BART_task;
    })();



    tutorial = new Bart_tutorial();
    tutorial.onboarding();
    Task = new BART_task();

    $('#instructions-box').click(function() {
        if (tutorial.status === 'onboarding') {
            tutorial.learntopump();
        } else if (tutorial.status === 'popped') {
            tutorial.watchrangeIntro();
        } else if (tutorial.status === 'onboardWatch') {
            $('#progress-container').css({visibility:'visible'});
            $('#instructions-box').animate({opacity:'0'});
            tutorial.watchrange(0);
        } else if (tutorial.status === 'maxRating'){
            $('#progress-container').css({visibility:'hidden'});
            tutorial.maxRating();
        }else if (tutorial.status === 'Distribution') {
            tutorial.distribution();
        } else if (tutorial.status === 'preTask') {
            tutorial.changeStatus('done');
            $('#instructions-box').hide();
            Task.newTrial();
        }
    });

    $("#task-container").mousedown(function() {
        tutorial.isDown = true;
    }).mouseup(function(){
        tutorial.isDown = false;
    });

    $("#pump-box").click(function() {
        if (tutorial.status === 'learntopump') {
            if (tutorial.active) {
                tutorial.tokens++;
                $("#balloon-image").animate({height: '+=3.25px', width: '+=3px', top: '-=1px'}, 50);
                $("#token-text").text(String(tutorial.tokens) + ' Tokens');
                $('#pump-text').animate({opacity: '0'}, tutorial.checkTime());

                if (tutorial.tokens === 7) {
                    tutorial.changeStatus('popped');
                    clearInterval(tutorial.flashinterval);
                    clearInterval(Task.flashinterval);
                    tutorial.active = false;
                    $('#continue-instruction').show();
                    tutorial.displayInstruction(
                        ' <strong>Oh no! It looks like the balloon popped.</strong><br><br>' +
                        'Every balloon that you inflate will have a different maximum size that it can grow to.' +
                        ' Once the balloon gets to its max size, it will pop and you will lose your current tokens.'
                    );
                    popAnimation();
                }
            }
        } else if (tutorial.status === 'learntocash' && tutorial.tokens < 10){
            console.log('hi');
            if (tutorial.active){
                tutorial.tokens++;
                $("#balloon-image").animate({height: '+=3.25px', width: '+=3px', top: '-=1px'}, 50);
                $("#token-text").text(String(tutorial.tokens) + ' Tokens');
                $('#pump-text').animate({opacity: '0'}, Task.checkTime());
            }
        } else if (Task.active){
            clearInterval(tutorial.flashinterval);
            clearInterval(Task.flashinterval);
            console.log(Task.tokens);
            Task.tokens++;
            $("#balloon-image").animate({height: '+=3.25px', width: '+=3px', top: '-=1px'}, 50);
            $("#token-text").text(String(Task.tokens) + ' Tokens');
            $('#pump-text').animate({opacity: '0'}, Task.checkTime());
            if (Task.tokens === Task.popPoint) {
                Task.active = false;
                popAnimation();
                $('#cash-text').html('Next Balloon');
                Task.proceed = true;
            } else if (Task.proceed) {
                Task.newTrial();

            }
        }
    });

    $('#cash-box').click(function(){

        if (tutorial.status === 'learntocash' && tutorial.tokens == 10) {
            if (tutorial.active) {
                $('#continue-instruction').show();
                clearInterval(tutorial.flashinterval);
                clearInterval(Task.flashinterval);
                tutorial.active = false;
                cashDisplay();
                tutorial.displayInstruction(
                    "And that's all there is to it! <br><br> In this task you will be presented with 30 balloons." +
                    " For each balloon you can choose to pump the balloon to whatever size you like before cashing in" +
                    " your tokens. But remember, if you pump the balloon too much, it will explode and you will lose your tokens." +
                    "<br><br>If you are ready to start this task for real, click/tap this box and we will get started."
                );
                tutorial.changeStatus('preTask');

            }
        } else if (Task.active){
            clearInterval(tutorial.flashinterval);
            clearInterval(Task.flashinterval);
            Task.active = false;
            cashDisplay();
            $('#cash-text').html('Next Balloon');
            Task.proceed = true;
        } else if (Task.proceed) {
            Task.newTrial();
        }
    });

}();




