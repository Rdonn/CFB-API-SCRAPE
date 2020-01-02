export class PuntReturn {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
Avg:number;

@Column()
G:number;

@Column()
Ret:number;

@Column()
RetG:number;

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
