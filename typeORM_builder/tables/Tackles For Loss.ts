export class TacklesForLoss {

@PrimaryColumn()
playerid:number;

@PrimaryColumn()
yearplayed:number;

@Column()
G:number;

@Column()
Split:number;

@Column()
TFL:number;

@Column()
TFLYards:number;

@Column()
TFLG:number;

@OneToOne(type => Player)
player:Player;
}
