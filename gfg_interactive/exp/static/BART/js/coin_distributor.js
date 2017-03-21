var Canvas = document.getElementById('coin_distribution'),
    Context = Canvas.getContext('2d'),
    coins = [],
    Bins = [],
    Deleters = [],
    QuestionMark = {x: Canvas.clientWidth - (Canvas.clientWidth/1.005),y:Canvas.clientHeight/1,width:Canvas.clientHeight/25,height:Canvas.clientHeight/25},
    ContinueButton = {x:Canvas.clientWidth/1.13,y:QuestionMark.y,width:Canvas.clientWidth/10,height:QuestionMark.height},
    ContinueGo = null,
    InstructionsOpen = false;

function Coin(x,bottomed,binindex){
    this.x = x;
    this.y = Canvas.clientHeight/20;
    this.width = Canvas.clientWidth/10;
    this.height = Canvas.clientHeight/25;
    this.speed = 0.1;
    this.gravity = 0.9;
    this.gravitySpeed = 0;
    this.bottomed = bottomed;
    this.binindex = binindex;
}

Coin.prototype.update = function() {
    this.newPos();
    var grd=Context.createLinearGradient(this.x,this.y,this.x + this.width,this.y+this.height);
    grd.addColorStop(0,"#7B7323");
    grd.addColorStop(0.3,"#f5de50");
    grd.addColorStop(1,"#7B7323");
    Context.fillStyle = grd;
    Context.fillRect(this.x,this.y,this.width,this.height);
    Context.rect(this.x,this.y,this.width,this.height);
    Context.stroke();
};

Coin.prototype.newPos = function(){
    this.gravitySpeed += this.gravity;
    this.y += this.speed + this.gravitySpeed;
    this.hitBottom();
};

Coin.prototype.hitBottom = function() {
    if (this.y > this.bottomed){
        this.y = this.bottomed;
    }
};

function newCoin(bin){
    var coin = new Coin(bin.x,bin.bottomed,bin.binIndex);
    coins.push(coin);
}



function Bin(x,i){
    this.x= x;
    this.y= Canvas.clientHeight/14;
    this.width= Canvas.clientWidth/10;
    this.height= Canvas.clientHeight - (Canvas.clientHeight/10);
    this.bottomed = Canvas.clientHeight - (Canvas.clientHeight/25);
    this.inBin = 0;
    this.binIndex = i;
}

Bin.prototype.update = function() {
    Context.strokeStyle="#999999";
    Context.setLineDash([5, 10]);
    Context.beginPath();
    Context.moveTo(this.x,Canvas.clientHeight/20);
    Context.lineTo(this.x,Canvas.clientHeight);
    Context.stroke();
    Context.setLineDash([0,10]);
};



function Deleter(x){
    this.x = x;
    this.y = Canvas.clientHeight - (Canvas.clientHeight/25);
    this.width = Canvas.clientWidth/10;
    this.height = 30;
}

Deleter.prototype.update = function() {
    Context.fillStyle = "#989898";
    Context.fillRect(this.x,this.y,this.width,this.height);
    Context.rect(this.x,this.y,this.width,this.height);
    Context.stroke();
    Context.fillStyle = "#0B2972";
    Context.font = String((Canvas.clientWidth/75)) + "px Arial";
    Context.fillText("REMOVE",this.x + (Canvas.clientWidth/45),this.y + (Canvas.clientHeight/35));
};



function Distribution_init(){
    fitToContainer();
    $('#coin_distribution').show();

    for (i = 0; i < 11; i++){
        b = new Bin(i*(Canvas.clientWidth/10),i);
        x = new Deleter(i*(Canvas.clientWidth/10));
        Bins.push(b);
        Deleters.push(x);
    }
    updateAll();
}

