export class Tackles {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
Assisted:number;

@Column()
G:number;

@Column()
Solo:number;

@Column()
Split:number;

@Column()
Total:number;

@Column()
TotalG:number;

@OneToOne(type => Player)
player:Player;
}
