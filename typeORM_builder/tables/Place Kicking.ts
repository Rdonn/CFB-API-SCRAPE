export class PlaceKicking {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
:number;

@Column()
Att:number;

@Column()
AttG:number;

@Column()
ExtraPoint:number;

@Column()
FieldGoal:number;

@Column()
G:number;

@Column()
Made:number;

@Column()
MadeG:number;

@Column()
Pct:number;

@Column()
Split:number;

@OneToOne(type => Player)
player:Player;
}
