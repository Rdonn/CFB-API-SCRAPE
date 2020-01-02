export class Scoring {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
XP:number;

@Column()
XP:number;

@Column()
FG:number;

@Column()
G:number;

@Column()
Points:number;

@Column()
PointsG:number;

@Column()
Safety:number;

@Column()
Split:number;

@Column()
TD:number;

@OneToOne(type => Player)
player:Player;
}
