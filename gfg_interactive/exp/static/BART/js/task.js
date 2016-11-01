var blocks, currSession;

jQuery(function() {
    $("body").on('click', 'button', function(event) {
        return currSession.buttonClick(event.target);
    });
    return currSession.start();
});

blocks = [new BART.Instruction(BART.InstructionText[0]),new BART.Instruction(BART.InstructionText[1])];

currSession = new common.Session(blocks);

currSession.start();

