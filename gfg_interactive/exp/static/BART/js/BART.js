hideButtons = function() {
    $("#leftButton").hide();
    return $("#rightButton").hide();
};

function TaskDisplay(show){
    if (show) {
        $('#taskContainer').show();
        $('#mainContainer').show();
        $('#instructionside').show();
    } else {
        $('#taskContainer').hide();
        $('#mainContainer').hide();
        $('#instructionside').hide();
    }
}



keyText = function(text, key) {
    if (key === 'left') {
        $("#leftText").html(text);
        return $("#leftButton").show();
    } else {
        $("#rightText").html(text);
        return $("#rightButton").show();
    }
};

BART_Instructions = (function () {
    function BART_Instructions(message,leftKey,rightKey) {
        this.message = message;
        this.leftKey = leftKey != null ? leftKey : null;
        this.rightKey = rightKey != null ? rightKey : "Continue";
    }

    BART_Instructions.prototype.start = function(exitTrial) {
        this.exitTrial = exitTrial;
        console.log('starting instructions');
        TaskDisplay(false);

        $("#inst").html(this.message);
        $("#inst").show();
        $('#rightText').text('Next Balloon');
        hideButtons();
        if (this.leftKey != null) {
            keyText(this.leftKey, 'left');
        }
        return keyText(this.rightKey,'right');
    };

    BART_Instructions.prototype.buttonClick = function(button) {
        var acc;
        if (button.id == 'leftText' || button.id == 'leftButton') {
            acc = 'BACK';
            this.exitTrial(false);
        }
        else if (button.id === 'rightText' || button.id === 'rightButton') {
            acc = 'FORWARD';
            this.exitTrial();
        }
    };

    return BART_Instructions;

})();

BART_Block = (function() {
    function BART_Block(practice) {
        this.practice = practice;
        this.balloonNum = 0;
        this.ended = false;
        this.Tokens = 0;
        this.popPoint = Math.floor((Math.random() * 63) + 1);


        this.resetAllDisplay = function() {
            $('#inst').hide();
            $('#taskContainer').show();
            $("#poppedIm").hide();
            $('#resultText').css({opacity: '0'});
            hideButtons();
            $('#ContinueButton').css({opacity:'0'}).hide();
            $("#pumpText").text('0 tokens');
            $("#balloonIm").css({height: '50px', width: '50px', top: '250px'}).show();
            $("#balloonIm").animate({opacity: '1'});
            $('#resultText').css({top: '0px'});
            $('#cashText').text('CASH IN');
            $('#cashBox').animate({opacity:'1'},{queue:false});
        };

    }

    BART_Block.prototype.start = function(exitTrial) {
        TaskDisplay(true);
        this.exitTrial = exitTrial;
        $('#rightText').text('Next Balloon');
        if (!this.practice) {
            $("#InstructionSide").css({opacity:'0'});
            this.maxTrials = 3;
        } else {
            this.maxTrials = 10;
        }
        hideButtons();
        console.log('hi');
        this.resetAllDisplay();
    };

    BART_Block.prototype.buttonClick = function(button) {
        if (button.id === 'ContinueButton') {
            if (this.balloonNum == this.maxTrials -1) {
                this.exitTrial();
            }

            this.Tokens = 0;
            this.ended = false;
            this.balloonNum ++;
            this.popPoint = Math.floor((Math.random() * 63) + 1);
            this.resetAllDisplay();


        }

        else if (button.id === 'pumpBox') {
            if (!this.ended) {
                this.Tokens ++;
                $("#balloonIm").animate({height: '+=3.25px', width: '+=3px', top: '-=3px'}, 50);
                $("#pumpText").text(String(this.Tokens) + ' tokens');


                if (this.Tokens >= this.popPoint) {
                    this.ended = true;
                    $('#resultText').text('Popped');
                    $('#resultText').css({color:'red'});
                    $("#balloonIm").css({opacity:'0'}).hide();
                    $("#pumpText").text('0 tokens');
                    $('#mainContainer').css({backgroundColor: '#FFB7B7'});

                    $('#mainContainer').delay(500)
                        .animate({backgroundColor:'#f8f7ff'},{duration:750,easing:"linear", queue:false});
                    $('#cashBox').delay(500).animate({opacity:'0'},{duration:200, easing:"linear", queue:false});
                    $('#resultText').delay(500).animate({top: '20px' ,opacity:'1'},{duration:750, easing:'linear',queue:false});
                    $('#ContinueButton').show().delay(200).animate({opacity: '1'}, {duration:750});

                    if (this.balloonNum == this.maxTrials -1) {
                        $('#rightText').text('End Section');
                    }
                }
            }
        }

        else if (button.id === 'cashBox') {
            if (!this.ended) {
                this.ended = true;
                $('#resultText')
                    .text('Cashed!')
                    .css({top: '20px', color:'green'});
                $('#balloonIm').animate({opacity:'0'},{duration:200}).hide();
                $('#cashBox').delay(500).animate({opacity:'0'},{duration:750, easing:"linear", queue:false});
                $('#resultText').delay(500).animate({top: '20px' ,opacity:'1'},{duration:750, easing:'linear',queue:false});
                $('#ContinueButton').show().delay(200).animate({opacity: '1'}, {duration:750});

                if (this.balloonNum == this.maxTrials -1) {
                    $('#rightText').text('End Section');
                }
            }
        }
    };


    return BART_Block;

})();
