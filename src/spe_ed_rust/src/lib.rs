

// crate::action::action::start as strt;
use std::time::{SystemTime};
mod base;   
use base::base::{Player, State};
mod action;
use action::action as act;
use num_cpus;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use json::parse;




/// Formats the sum of two numbers as string.
#[pyfunction]
fn accept( rows: Vec<i128>, cols: Vec<i128>, turn: i8, max_player:usize, players:String, width: usize, height: usize) -> PyResult<i8> {
    let parsed =  parse(&players).unwrap();
    let pl = Player{
        id : 6,
        x : 0,
        y : 0,
        direction: 0,
        speed: 0,
        active: false

    }; 

    
    let mut pls = [pl;6];

            
        let mut p = Player{
            id : 1,
            x: parsed["1"]["x"].as_usize().unwrap(),
            y: parsed["1"]["y"].as_usize().unwrap(),
            direction : parsed["1"]["direction"].as_i8().unwrap(),
            speed : parsed["1"]["speed"].as_usize().unwrap(),
            active: parsed["1"]["active"].as_bool().unwrap(),

        };
        pls[0] = p;
        
        p = Player{
            id : 2,
            x: parsed["2"]["x"].as_usize().unwrap(),
            y: parsed["2"]["y"].as_usize().unwrap(),
            direction : parsed["2"]["direction"].as_i8().unwrap(),
            speed : parsed["2"]["speed"].as_usize().unwrap(),
            active: parsed["2"]["active"].as_bool().unwrap(),

        };
        pls[1] = p;
        
         p = Player{
            id : 3,
            x: parsed["3"]["x"].as_usize().unwrap(),
            y: parsed["3"]["y"].as_usize().unwrap(),
            direction : parsed["3"]["direction"].as_i8().unwrap(),
            speed : parsed["3"]["speed"].as_usize().unwrap(),
            active: parsed["3"]["active"].as_bool().unwrap(),

        };
        pls[2]= p;
        
        p = Player{
            id : 4,
            x: parsed["4"]["x"].as_usize().unwrap(),
            y: parsed["4"]["y"].as_usize().unwrap(),
            direction : parsed["4"]["direction"].as_i8().unwrap(),
            speed : parsed["4"]["speed"].as_usize().unwrap(),
            active: parsed["4"]["active"].as_bool().unwrap(),

        };
        pls[3]=p;
        
        p = Player{
            id : 5,
            x: parsed["5"]["x"].as_usize().unwrap(),
            y: parsed["5"]["y"].as_usize().unwrap(),
            direction : parsed["5"]["direction"].as_i8().unwrap(),
            speed : parsed["5"]["speed"].as_usize().unwrap(),
            active: parsed["5"]["active"].as_bool().unwrap(),

        };
        pls[4]= p;
        
        p = Player{
            id : 6,
            x: parsed["6"]["x"].as_usize().unwrap(),
            y: parsed["6"]["y"].as_usize().unwrap(),
            direction : parsed["6"]["direction"].as_i8().unwrap(),
            speed : parsed["6"]["speed"].as_usize().unwrap(),
            active: parsed["6"]["active"].as_bool().unwrap(),

        };
        pls[5]= p;
           
    let game_state = State{
        rows,
        cols,
        turn,
        max_player,
        players : pls,
        width,
        height
    };
     
    //return time richtig setzen
    Ok(act::iter_depth(max_player, game_state, 1))
    
    
}

/// A Python module implemented in Rust.
#[pymodule]
fn spe_ed_lib(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(accept, m)?)?;

    Ok(())
}




 
pub fn main() {
    let cpus = num_cpus::get();
    print!("CPUs: {} \n",cpus);
}
