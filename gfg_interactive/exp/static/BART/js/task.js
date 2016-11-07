var blocks, currSession;

jQuery(function() {
    $("body").on('click', 'button', function(event) {
        return currSession.buttonClick(event.target);
    });
    return currSession.start();
});

blocks = [new BARTTask.Instruction(BARTTask.warning), new BARTTask.practice(true), new BARTTask.practice(false)];

currSession = new common.Session(blocks);

currSession.start();