function updateAll(){
    Context.clearRect(0,0,Canvas.clientWidth,Canvas.clientHeight);
    fitToContainer();

    Context.fillStyle = "#000000";
    Context.font = String((Canvas.clientWidth/50)) + "px Arial";
    var results = Bins.map(function(a) {return a.inBin;});
    var sum = results.reduce(function(a, b) { return a + b; }, 0);
    Context.fillText(String(sum) + ' BETS',(Canvas.clientWidth / 2) - 35, (Canvas.clientHeight/30));
    if (sum >= 50){
        Context.fillStyle = "#009108";
        Context.fillRect(Canvas.clientWidth/1.13,QuestionMark.y,Canvas.clientWidth/10,QuestionMark.height);
        Context.stroke();
        Context.fillStyle = "#ffffff";
        Context.font = String((Canvas.clientWidth/50)) + "px Arial";
        Context.fillText('Continue',Canvas.clientWidth/1.12, Canvas.clientHeight/30);
        ContinueGo = true;
    } else{
        ContinueGo = false;
    }

    coins.forEach(function(c){
        c.update();
    });
    Bins.forEach(function(b){
        b.update();
    });
    Deleters.forEach(function(d){
        d.update();
    });

    Context.setLineDash([0,0]);
    Context.rect(QuestionMark.x,QuestionMark.y,QuestionMark.width,QuestionMark.height);
    Context.stroke();
    Context.fillStyle = "#0B2972";
    Context.font = String((Canvas.clientWidth/50)) + "px Arial";
    Context.fillText('?',QuestionMark.x, Canvas.clientHeight/28);

    Context.fillStyle = "black";
    Context.beginPath();
    Context.moveTo(0,Canvas.clientHeight - (Canvas.clientHeight/25));
    Context.lineTo(Canvas.clientWidth,Canvas.clientHeight - (Canvas.clientHeight/25));
    Context.stroke();

    requestAnimationFrame(updateAll);

}

Canvas.addEventListener('click', function(event) {

    var x = event.pageX - Canvas.offsetLeft,
        y = event.pageY - Canvas.offsetTop;
    if (!InstructionsOpen) {
        Bins.forEach(function (bin, i) {
            if (y > bin.y && y < bin.y + bin.height &&
                x > bin.x && x < bin.x + bin.width) {
                if (bin.inBin < 20) {
                    bin.inBin++;
                    bin.bottomed -= (Canvas.clientHeight / 25);

                    newCoin(bin);
                }
            }
        });

        Deleters.forEach(function (d, i) {
            if (y > d.y && y < d.y + d.height &&
                x > d.x && x < d.x + d.width) {
                if (Bins[i].inBin > 0) {
                    Bins[i].inBin -= 1;
                    var results = coins.filter(function (coin) {
                        return coin.x == d.x;
                    });

                    var index = coins.findIndex(function (coin) {
                        return coin.x == results[results.length - 1].x
                            && coin.y == results[results.length - 1].y;
                    });
                    Bins[i].bottomed += (Canvas.clientHeight / 25);
                    coins.splice(index, 1);
                }
            }
        });
        if ( y > QuestionMark.y && y < QuestionMark.y + QuestionMark.height &&
            x > QuestionMark.x && x < QuestionMark.x + QuestionMark.width){

            InstructionsOpen = true;
            $("#hider").show();
        }

    } else {
        if (( y > QuestionMark.y && y < QuestionMark.y + QuestionMark.height &&
            x > QuestionMark.x && x < QuestionMark.x + QuestionMark.width)){
            $("#hider").hide();
            InstructionsOpen = false;

        }
    }
    if (ContinueGo && y > ContinueButton.y && y < ContinueButton.y + ContinueButton.height &&
        x > ContinueButton.x && x < ContinueButton.x + ContinueButton.width) {
        console.log('yes');
        tutorial.removeChart();
    }
}, false);

function fitToContainer(){
    // Make it visually fill the positioned parent
    Canvas.style.width ='60%';
    Canvas.style.height='65%';
    // ...then set the internal size to match
    Canvas.width  = Canvas.offsetWidth;
    Canvas.height = Canvas.offsetHeight;

    Bins.forEach(function(b,i){
        Bins[i].width = Canvas.width/10;
        Bins[i].x = i*(Canvas.clientWidth/10);
        Deleters[i].width = Canvas.width/10;
        Deleters[i].x = i*(Canvas.clientWidth/10);
    });
    coins.forEach(function(c,i){
        coins[i].width = Canvas.width/10;
        coins[i].x = Bins[coins[i].binindex].x;
    });
    QuestionMark.x = Canvas.clientWidth - (Canvas.clientWidth/1.005);
    QuestionMark.y =Canvas.clientHeight - (Canvas.clientHeight/1.005);
    QuestionMark.width = Canvas.clientHeight/25;
    QuestionMark.height = Canvas.clientHeight/25;
    ContinueButton.x = Canvas.clientWidth/1.13;
    ContinueButton.y = QuestionMark.y;
    ContinueButton.width = Canvas.clientWidth/10;
    ContinueButton.height = QuestionMark.height;
}

function addAndSubmitData() {
    var results = Bins.map(function(a) {return a.inBin;});
    results.push(tutorial.maxSize);
    var result = results.join();
    datahandler.recordTrialData({
        'balloon_num': 0,
        'action': 5,
        'pumps': 0,
        'pop_point': 0,
        'dist': result
    });
    datahandler.saveData();
}

function removeInstruction(){
    console.log('h');
    $("#hider").hide();
    InstructionsOpen = false;
}
