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


function PracticeBlock() {
    this.trial = 0;
};

PracticeBlock.prototype.start = function(exitTrial) {
    this.exitTrial = exitTrial;
    $('#inst').hide();
    $('#taskContainer').show();
    hideButtons();
    this.Trial();
};

PracticeBlock.prototype.Trial = function(exiTrial) {
    var elements, pumps, cashed, popped, maxVal, pauseTime,canvas, ctx, balloon, bWidth,bHeight,vertadd;

    balloon = document.getElementById("balloonIm");
    canvas = document.getElementById("taskcanvas");
    ctx = canvas.getContext('2d');
    elements = [];

    reset();
    $("#pumpCanvas").on('click', function() {
        pumps ++;
        if (pumps < maxVal){
            pump();
        }else{
            //pop
        }
    });
    $("#cashCanvas").on('click', function() {
        console.log('cash');
    });

    function reset() {
        this.trial ++; 
        pumps = 0;
        cashed = false;
        popped = false;
        maxVal = Math.floor((Math.random() * 64) + 1);
        pauseTime = (Math.random() * 5) + 1;
        ctx.fillStyle = "#60c16d";
        ctx.fillRect(0,400,500,100);
        ctx.font = "30px Arial";
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        ctx.fillText("Cash In",canvas.width/2, 475);
        bWidth = 10;
        bHeight = 10;
        vertadd = 0;
        ctx.drawImage(balloon, (canvas.width/2) - bWidth/2, (canvas.height/1.5) - bHeight/2, bWidth, bHeight);
    }

    function pumpGrow() {
        ctx.clearRect(0,0,500,500);
        bWidth = bWidth + 7.5;
        bHeight = bHeight + 7.5;
        vertadd = vertadd + 3;
        console.log(bWidth,bHeight);
        ctx.drawImage(balloon, (canvas.width/2) - bWidth/2, ((canvas.height/1.5) - bHeight/2) - vertadd , bWidth, bHeight);

        ctx.fillStyle = "#60c16d";
        ctx.fillRect(0,400,500,100);
        ctx.font = "30px Arial";
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        ctx.fillText("Cash In",canvas.width/2, 475);
    }
    function pump() {
        this.interval = setInterval(pumpGrow, 20);
    }

    function pop() {
        ctx.clearRect(0,0,500,500);

    }



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
    practice: PracticeBlock
};
