export class Kickoffs {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
Avg:number;

@Column()
G:number;

@Column()
Kickoffs:number;

@Column()
Onside:number;

@Column()
OutOfBounds:number;

@Column()
Split:number;

@Column()
Touchback:number;

@Column()
Touchback:number;

@Column()
Yards:number;

@OneToOne(type => Player)
player:Player;
}
