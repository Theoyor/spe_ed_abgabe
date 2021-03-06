
pub mod action{
    use super::super::base::base::State;
    use std::cmp;
    use std::time::{SystemTime, UNIX_EPOCH};

    // Iterative Funktion zum Aufrufen der rekursiven Funktion
    // Rückgabewert wird für alle Tiefen einzeln berechnet
    // Wenn die Zeit zu knapp wird, gebe letztes vollständig berechnetes Ergebnis zurück
    // Die Zeitberechnung hat kurzfristig versagt, daher immer mit Suchtiefe 12, die sollte immer schnell genug sein.
    pub fn iter_depth(max_player: usize, game_state: State, return_time: f32) ->i8{
        let mut move_to_make = 0;
        for i in 12..13 {
            match start(max_player, i, game_state.clone(), &return_time) {
                Ok(value) => {
                    move_to_make = value;},
                Err(s) => {
                    println!("Erreichte Tiefe: {}, fehler: {}", i-1, s);
                    return move_to_make;}
            }
        }
        return move_to_make;
    }

    // Unsere Ausführung des Multi-Minimax Algorithmus
    pub fn start(max_player: usize, depth:i8, game_state: State, return_time: &f32) ->Result<i8,i8>{
        
        let mut move_to_make:i8 = 0;
        let mut max_move = -1000;
        let mut a = -1000;

        // Gehe jeden move durch und gib das beste Ergebnis zurück
        for i in (0 as i8)..5{
            let mut min_move:i16 = 1000;
            let mut b = 1000;
            // Spiele das Spiel gegen jeden Gegner einzeln weiter.
            // move kriegt den Wert, von dem Gegner gegen wir am schlechtesten Abschneiden
            for x in 1..7{
                
                if x == max_player || !game_state.players[x-1].active{
                    continue;
                }
                let mut c :i16 = 0;
                // Hier wird abgestiegen mit normalen miniMax und AlphaBeta Pruning
                match descend(max_player, x, depth-1, a, b, false, game_state.update_gameboard(i, max_player), return_time) {
                    Ok(value) => {c = value;},
                    Err(s) => {return Err(s)}
                }
                min_move = cmp::min(min_move, c);
                b = min_move;
                if a>=b{
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

    // Minmax algorithmus mit AlphaBeta Pruning
    pub fn descend(max_player: usize, min_player: usize, depth: i8, a : i16, b: i16, max: bool, game_state: State, return_time: &f32) -> Result<i16,i8>{
        //mov: change_nothing = 0, speed_up = 1, slow down = 2, turn_right = 3, turn_left = 4

        // Abbruch falls wir oder Gegner tot sind. Je später wir sterben desto besser, je früher der Gegner
        // stirbt desto besser
        if game_state.players[max_player-1].active == false {
            return Ok(-1000-depth as i16);
        }
        if game_state.players[min_player-1].active == false {
            return Ok(1000+depth as i16);
        }
        // Wenn maximal Tiefe erreicht
        if depth == 0{
            return Ok(game_state.spielstands_bewertung(max_player, min_player));
        }
        /*
        let start = SystemTime::now();
        let since_the_epoch = start.duration_since(UNIX_EPOCH).expect("Time went backwards").as_secs_f32();
        // Wenn weniger als 1 Sekunde verbleibend abbrechen
        if return_time-since_the_epoch < 1.0 {
            println!("Zeit abgelaufen, jetzt : {}",since_the_epoch);
            println!("Zeit abgelaufen, deadline : {}",return_time);
            println!("Zeit abgelaufen, differenz : {}",return_time-since_the_epoch);
            return Err(42);
        }
        */
        // Wenn maximiert wird
        if max{
            let mut a2 :i16 = a;
            let mut max_move:i16 = -1000;
            for i in 0..5{
                let mut c = 0;
                match descend(max_player, min_player, depth-1, a2, b, false, game_state.update_gameboard(i, max_player), return_time) {
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
            // Wenn minimiert wird
            let mut b2 = b;
            let mut min_move = 1000;
            for i in 0..5{
                let mut c = 0;
                match descend(max_player, min_player, depth-1, a, b2, true, game_state.update_gameboard(i, min_player), return_time) {
                    Ok(value) => {c = value},
                    Err(s) => {return Err(s)}
                }
                min_move = cmp::min(min_move, c);
                b2 = cmp::min(b2, min_move);
                if a >= b2{
                    break;
                }
            }
            return Ok(min_move)
        }
    }
}