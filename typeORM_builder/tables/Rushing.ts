export class Rushing {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
Att:number;

@Column()
AttG:number;

@Column()
Avg:number;

@Column()
G:number;

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
