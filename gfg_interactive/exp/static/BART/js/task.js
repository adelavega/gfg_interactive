var blocks, currSession;

jQuery(function() {
    $("body").on('click', 'button', function(event) {
        return currSession.buttonClick(event.target);
    });
    return currSession.start();
});

new Trial('yse');
new Trial('no');
// blocks = [new Trial('yes')];

// currSession = new common.Session(blocks);

// currSession.start();

