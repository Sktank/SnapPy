/**
 * Created with PyCharm.
 * User: spencertank
 * Date: 2/1/14
 * Time: 6:12 PM
 * To change this template use File | Settings | File Templates.
 */


    // recieve turtle commands from visualizer
window.onmessage = function(e) {
    var data = e.data,
        block,
        command_list,
        command,
        args;

    ////console.log('snap: ' + data);
    data = data.replace(/\s/g, '');
    command_list = data.split(':');
    ////console.log(command_list);
    command = command_list[0];
    args = command_list;
    args.splice(0,1);

    // generates a block based on visualizer message and executes it
    function executeVisualizerCode(message, args) {
        block = SpriteMorph.prototype.blockForSelector(message, true);
        block.parent = window.ide.currentSprite.scripts;
        ////console.log(block.inputs());
        for (var i = 0; i < args.length; i++) {
            block.inputs()[i].setContents(args[i]);
        }
        block.mouseClickLeft();
    }

    // Determines which block to create
    switch (command) {

        // motion
        case 'forward':
            executeVisualizerCode('forward', args);
            break;
        case 'backward':
            args[0] = args[0] * -1;  // multiply argument by -1 because we are going backwards
            executeVisualizerCode('forward', args);
            break;
        case 'right':
            executeVisualizerCode('turn', args);
            break;
        case 'left':
            executeVisualizerCode('turnLeft', args);
            break;
        case 'setpos':
            executeVisualizerCode('gotoXY', args);
            break;
        case 'setx':
            executeVisualizerCode('setXPosition', args);
            break;
        case 'sety':
            executeVisualizerCode('setYPosition', args);
            break;
        case 'seth':
            executeVisualizerCode('setHeading', args);
            break;

        // pen
        case 'clear':
            executeVisualizerCode('clear', args);
            break;
        case 'penup':
            executeVisualizerCode('up', args);
            break;
        case 'pendown':
            executeVisualizerCode('down', args);
            break;
        case 'pensize':
            executeVisualizerCode('setSize', args);
            break;
        case 'stamp':
            executeVisualizerCode('doStamp', args);
            break;
    }
};