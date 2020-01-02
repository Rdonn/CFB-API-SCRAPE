export class Punting {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
Avg:number;

@Column()
G:number;

@Column()
Punts:number;

@Column()
PuntsG:number;

@Column()
Split:number;

@Column()
Yards:number;

@Column()
YardsG:number;

@OneToOne(type => Player)
player:Player;
}
