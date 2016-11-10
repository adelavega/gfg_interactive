var blocks, currSession;

jQuery(function() {
    $("body").on('click', 'button', function(event) {
        return currSession.buttonClick(event.target);
    });
    return currSession.start();
});

blocks = [new BARTTask.Instruction(BARTTask.InstructionText[1])];
for (i = 0; i <= 5; i++) {
    blocks.push(new BARTTask.Task(false,i));
}

currSession = new common.Session(blocks);

currSession.start();

