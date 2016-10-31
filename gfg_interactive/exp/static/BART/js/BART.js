function BART(){
    this.trial = 0;
    this.pumps = 0;
    this.cashed = false;
    this.popped = false;
    this.popPoint = 0;
}

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

Instructions.prototype.start = function(exitTrial) {
    this.exitTrial = exitTrial;
    $("#inst").html(this.message);
    $("#inst").show();
    hideButtons();
    if (this.leftKey != null) {
        keyText(this.leftKey, 'left');
    }
    return keyText(this.rightKey,'right');
};

