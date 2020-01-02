export class Sacks {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
G:number;

@Column()
SackYards:number;

@Column()
Sacks:number;

@Column()
SacksG:number;

@Column()
Split:number;

@OneToOne(type => Player)
player:Player;
}
