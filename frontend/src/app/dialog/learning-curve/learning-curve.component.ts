import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';
import { MlService } from '../../providers/ml/ml.service';


@Component({
	selector: 'app-learning-curve',
	templateUrl: './learning-curve.component.html',
	styleUrls: ['./learning-curve.component.sass']
})
export class LearningCurveComponent implements OnInit {
	public learningCurve: any;
	public completeness: any;
	public accuracy: any;
	public dictionary: string;
	public catName: string;

	constructor(
		public dialogRef: MatDialogRef<LearningCurveComponent>,
		public ml: MlService,
		@Inject(MAT_DIALOG_DATA) public data: any) {
		this.dictionary = this.data.dict;
		this.completeness = this.data.completeness;
		this.accuracy = this.data.accuracy;
		this.catName = this.data.catName;
		this.ml.get_learning_curve(this.catName, this.dictionary).then((data) => this.learningCurve = data)
		console.log(data);
	}

	onNoClick(): void {
		this.dialogRef.close();
	}

	async ngOnInit() {

	}

}
