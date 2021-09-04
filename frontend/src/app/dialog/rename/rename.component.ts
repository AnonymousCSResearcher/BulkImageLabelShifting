import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';


@Component({
	selector: 'app-rename',
	templateUrl: './rename.component.html',
	styleUrls: ['./rename.component.sass']
})
export class RenameComponent {
	public newFolderName = '';

	constructor(
		public dialogRef: MatDialogRef<RenameComponent>,
		@Inject(MAT_DIALOG_DATA) public data: any) {
		console.log(data);
	}

	onNoClick(): void {
		this.dialogRef.close(this.newFolderName);
	}

}
