var blocks, currSession;

jQuery(function() {
    $("body").on('click', 'button', function(event) {
        return currSession.buttonClick(event.target);
    });
    return currSession.start();
});

blocks = [new BARTTask.Task(true,3), new BARTTask.Task(false,30)];

currSession = new common.Session(blocks);

currSession.start();

