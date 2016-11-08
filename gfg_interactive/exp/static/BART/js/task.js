var blocks, currSession;

jQuery(function() {
    $("body").on('click', 'button', function(event) {
        return currSession.buttonClick(event.target);
    });
    return currSession.start();
});

blocks = [new BARTTask.Task(false), new BARTTask.Task(true)];

currSession = new common.Session(blocks);

currSession.start();

