var blocks, currSession;

jQuery(function() {
    $("body").on('click', 'button', function(event) {
        return currSession.buttonClick(event.target);
    });
    return currSession.start();
});
var InstructionText = [
        "Throughout this task, you will be presented with 30 balloons, one at a time. <br><br> You will be asked to inflate these balloons. Every time you choose to iinflate the balloon, it will grow slighty and you will receive one token.",
        "You can choose to stop inflating a balloon at any point and collect your tokens by choosing to 'cash in'. <br><br>once you choose to cash in, you will begin again with a new balloon.",
        "It is your choice to determine how much to pump up the balloon, but be aware that at some point the balloon will explode <br><br>The explosion point varies across balloons, ranging from the first pump to enough pumps to make the balloon fill almost the entire containing box.<br><br> if the balloon explodes, you will lose all of your tokens and move on to the next balloon.",
        "At the end of the task you will view a report of your performance in the task.<br><br> To practice with a few balloons, press continue.",
        "This ends your practice block. <br><br>You will now play 30 trials. When you are ready press the continue button.",
        "You have now completed this task. <br><br> if you would like, you can now continue to the review section of this task to review your performance"
    ];

blocks = [ new BART_Instructions(InstructionText[0]),new BART_Instructions(InstructionText[1]),new BART_Instructions(InstructionText[2]),new BART_Instructions(InstructionText[3]),new BART_Block(true),new BART_Instructions(InstructionText[4]), new BART_Block(false),new BART_Instructions(InstructionText[5])];

currSession = new common.Session(blocks);

currSession.start();

