import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';


@Component({
	selector: 'app-confirm',
	templateUrl: './confirm.component.html',
	styleUrls: ['./confirm.component.sass']
})
export class ConfirmComponent implements OnInit {
	public folderName = '';

	constructor(
		public dialogRef: MatDialogRef<ConfirmComponent>,
		@Inject(MAT_DIALOG_DATA) public data: any) {
		console.log(data);
	}

	onNoClick(): void {
		this.dialogRef.close();
	}

	ngOnInit(): void {
	}

}
