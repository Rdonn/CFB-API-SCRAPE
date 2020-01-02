export class TotalOffense {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
G:number;

@Column()
PassYards:number;

@Column()
Plays:number;

@Column()
RushYards:number;

@Column()
Split:number;

@Column()
TotalYards:number;

@Column()
YardsG:number;

@Column()
YardsPlay:number;

@OneToOne(type => Player)
player:Player;
}
