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
        if (!practice) {
            $("#InstructionSide").hide();
        }
    }

    Trial.prototype.start = function(exitTrial) {
        this.exitTrial = exitTrial;
        hideButtons();
    };

    Trial.prototype.buttonClick = function(button) {
        if (button.id === 'ContinueButton') {
            this.ended = true;
        }
        else if (button.id === 'mainContainer') {
            if (!this.ended){
                this.balloonNum ++;
                console.log(this.balloonNum);
            }
        }
    };
    return Trial;
})();
