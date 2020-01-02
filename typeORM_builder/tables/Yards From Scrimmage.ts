export class YardsFromScrimmage {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
G:number;

@Column()
Plays:number;

@Column()
RecvYards:number;

@Column()
RushYards:number;

@Column()
Split:number;

@Column()
TD:number;

@Column()
TotalYards:number;

@Column()
YardsG:number;

@Column()
YardsPlay:number;

@OneToOne(type => Player)
player:Player;
}
