export class AllPurposeRunning {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
G:number;

@Column()
IntRet:number;

@Column()
KickRet:number;

@Column()
Plays:number;

@Column()
PuntRet:number;

@Column()
Recv:number;

@Column()
Rush:number;

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
