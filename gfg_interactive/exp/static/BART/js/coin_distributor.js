var Canvas = document.getElementById('coin_distribution'),
    Context = Canvas.getContext('2d'),
    coins = [],
    Bins = [],
    Deleters = [],
    QuestionMark = {x: Canvas.clientWidth/85, y:Canvas.clientHeight/500, width: Canvas.clientHeight/25, height:Canvas.clientHeight/25},
    ContinueButton = {x: Canvas.clientWidth/1.13,y: QuestionMark.y,width: Canvas.clientWidth/10, height: QuestionMark.height},
    ContinueGo = null;
    InstructionsOpen = false;

function Coin(x,bottomed){
    this.x = x;
    this.y = Canvas.clientHeight/20;
    this.width = Canvas.clientWidth/10;
    this.height = Canvas.clientHeight/25;
    this.speed = 0.1;
    this.gravity = 0.9;
    this.gravitySpeed = 0;
    this.bottomed = bottomed;
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
    var coin = new Coin(bin.x,bin.bottomed);
    coins.push(coin);
}



function Bin(x){
    this.x= x;
    this.y= Canvas.clientHeight/14;
    this.width= Canvas.clientWidth/10;
    this.height= Canvas.clientHeight - (Canvas.clientHeight/10);
    this.bottomed = Canvas.clientHeight - (Canvas.clientHeight/25);
    this.inBin = 0;
}

Bin.prototype.update = function() {
    Context.strokeStyle="#999999";
    Context.setLineDash([5, 10]);
    Context.beginPath();
    Context.moveTo(this.x,Canvas.clientHeight/20);
    Context.lineTo(this.x,Canvas.clientHeight);
    Context.stroke();
    Context.strokeStyle="black";
    Context.setLineDash([0,0]);
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
    $('#coin_distribution').css({'z-index':'3','opacity':'1'});
    for (i = 0; i < 11; i++){
        b = new Bin(i*(Canvas.clientWidth/10));
        x = new Deleter(i*(Canvas.clientWidth/10));
        Bins.push(b);
        Deleters.push(x);
    }
    updateAll();
}

function updateAll(){

    Context.clearRect(0,0,Canvas.clientWidth,Canvas.clientHeight);

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

    Context.rect(Canvas.clientWidth/200,QuestionMark.y,QuestionMark.width,QuestionMark.height);
    Context.stroke();
    Context.fillStyle = "#0B2972";
    Context.font = String((Canvas.clientWidth/50)) + "px Arial";
    Context.fillText('?',Canvas.clientWidth/85, Canvas.clientHeight/30);


    requestAnimationFrame(updateAll);

}

Canvas.addEventListener('click', function(event) {
    console.log('clicked');
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
                    console.log(results);
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
            console.log('h');
            InstructionsOpen = true;
            $("#hider").show();
        }

    } else {
        if ( (y > InstructionBox.y && y < InstructionBox.y + InstructionBox.height &&
            x > InstructionBox.x && x < InstructionBox.x + InstructionBox.width) ||
            ( y > QuestionMark.y && y < QuestionMark.y + QuestionMark.height &&
            x > QuestionMark.x && x < QuestionMark.x + QuestionMark.width)){
            $("#hider").hide();
            InstructionsOpen = false;

        }
    }
    if (ContinueGo && y > ContinueButton.y && y < ContinueButton.y + ContinueButton.height &&
            x > ContinueButton.x && x < ContinueButton.x + ContinueButton.width) {
        FinishandEndDistribution();
    }
}, false);


function FinishandEndDistribution() {

    $('#coin_distribution').hide();

}

function removeInstruction(){
    $("#hider").hide();
    InstructionsOpen = false;
}

Distribution_init();

// TODO: program move on functionality and data entry
// TODO: integrate with GFG-BART
