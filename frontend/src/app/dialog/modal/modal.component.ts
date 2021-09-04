import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';


@Component({
	selector: 'app-modal',
	templateUrl: './modal.component.html',
	styleUrls: ['./modal.component.sass']
})
export class ModalComponent implements OnInit {


	constructor(
		public dialogRef: MatDialogRef<ModalComponent>,
		@Inject(MAT_DIALOG_DATA) public data: any) {
		console.log(data);
	}

	onNoClick(): void {
		this.dialogRef.close(false);
	}

	ngOnInit(): void {
	}

}
