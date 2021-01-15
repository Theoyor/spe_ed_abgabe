const statesObj = {
    game:[
        {0:"dummy"},
        {
            width: 10, 
            height: 10, 
            cells: [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 3, 0, 0, 0, 6, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 4, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 5, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 
            players: {
                1: {x: 4, y: 5, direction: "left", speed: 1, active: true, name: "zwei"}, 
                2: {x: 0, y: 0, direction: "left", speed: 1, active: false, name: "zwei"}, 
                3: {x: 2, y: 1, direction: "right", speed: 1, active: true, name: "zwei"}, 
                4: {x: 6, y: 7, direction: "left", speed: 1, active: true, name: "zwei"}, 
                5: {x: 8, y: 3, direction: "left", speed: 1, active: true, name: "zwei"}, 
                6: {x: 2, y: 5, direction: "up", speed: 1, active: true, name: "zwei"}}, 
                you: 1, 
                running: true, 
                deadline: "2020-10-01T12:00:00Z"
            },
        {
            width: 10, 
            height: 10, 
            cells: [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 6, 0, 0, 0, 0], 
                [0, 3, 3, 0, 0, 6, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 4, 4, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 5, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 5, 0, 0, 0, 0, 0, 0]], 
            players: {
                1: {x: 4, y: 6, direction: "left", speed: 1, active: true, name: "zwei"}, 
                2: {x: 0, y: 0, direction: "left", speed: 1, active: false, name: "zwei"}, 
                3: {x: 2, y: 2, direction: "right", speed: 1, active: true, name: "zwei"}, 
                4: {x: 6, y: 8, direction: "left", speed: 1, active: true, name: "zwei"}, 
                5: {x: 9, y: 3, direction: "left", speed: 1, active: true, name: "zwei"}, 
                6: {x: 1, y: 5, direction: "up", speed: 1, active: true, name: "zwei"}}, 
                you: 1, 
                running: true, 
                deadline: "2020-10-01T12:00:00Z"
        }]}
                








unpackStates(JSON.stringify(statesObj));


//hier kommt JSON-String rein

function unpackStates(statesDoc){
    const states = JSON.parse(statesDoc);

    //Initialize layout
    var rowString = (6*states.game[1].height).toString().concat('px')
    var columnString = ' ';
    
    
    let y = 6;
    for (let i = (states.game[1].width/10); i < 11; i++) {
        
        columnString = columnString.concat('auto ')
        if(y == 1){
            break;
        }
        y += 1; 
    }
    
    document.getElementById('wrapper').style.gridAutoRows = rowString;
    document.getElementById('wrapper').style.gridTemplateColumns = columnString;

    
    //console.log(states)
    for (let i = 1; i < states.game.length; i++) {
        unpackOneState(states.game[i], i);
    }

    
}

function unpackOneState(state, round){
    //console.log(state);
    var players = [];
    
    const arr = Object.entries(state.players);
    console.log(arr);

    arr.forEach(player => {
        players = players.concat([{num: player[0], x:player[1].x,y:player[1].y, out: !player[1].active}])

    });

    
    displayOne(state.cells, round, players ,state.width, state.height )
}

function displayOne(field, round, players, width, height){

    var roundString = "Round: "
    roundString = roundString.concat(round.toString());

    var outString = "Out: "
    players.forEach(player => {
        if(player.out){
            outString = outString.concat(player.num.toString());
            outString = outString.concat(", ");
        }
        
    });

    const wrapper = document.getElementById("wrapper");

    const container = document.createElement("div");
    container.setAttribute("class", "stateContainer")
    
    const canvas = document.createElement("canvas");
    
    const status = document.createElement("div")
    status.setAttribute("class", "status")

    
    const header = document.createElement("div");    

    
    header.appendChild(document.createTextNode(roundString));
    status.appendChild(header)
    status.appendChild(document.createTextNode(outString))

    container.appendChild(canvas);
    container.appendChild(status);
    wrapper.appendChild(container);

    canvas.width = 6*height;
    canvas.height = 6*width;
    const ctx = canvas.getContext("2d");

    for (let y = 0; y < field.length; y++) {
        for (let x = 0; x < field[y].length; x++) {
            if(field[x][y] != 0){
                switch (field[x][y]){
                    case 1:
                        ctx.fillStyle = "red";
                        break;
                    case 2:
                        ctx.fillStyle = "lime";
                        break;
                    case 3:
                        ctx.fillStyle = "blue";
                        break;
                    case 4:
                        ctx.fillStyle = "fuchsia";
                        break;
                    case 5:
                        ctx.fillStyle = "yellow";
                        break;
                    case 6:
                        ctx.fillStyle = "aqua";
                        break;
                    default:
                        ctx.fillStyle = "grey";
                        break;
                }
                ctx.fillRect(x*6,y*6,6,6);
            }
        }
        
    }
    //console.log(players);

    players.forEach(player => {
        switch (player.num){
            case "1":
                ctx.fillStyle = "maroon";
                break;
            case "2":
                ctx.fillStyle = "green";
                break;
            case "3":
                ctx.fillStyle = "navy";
                break;
            case "4":
                ctx.fillStyle = "purple";
                break;
            case "5":
                ctx.fillStyle = "olive";
                break;
            case "6":
                ctx.fillStyle = "teal";
                break;
            default:
                ctx.fillStyle = "black";
                break;
            }
            
        //console.log("hiiiii");
        if(!player.out){
            ctx.fillRect(player.x*6,player.y*6,6,6);  
        }
        
    });

    
}




