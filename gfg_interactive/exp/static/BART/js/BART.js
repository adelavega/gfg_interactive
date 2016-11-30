hideButtons = function() {
    $("#leftButton").hide();
    return $("#rightButton").hide();
};

keyText = function(text, key) {
    if (key === 'left') {
        $("#leftText").html(text);
        return $("#leftButton").show();
    } else {
        $("#rightText").html(text);
        return $("#rightButton").show();
    }
};

function Instruct(message,leftKey,rightKey) {
    this.message = message;
    this.leftKey = leftKey != null ? leftKey : null;
    this.rightKey = rightKey != null ? rightKey : "Continue";
}

Instruct.prototype.start = function(exitTrial) {
    this.exitTrial = exitTrial;
    $('#taskContainer').hide();
    $("#inst").html(this.message);
    $("#inst").show();
    hideButtons();
    if (this.leftKey != null) {
        keyText(this.leftKey, 'left');
    }
    return keyText(this.rightKey,'right');
};

Instruct.prototype.buttonClick = function(button) {
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


Trial = (function() {
    function Trial(practice) {
        this.practice = practice;
        this.balloonNum = 0;
        this.ended = false;
        this.Tokens = 0;
        this.popPoint = Math.floor((Math.random() * 63) + 1);
        if (!practice) {
            $("#InstructionSide").hide();
            this.maxTrials = 3;
        } else {
            this.maxTrials = 10;
        }

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

    Trial.prototype.start = function(exitTrial) {
        this.exitTrial = exitTrial;
        hideButtons();
        console.log('hi');
        this.resetAllDisplay();
    };

    Trial.prototype.buttonClick = function(button) {
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


    return Trial;

})();
