import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef, MatSelect } from '@angular/material';
import { PathService } from '../../providers/path/path.service';
import { MlService } from '../../providers/ml/ml.service';
import { NgxUiLoaderService } from 'ngx-ui-loader';


@Component({
	selector: 'app-uncertain-image',
	templateUrl: './uncertain-image.component.html',
	styleUrls: ['./uncertain-image.component.scss']
})
export class UncertainImageComponent implements OnInit {

	public renderedImages: any;
	public actualLabel: any[] = [];
	public catName: string;
	public dictionary: string;
	public folderNames: any;
	public recommendedLabel: string;
	public currentLabel: string;
	public images: any;

	constructor(
		public dialogRef: MatDialogRef<UncertainImageComponent>,
		@Inject(MAT_DIALOG_DATA) public data: any, public path: PathService, public ml: MlService, private ngxService: NgxUiLoaderService) {
		console.log(this.data);
		this.renderedImages = data.candidates;
		this.catName = data.catName;
		this.dictionary = data.dictionary;
		this.recommendedLabel = data.recommendedLabel;
		this.currentLabel = data.currentLabel;
		this.getFolderNames();

	}

	ngOnInit() {
	}

	onNoClick(increment_counter: boolean): void {
		if (increment_counter) {
			this.ml.incrementClickCounter(this.catName, this.dictionary);
		}

		this.dialogRef.close();
	}


	async getFolderNames() {
		this.folderNames = await this.path.getFolderNamesOfDict(this.catName, this.path.currentTimeStamp, this.dictionary);
	}


	async moveAllImagesofFolder() {
		this.ngxService.start();
		for (let i = 0; i < this.renderedImages.length; i++) {
			let index: any = await this.path.getFileIndex(this.catName, encodeURI(this.renderedImages[i].file), this.currentLabel, this.dictionary);
			await this.path.moveImageToFolder(this.catName, this.currentLabel, index.index, this.recommendedLabel, this.dictionary, this.renderedImages[i].idx);
			console.log("image moved");
		}
		await this.ml.incrementClickCounter(this.catName, this.dictionary);
		this.ngxService.stop();
		this.onNoClick(false);
	}

	async moveImageToFolder(catName, from, imageIndex, to, realIndex, fileName, dict_name) {
		await this.ml.incrementClickCounter(this.catName, this.dictionary);
		let index: any = await this.path.getFileIndex(catName, encodeURI(fileName), from, dict_name);
		await this.path.moveImageToFolder(catName, from, index.index, to, this.dictionary, imageIndex);
		this.renderedImages.splice(realIndex, 1);
		if (this.renderedImages.length == 0) {
			this.onNoClick(false)
		}
	}


}
