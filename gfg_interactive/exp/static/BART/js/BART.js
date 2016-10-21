(function() {
    var run_BART, pumps, popped, cashed, popPoint, trial;
    trial = 0;
    var dataHandler = DataHandler(sessionid);
    run_BART = (function(){
        reset();
        while (trial <= 30){
            BART_trial();
        }
    })();

    function BART_trial(){
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
                    reset();
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
        run: run_BART
    };



}).call(this);