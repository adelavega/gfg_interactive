var blocks, currSession;

jQuery(function() {
    $("body").on('click', 'button', function(event) {
        return currSession.buttonClick(event.target);
    });
    return currSession.start();
});

blocks = [new BARTTask.Instruction(BARTTask.InstructionText[1]),new BARTTask.Instruction(BARTTask.InstructionText[2]),new BARTTask.Task(true), new BARTTask.Task(false)];

currSession = new common.Session(blocks);

currSession.start();

