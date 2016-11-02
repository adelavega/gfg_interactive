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
    var  finished, pumps, cashed, popped, maxVal, pauseTime,canvas, ctx, balloon, bWidth,bHeight,vertadd;
    balloon = document.getElementById("balloonIm");
    canvas = document.getElementById("taskcanvas");
    ctx = canvas.getContext('2d');

    finished = false;
    reset();
    $("#pumpCanvas").on('click', function() {

        if (finished == false)
        {
            if (pumps < maxVal) {
                pumps++;
                pump();
            } else {
                pop();
            }
        }
    });
    $("#cashCanvas").on('click', function() {
        cash();
    });

    function reset() {
        this.trial ++;
        pumps = 0;
        finished = false;
        cashed = false;
        popped = false;

        // maxVal = Math.floor((Math.random() * 64) + 1);
        maxVal = 10;
        pauseTime = ((Math.random() * 7) + 1) * 360;
        $("#pumpCanvas").hide();
        ctx.clearRect(0,0,500,500);
        ctx.font = "50px Arial";
        ctx.fillStyle = 'black';
        ctx.textAlign = 'center';
        ctx.fillText("+",canvas.width/2, canvas.height/2);

        setTimeout(function(){
            $("#pumpCanvas").show();
            ctx.clearRect(0,0,500,500);
            ctx.fillStyle = "#60c16d";
            ctx.fillRect(0,400,500,100);

            ctx.font = "30px Arial";
            ctx.fillStyle = 'white';
            ctx.textAlign = 'center';
            ctx.fillText("Cash In",canvas.width/2, 460);

            ctx.font = "30px Arial";
            ctx.fillStyle = 'black';
            ctx.textAlign = 'center';
            ctx.fillText("0 Tokens",canvas.width/2, 50);

            bWidth = 10;
            bHeight = 10;
            vertadd = 0;
            ctx.drawImage(balloon, (canvas.width/2) - bWidth/2, (canvas.height/1.5) - bHeight/2, bWidth, bHeight);
        }, pauseTime);



    }

    function pumpGrow() {
        ctx.clearRect(0,0,500,500);
        bWidth += 1;
        bHeight += 1;
        vertadd += 0.4;
        ctx.drawImage(balloon, (canvas.width/2) - bWidth/2, ((canvas.height/1.5) - bHeight/2) - vertadd , bWidth, bHeight);

        ctx.fillStyle = "#60c16d";
        ctx.fillRect(0,400,500,100);

        ctx.font = "30px Arial";
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        ctx.fillText("Cash In",canvas.width/2, 460);

        ctx.font = "30px Arial";
        ctx.fillStyle = 'black';
        ctx.textAlign = 'center';
        ctx.fillText(pumps.toString() + ' Tokens',canvas.width/2, 50);


    }
    function pump() {

        var startTime = new Date().getTime();
        this.interval = setInterval(function(){

            if(new Date().getTime() - startTime > 75){

                clearInterval(this.interval);
            }
            pumpGrow();

        }, 20);
    }

    function cash() {
        $("#pumpCanvas").hide();
        finished = true;
        console.log('cashed');
        cashed = true;
        ctx.clearRect(0,0,500,500);
        ctx.font = "30px Arial";
        ctx.fillStyle = 'green';
        ctx.textAlign = 'center';
        ctx.globalAlpha = 1;
        ctx.fillText("Cashed In", canvas.width / 2, canvas.height / 2);

        ctx.font = "30px Arial";
        ctx.fillStyle = 'black';
        ctx.textAlign = 'center';
        ctx.fillText(pumps.toString() + ' Tokens',canvas.width/2, 50);
    }

    function pop() {
        $("#pumpCanvas").hide();
        finished = true;
        popped = true;
        pumps = 0;
        var vertsub = 0;
        var popsize = pumps * 10;
        var opacity = 1;
        var startTime = new Date().getTime();
        var starttime2, starttime3;

        this.interval = setInterval(function(){
            if (new Date().getTime() - startTime > 30){
                clearInterval(this.interval);
                starttime2 = new Date().getTime();
            }
            ctx.clearRect(0,0,500,500);
            var Im = document.getElementById("PoppedIm");
            popsize += 10;
            vertsub = popsize;
            ctx.drawImage(Im, (canvas.width/2) - popsize/2, (canvas.height/1.5) - vertsub, popsize,popsize);

            ctx.font = "30px Arial";
            ctx.fillStyle = 'black';
            ctx.textAlign = 'center';
            ctx.fillText(pumps.toString() + ' Tokens',canvas.width/2, 50);
        },20);

        this.interval3 = setInterval(function(){
            if (new Date().getTime() - starttime2 > 60){
                clearInterval(this.interval3);
                starttime3 = new Date().getTime();
            }
            if (starttime2) {
                ctx.clearRect(0,0,500,500);

                var Im = document.getElementById("PoppedIm");
                opacity -= 0.5;
                if (opacity < 0){
                    opacity = 0;
                }
                ctx.globalAlpha = opacity;

                vertsub += 10;
                ctx.drawImage(Im, (canvas.width/2) - popsize/2, (canvas.height/1.5) - vertsub, popsize,popsize);

                ctx.font = "30px Arial";
                ctx.fillStyle = 'black';
                ctx.textAlign = 'center';
                ctx.fillText(pumps.toString() + ' Tokens',canvas.width/2, 50);
            }
        },20);

        this.interval4 = setInterval(function() {
            if (new Date().getTime() - starttime3 > 200){
                clearInterval(this.interval4);
            }
            if (starttime3) {
                ctx.clearRect(0, 0, 500, 500);

                ctx.font = "30px Arial";
                ctx.fillStyle = 'red';
                ctx.textAlign = 'center';
                opacity += 0.5;
                ctx.globalAlpha = opacity;
                ctx.fillText("Popped!", canvas.width / 2, canvas.height / 2);

                ctx.font = "30px Arial";
                ctx.fillStyle = 'black';
                ctx.textAlign = 'center';
                ctx.fillText(pumps.toString() + ' Tokens',canvas.width/2, 50);
            }
        },20);
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
