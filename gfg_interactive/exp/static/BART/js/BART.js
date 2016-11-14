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

function Task() {
    $("#instructionside").show();
    this.reset = reset;
    this.trial = trial;
    this.balloonNum = 0;
}

Task.prototype.start = function(exitTrial) {
    this.exitTrial = exitTrial;
    this.trial();
};

Task.prototype.buttonClick = function() {
    if (this.balloonNum == 2){
        $("#instructionside").hide();
    }
        this.reset();
        this.trial();
    if (this.balloonNum >= 5) {
           this.exitTrial();
    }
};


reset = function() {
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
    this.balloonNum = this.balloonNum + 1;
    console.log(this.balloonNum);
};


trial = function() {
    this.reset();
    var pumps = 0;
    var popPoint = Math.floor((Math.random() * 63) + 1);
    var state = null;

    $('#pumpBox').click(function(){
        if (!state) {
            pumps ++;
            $("#balloonIm").animate({height: '+=3.25px', width: '+=3px', top: '-=3px'}, 50);
            $("#pumpText").text(String(pumps) + ' tokens');
            if (pumps > popPoint){
                state = 'Popped';
                pumps = 0;
                $('#resultText').text('Popped');
                $('#resultText').css({color:'red'});
                $("#balloonIm").css({opacity:'0'}).hide();
                $("#pumpText").text(String(pumps) + ' tokens');
                $('#mainContainer').css({backgroundColor: '#FFB7B7'});

                $('#mainContainer').delay(500)
                    .animate({backgroundColor:'#f8f7ff'},{duration:750,easing:"linear", queue:false});
                $('#cashBox').delay(500).animate({opacity:'0'},{duration:200, easing:"linear", queue:false});
                $('#resultText').delay(500).animate({top: '20px' ,opacity:'1'},{duration:750, easing:'linear',queue:false});
                $('#ContinueButton').show().delay(200).animate({opacity: '1'}, {duration:750});
            }
        }
    });

    $('#cashBox').click(function(){
        if (!state) {
            state = 'cashed';
            $('#resultText')
                .text('Cashed!')
                .css({top: '20px', color:'green'});
            $('#balloonIm').animate({opacity:'0'},{duration:200}).hide();
            $('#cashBox').delay(500).animate({opacity:'0'},{duration:750, easing:"linear", queue:false});
            $('#resultText').delay(500).animate({top: '20px' ,opacity:'1'},{duration:750, easing:'linear',queue:false});
            $('#ContinueButton').show().delay(200).animate({opacity: '1'}, {duration:750});
        }
    });
};


BARTTask = {
    warning : "<span style='color:red; font-size:60px'> " + (String.fromCharCode(9888)) + " </span> This task requires 10-15 minutes of your undivided attention <br><br> If you don't have time right now, please come back when you have can focus. <br><br> Otherwise, click continue to begin!",
    InstructionText : [
        "Throughout this task, you will be presented with 30 balloons, one at a time. <br><br> You will be asked to inflate these balloons. Every time you choose to iinflate the balloon, it will grow slighty and you will receive one token.",
        "You can choose to stop inflating a balloon at any point and collect your tokens by choosing to 'cash in'. <br><br>once you choose to cash in, you will begin again with a new balloon.",
        "It is your choice to determine how much to pump up the balloon, but be aware that at some point the balloon will explode <br><br>The explosion point varies across balloons, ranging from the first pump to enough pumps to make the balloon fill almost the entire containing box.<br><br> if the balloon explodes, you will lose all of your tokens and move on to the next balloon.",
        "At the end of the task you will view a report of your performance in the task.<br><br> To practice with a few balloons, press continue."
    ],
    Instruction: Instruct,
    Task: Task
};
