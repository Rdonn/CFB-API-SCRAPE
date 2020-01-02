export class FumbleReturns {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
FumRet:number;

@Column()
G:number;

@Column()
Split:number;

@Column()
TD:number;

@Column()
Yards:number;

@OneToOne(type => Player)
player:Player;
}
