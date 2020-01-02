export class MiscDefense {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
FumblesForced:number;

@Column()
G:number;

@Column()
KicksPuntsBlocked:number;

@Column()
PassesBrokenUp:number;

@Column()
QBHurries:number;

@Column()
Split:number;

@OneToOne(type => Player)
player:Player;
}
