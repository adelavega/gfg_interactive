var blocks, currSession;

jQuery(function() {
    $("body").on('click', 'button', function(event) {
        return currSession.buttonClick(event.target);
    });
    return currSession.start();
});


blocks = [new Trial(true), new Trial(false)];

currSession = new common.Session(blocks);

currSession.start();

