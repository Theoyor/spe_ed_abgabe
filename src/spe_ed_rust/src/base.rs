//!Deadline Global

pub mod base{
    use std::cmp;
    use std::usize;
    use rand::Rng;
    
    //use std::fmt;
    //use heapless::Vec;
    //use heapless::consts::U24;
    
    pub fn sub_lim(a:usize, b:usize) -> usize{
        if a>b{
            return a-b;
        }
        return 0;
    }



    #[derive(Clone, Copy)]
    pub struct Player{
        pub id : usize,
        pub x : usize,
        pub y : usize,
        pub direction : i8,   //up = 0, right = 1, down = 2, left = 3
        pub speed : usize,
        pub active : bool
    }

    #[derive(Clone)]
    pub struct  State{
        pub rows :  Vec<i128>,
        pub cols :  Vec<i128>,
        pub turn : i8,
        pub max_player : usize,
        pub players : [Player;6],
        pub width : usize,
        pub height : usize,
    }


    impl State {

        pub fn spielstands_bewertung(&self, max_player:usize, min_player:usize)->i16 {
            let e = self.nearbyFields(min_player)-self.nearbyFields(max_player);
            return e;
        }

        pub fn nearbyFields(&self, id:usize)->i16 {
            let width = self.width as i8;
            let heigth = self.height as i8;
            let rows = &self.rows;
            let x = self.players[id-1].x as i8;
            let y = self.players[id-1].y as i8;
            let r = 10;
            let mut counter = 0;
            let mut mask = 0;
             if x+r < width {
                mask = (1 << (2 * r + 1)) - 1;
            }else{
                mask = (1 << (width-(x-r))) - 1;
             }
            if y-r < 0{
                counter += (-y+r)*(1+r+r);
            }
            if y+r >= heigth{
                counter += (y+r+1-heigth)*(1+r+r);
            }
            let shift = cmp::max(0,width-(x+r+1));
            let p = cmp::min(heigth,y+r+r) as usize;
            let t = cmp::max(y-r,0) as usize;
            for i in t..p{
                if (x-r) < 0 {
                        counter += x-r;
                }
                if (x+r)>= width{
                    counter += (x+r+1-heigth);
                }
                counter += (((rows[i] >> shift  & mask)as i128).count_ones() as i8);
            }
            return counter as i16;
        }

        pub fn update_gameboard(&self, mov: i8, id: usize) -> State {
            //return self.clone();
            //mov: change_nothing = 0, speed_up = 1, slow down = 2, turn_right = 3, turn_left = 4
            let mut direction = self.players[id - 1].direction;
            let mut speed = self.players[id - 1].speed;
            let mut x = self.players[id - 1].x;
            let mut y = self.players[id - 1].y;
            let mut active = self.players[id - 1].active;
            let mut cols = self.cols.to_vec();
            let mut rows = self.rows.to_vec();

            if (direction == 3 && mov == 3) || (direction == 1 && mov == 4) {
                direction = 0;
            } else if (direction == 1 && mov == 3) || (direction == 3 && mov == 4) {
                direction = 2;
            } else if (direction == 2 && mov == 3) || (direction == 0 && mov == 4) {
                direction = 3;
            } else if (direction == 0 && mov == 3) || (direction == 2 && mov == 4) {
                direction = 1;
            } else if mov == 1 {
                if speed == 10 {
                    active = false;
                }
                speed = speed + 1;
            } else if mov == 2 {
                if speed == 1 {
                    active = false;
                }
                speed = sub_lim(speed, 1);
            }

            if (direction == 0&&y<speed)||(direction == 1&&x+speed>=self.width)||(direction==2&&y+speed>=self.height)||(direction==3&&x<speed){
                active = false;
            }else if self.turn % 12 != 0 {

                if direction == 0 {
                    let wanted_col = &mut cols[x];
                 //   if (y as i16) - (speed as i16) < 0 {
                  //      active = false;
                   // }
                    for i in (y-speed)..y {
                        if *wanted_col >> i & 1 == 0 {
                            *wanted_col |= 2 ^ i as i128;
                            rows[i] |= 2 ^ x as i128;
                        } else {
                            active = false;
                        }
                    }
                    y -= speed;

                } else if direction == 1 {
                    let wanted_row = &mut rows[y];
                   // if x + 1 + speed > self.width {
                    //    active = false;
                    //}
                    for i in (x + 1)..(x + 1 + speed) {
                        if *wanted_row >> i & 1 == 0 {
                            *wanted_row |= 2 ^ i as i128;
                            cols[i] |= 2 ^ y as i128;
                        } else {
                            active = false;
                        }
                    }
                    x += speed;

                } else if direction == 2 {
                    let wanted_col = &mut cols[x];

                 //   if y + 1 + speed > self.height {
                  //      active = false;
                   // }
                    for i in (y + 1)..(y + 1 + speed) {
                        if *wanted_col >> i & 1 == 0 {
                            *wanted_col |= 2 ^ i as i128;
                            rows[i] |= 2 ^ x as i128;
                        } else {
                            active = false;
                        }
                    }
                    y += speed;
                } else if direction == 3 {//offset von 1 nicht vergessen
                    let wanted_row = &mut rows[y];
                   // if( x as i16) - (speed as i16) < 0 {
                     //   active = false;
                   // }else{
                    for i in (x-speed)..x {
                        if *wanted_row >> i & 1 == 0 {
                            *wanted_row |= 2 ^ i as i128;
                            cols[i] |= 2 ^ y as i128;
                        } else {
                            active = false;
                        }
                    }
                    //}
                    x -= speed;
                    
                }
            } else {
                let mut f1 = (0, 0);
                let mut f2 = (0, 0);

                if direction == 0 {
                    f1 = (x, y - 1);
                    f2 = (x, y - speed);
                    y -= speed;
                } else if direction == 1 {
                    f1 = (x + 1, y);
                    f2 = (x + speed, y);
                    x += speed;
                } else if direction == 2 {
                    f1 = (x, y + 1);
                    f2 = (x, y + speed);
                    y += speed;
                } else if direction == 3 {
                    f1 = (x - 1, y);
                    f2 = (x - speed, y);
                    x -= speed;
                }

                if f1 != f2 {
                    if rows[f1.1] >> f1.0 & 1 == 0 {
                        rows[f1.1] |= 2 ^ f1.0 as i128;
                        cols[f1.0] |= 2 ^ f1.1 as i128;
                    } else {
                        active = false
                    }
                }
                if rows[f2.1] >> f2.0 & 1 == 0 {
                    rows[f2.1] |= 2 ^ f2.0 as i128;
                    cols[f2.0] |= 2 ^ f2.1 as i128;
                } else {
                    active = false
                }
            }


            let p_new = Player {
                id: id,
                x: x,
                y: y,
                direction: direction,   //up = 0, right = 1, down = 2, left = 3
                speed: speed,
                active: active,
            };

            let mut arr = self.players;
            arr[id-1] = p_new;

            State {
                rows: rows,
                cols: cols,
                turn: self.turn+1,
                max_player: self.max_player,
                players: arr,
                width: self.width,
                height: self.height
            }
        }
    }

}