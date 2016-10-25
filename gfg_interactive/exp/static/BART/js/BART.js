(function() {
    var pumps, popped, cashed, popPoint, trial, beginTask
    trial = 0;
    var dataHandler = DataHandler(sessionid);
    var InstructionLIst = [
            "Throughout this task, you will be presented with 30 balloons, one at a time. <br><br> You will be asked to inflate these balloons. Every time you choose to iinflate the balloon, it will grow slighty and you will receive one token.",
            "You can choose to stop inflating a balloon at any point and collect your tokens by choosing to 'cash in'. <br><br>once you choose to cash in, you will begin again with a new balloon.",
            "It is your choice to determine how much to pump up the balloon, but be aware that at some point the balloon will explode <br><br>The explosion point varies across balloons, ranging from the first pump to enough pumps to make the balloon fill almost the entire containing box.<br><br> if the balloon explodes, you will lose all of your tokens and move on to the next balloon.",
            "At the end of the task you will view a report of your performance in the task.<br><br> To practice with a few balloons, press continue."
        ];

     beginTask = function() {
        var warning = "<span style='color:red; font-size:60px'> " + (String.fromCharCode(9888)) + " </span> This task requires 10-15 minutes of your undivided attention. <br><br> If you don't have time right now, please come back when you have can focus. <br><br> Otherwise, click continue to begin!";
        $('#GameBox').hide();
        $('#InstInfo').html(warning);
        $('#rightButton').click(function(){
           $('#instinfo').html(InstructionLIst[0]);
        });
    };


    function instRun(){
        var InstCount = 0;
        $(document).ready(function(){
            $('#InstInfo').html(InstructionLIst[InstCount]);
        $('#rightButton').click(function(){
            InstCount ++;
            $('#InstInfo').html(InstructionLIst[InstCount]);
            if (InstCount >= 1){
                $('#leftButton').show();
            }else{
                $('#leftButton').hide();
            }
        });
        $('#leftButton').click(function(){
            InstCount --;
            $('#InstInfo').html(InstructionLIst[InstCount]);
            if (InstCount >= 1){
                $('#leftButton').show();
            }else{
                $('#leftButton').hide();
            }
        });
    })}


    function BART_run(){
        trial ++;
        pumps = 0;
        popped = false;
        cashed = false;
        popPoint = Math.floor((Math.random() * 64) + 1);
        $(document).ready(function(){
            $("#pumpContainer").click(function(){
                    if(popped == false && cashed == false){
                        $("#balloonIm").animate({height: '+=3.25px', width: '+=3px'}, 50);
                        pumps += 1;
                        dataHandler.recordTrialData({
                            'balloon_num': trial,
                            'action': 1,
                            'pumps': pumps,
                            'pop_point': popPoint
                        });
                        $("#pumpText").text(pumps + ' tokens');
                        if(pumps >= popPoint){
                            popped = true;
                            pumps = 0;
                            $("#pumpContainer").css("pointerEvents","none");

                            dataHandler.recordTrialData({
                                'balloon_num': trial,
                                'action': 0,
                                'pumps': pumps,
                                'pop_point': popPoint
                            });
                        }
                    }
                    if(popped){
                        $("#tokenText").css({top: "-150%", left: "50%", color: "red"});
                        $("#poppedIm").css({
                            height: $("#balloonIm").css('height').toString(),
                            width: $("#balloonIm").css('width').toString(),
                            opacity: "1"
                        });
                        $("#poppedIm").animate({
                            height:"+=25px",
                            width: "+=25px"
                        },{duration: 50, easing: "linear"}).animate({
                            opacity: "0"
                        },{duration: 200, easing: "linear",queue:false});
                        $("#pumpContainer").delay(200).animate({backgroundColor: "#FFB7B7"},{duration: 500, easing: "linear", queue:false});
                        $('#pumpText').delay(200).animate({top: "-50%"}, {duration: 100, easing: 'linear', queue:false});
                        $("#balloonIm").delay(200).animate({bottom: "-150%"},{duration: 100, easing: "linear",queue:false});
                        $("#tokenText").delay(200).animate({top: "50%"},100, "linear").text('POPPED!');
                        $("#cashText").text("Reset");
                        $("#cashContainer").delay(150).animate({backgroundColor: "#BAB5B0"},{duration: 200, easing: "linear", queue:false});
                    }
                }
            );

            $("#cashContainer").click(function() {
                if(popped || cashed){
                    if (trial <= 30){
                        reset();
                    }
                }
                else if(popped == false && cashed == false){
                    $("#tokenText").css({left: "-150%", color: "green"});
                    $("#pumpContainer").animate({backgroundColor: "#86FAC9"},{duration: 500, easing: "linear", queue:false});
                    $('#pumpText').animate({top: "-50%"}, {duration: 250, easing: 'linear', queue:false});
                    $("#balloonIm").animate({left: "150%"},{duration: 200, easing: "linear",queue:false});
                    $("#tokenText").delay(100).animate({left: "50%"},750, "easeOutElastic").text(pumps + ' tokens');
                    $("#cashText").text("Next Trial");
                    $("#cashContainer").animate({backgroundColor: "#BAB5B0"},{duration: 200, easing: "linear", queue:false});
                    cashed = true;
                    dataHandler.recordTrialData({
                        'balloon_num': trial,
                        'action': 2,
                        'pumps': pumps,
                        'pop_point': popPoint
                    });
                }
            });
        });
    };

    function reset(){
        trial++;
        pumps = 0;
        popped = false;
        cashed = false;
        popPoint = Math.floor((Math.random() * 64) + 1);
        $("#balloonIm").css({
            height: "20px",
            width: "20px",
            left: "-100%",
            bottom: "30%"
        });
        if (trial > 0)
            dataHandler.saveData();

        dataHandler.recordTrialData({
            'balloon_num': trial,
            'action': 3,
            'pumps': pumps,
            'pop_point': popPoint
        });

        $('#pumpContainer').animate({backgroundColor: "white"}, {duration: 500, easing:"linear", queue:false});
        $("#pumpText").text("0 tokens").animate({top: "2%"}, {duration: 250, easing: 'linear', queue:false});
        $("#tokenText").animate({left: "150%"},{duration: 200, easing: "linear",queue:false});
        $("#balloonIm").delay(100).animate({left: "50%"},1000, "easeOutElastic").text(pumps + ' tokens');
        $("#cashContainer").css("backgroundColor", "mediumspringgreen");
        $("#cashText").text("CASH IN");
        $("#pumpContainer").css("pointerEvents","auto");
        console.log(trial);
    };

    this.BART = {
        runTask: BART_run,
        begin: beginTask
    };



}).call(this);