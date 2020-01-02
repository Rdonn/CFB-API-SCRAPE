export class Interceptions {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
G:number;

@Column()
Int:number;

@Column()
IntG:number;

@Column()
Split:number;

@Column()
TD:number;

@Column()
Yards:number;

@OneToOne(type => Player)
player:Player;
}
