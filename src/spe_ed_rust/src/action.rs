
pub mod action{
    use super::super::base::base::State;
    use std::cmp;
    use std::time::{SystemTime, UNIX_EPOCH};

    // return_time = wenn sys time > 0.7 * return time

    pub fn iter_depth(max_player: usize, game_state: State, return_time: f32) ->i8{
        let mut move_to_make = 0;
        println!("rows:{},cols:{}",game_state.rows.len(),game_state.cols.len());
        for i in 7..8 { //Maximum aufheben
            
            match start(max_player, i, game_state.clone(), &return_time) {
                Ok(value) => { move_to_make = value;},
                Err(s) => {return move_to_make;}
            }
        }
        println!("cords pre: {},{}",game_state.players[max_player-1].x,game_state.players[max_player-1].y);
        println!("direction pre: {}",game_state.players[max_player-1].direction);
        let e = game_state.update_gameboard(move_to_make, max_player);
        println!("cords post: {},{}",e.players[max_player-1].x,e.players[max_player-1].y);
        println!("direction post: {}",e.players[max_player-1].direction);
        return move_to_make;
    }

    pub fn start(max_player: usize, depth:i8, game_state: State, return_time: &f32) ->Result<i8,i8>{
       
        
        let mut move_to_make:i8 = 0;
        let mut max_move = -1000;
        let mut a = -1000;

        for i in (0 as i8)..5{
            let mut min_move:i16 = 1000;
            let mut b = 1000;
            for x in 1..7{
                
                if x == max_player || !game_state.players[x-1].active{
                    continue;
                }
                let mut c :i16 = 0;
                match descend(max_player, x, depth-1, a, b, false, game_state.update_gameboard(i, max_player), return_time) {
                    Ok(value) => {c = value;},
                    Err(s) => {return Err(s)}
                }

                min_move = cmp::min(min_move, c);
                b = min_move;
                if a<=b{
                    break;
                }
                
            }
            if min_move >= max_move {
                move_to_make = i;
                max_move = min_move;
                a = max_move;
            }
        } 
        return Ok(move_to_make)
    }

    pub fn descend(max_player: usize, min_player: usize, depth: i8, a : i16, b: i16, max: bool, game_state: State, return_time: &f32) -> Result<i16,i8>{
        //mov: change_nothing = 0, speed_up = 1, slow down = 2, turn_right = 3, turn_left = 4
        if game_state.players[max_player-1].active == false {
            return Ok(-1000);
        }
        if game_state.players[min_player-1].active == false {
            return Ok(1000);
        }
        if depth == 0{
            return Ok(game_state.spielstands_bewertung(max_player, min_player));
        }
        let start = SystemTime::now();
        let since_the_epoch = start.duration_since(UNIX_EPOCH).expect("Time went backwards").as_secs_f32();
        if return_time-since_the_epoch < 1.0 {
            return Err(42);
        }
        //let g = 0.7*(*return_time as f64);
        /*if SystemTime::now().duration_since(UNIX_EPOCH).expect("omg").as_millis()>(g as u128){
            return Err(1);
        }*/
        if max{
            let mut a2 :i16 = a;
            let mut max_move:i16 = -1000;
            for i in 0..5{
                let mut c = 0;
                match descend(max_player, min_player, depth-1, a, b, false, game_state.update_gameboard(i, max_player), return_time) {
                    Ok(value) => {c = value},
                    Err(s) => {return Err(s)}
                }
                max_move = cmp::max(max_move, c);
                a2 = cmp::max(a2, max_move);
                if a2 >= b{
                    break;
                }
            } 
            return Ok(max_move);
        }else{
            let mut b2 = b;
            let mut min_move = 1000;
            for i in 0..5{
                let mut c = 0;
                match descend(max_player, min_player, depth-1, a, b, true, game_state.update_gameboard(i, min_player), return_time) {
                    Ok(value) => {c = value},
                    Err(s) => {return Err(s)}
                }
                min_move = cmp::min(min_move, c);
                b2 = cmp::min(b2, min_move);
                if a <= b2{
                    break;
                }
            }
            return Ok(min_move)
        }
    }
}