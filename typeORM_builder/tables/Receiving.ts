export class Receiving {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
Avg:number;

@Column()
G:number;

@Column()
Rec:number;

@Column()
RecG:number;

@Column()
Split:number;

@Column()
TD:number;

@Column()
Yards:number;

@Column()
YardsG:number;

@OneToOne(type => Player)
player:Player;
}
