import { Component, HostListener, OnInit, ViewChild } from '@angular/core';
import { MlService } from '../../../providers/ml/ml.service';
import { MatDialog, MatPaginator, MatSelect } from '@angular/material';
import { PathService } from '../../../providers/path/path.service';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { ComponentCanDeactivate } from '../../../guard/can-deactivate.guard';
import { Location } from '@angular/common';
import { UncertainImageComponent } from '../../../dialog/uncertain-image/uncertain-image.component';
import { RenameComponent } from '../../../dialog/rename/rename.component';
import { LearningCurveComponent } from '../../../dialog/learning-curve/learning-curve.component';


@Component({
	selector: 'app-uncertain-folder-image',
	templateUrl: './uncertain-folder-image.component.html',
	styleUrls: ['./uncertain-folder-image.component.scss']
})
export class UncertainFolderImageComponent implements OnInit, ComponentCanDeactivate {
	@HostListener('window:beforeunload')
	canDeactivate(): boolean | Observable<boolean> {
		return confirm('WARNING: You have unsaved changes. Press Cancel to go back and save these changes, or OK to lose these changes.');
	}

	@ViewChild(MatPaginator) paginator: MatPaginator;
	public catName: string;
	public images: any;
	public length = 100;
	public pageSize = 10;
	public pageSizeOptions: number[] = [5, 15, 50, 100];
	public renderedImages: any;
	public pageIndex = 0;
	public folderNames: any;
	public currentFolder: any;
	public dictionary: any;
	public recommendedLabel: any;
	public recommendedCandidates: any[] = [];
	public completeness: any;
	public roundNumber: any;
	public learningCurve: any;
	@ViewChild('matSelect') matSelect: MatSelect;

	constructor(public ml: MlService, public dialog: MatDialog, public path: PathService, private route: ActivatedRoute, public location: Location) {
	}

	ngOnInit() {
		this.route.params.subscribe(
			async (data) => {
				this.catName = data.catName;
				this.dictionary = data.dictionary;
				this.images = this.ml.accuracy;
				await this.getFolderNames();
				this.images = await this.ml.getClassifyDict(this.catName, this.dictionary);
				console.log("uncertain Candidates", this.images);
				this.getCompleteness();
				this.getLearningCurve();
				this.getRoundNumber();
				this.getData({pageIndex: this.pageIndex, pageSize: this.pageSize});
			}
		);
	}

	/**
	 *
	 * @param catName
	 * @param from
	 * @param imageIndex
	 * @param to
	 * @param realIndex
	 * @param fileName
	 * @param dict_name
	 * @param idx
	 * @param rec_label_index
	 */
	async moveImageToFolder(catName, from, imageIndex, to, realIndex, fileName, dict_name, idx, rec_label_index?) {
		await this.ml.incrementClickCounter(this.catName, this.dictionary);
		if (rec_label_index >= 0) {
			this.recommendedCandidates = this.getRecommendedCandidates(from, to, rec_label_index);

			if (this.recommendedCandidates.length > 1) {
				this.evaluateMore();
				this.showUncertainPopUp(this.recommendedCandidates)
			} else {
				let index: any = await this.path.getFileIndex(catName, encodeURI(fileName), from, dict_name);
				this.images = await this.path.moveImageToFolder(catName, from, index.index, to, this.dictionary, imageIndex);
				this.getCompleteness();
				this.getLearningCurve();
				await this.updateCandidate();
				this.getData({pageIndex: this.pageIndex, pageSize: this.pageSize});
				if (this.images.candidates.length == 0) {
					this.goBack();
				}

			}
		} else {
			let index: any = await this.path.getFileIndex(catName, encodeURI(fileName), from, dict_name);
			this.images = await this.path.moveImageToFolder(catName, from, index.index, to, this.dictionary, imageIndex);
			await this.updateCandidate();
			this.getData({pageIndex: this.pageIndex, pageSize: this.pageSize});

			if (this.images.candidates.length == 0) {
				this.goBack();
			}
		}

	}

	getData(obj) {
		this.pageIndex = obj.pageIndex;
		this.pageSize = obj.pageSize;
		let index = 0,
			startingIndex = obj.pageIndex * obj.pageSize,
			endingIndex = startingIndex + obj.pageSize;
		this.renderedImages = this.images.candidates.filter(() => {
			index++;
			return (index > startingIndex && index <= endingIndex);
		});
	}

	async acceptImage(catalogname, index, dict_name) {
		this.images = await this.ml.acceptImageinDict(catalogname, index, dict_name);
		await this.updateCandidate();
		this.getData({pageIndex: this.pageIndex, pageSize: this.pageSize});
		if (this.images.candidates.length == 0) {
			this.goBack();
		}
	}

	async getFolderNames() {
		this.folderNames = await this.path.getFolderNamesOfDict(this.catName, this.path.currentTimeStamp, this.dictionary);
	}

	async updateCandidate() {
		this.images = await this.ml.getClassifyDict(this.catName, this.dictionary).catch(
			(err) => {
				console.log(err);
			});
	}

	goBack() {
		this.location.back();
	}

	getRecommendedCandidates(curr_lab, recommended_label, recommended_label_index) {
		let recommendedCandidates = null;
		this.recommendedLabel = recommended_label;
		if (this.images.candidates.length) {
			recommendedCandidates = this.images.candidates.filter(
				candidates => candidates.curr_lab == curr_lab &&
					candidates.pred_labs[recommended_label_index] == recommended_label);
			recommendedCandidates.forEach((res) => {
				res.index = this.images.candidates.indexOf(res)

			});
			console.log("recommendedCandidates", recommendedCandidates);
		}
		return recommendedCandidates;
	}

	showUncertainPopUp(candidates: any) {
		const dialogRef = this.dialog.open(UncertainImageComponent, {
			minWidth: '80%',
			maxWidth: '90%',
			maxHeight: '90%',
			minHeight: '80%',
			data: {
				candidates: candidates,
				catName: this.catName,
				dictionary: this.dictionary,
				recommendedLabel: this.recommendedLabel,
				currentLabel: candidates[0].curr_lab

			}
		});

		dialogRef.afterClosed().subscribe(async () => {
			await this.updateCandidate();
			this.getCompleteness();
			this.getLearningCurve();
			this.getData({pageIndex: this.pageIndex, pageSize: this.pageSize});

		});
	}

	showDialogLearningCurve() {
		this.dialog.open(LearningCurveComponent, {
			data: {
				accuracy: this.ml.accuracy.accuracy,
				completeness: this.completeness,
				catName: this.catName,
				dict: this.dictionary
			}
		});

	}

	async getCompleteness() {
		this.completeness = await this.ml.getCompleteness(this.catName, this.dictionary);
		console.log('completeness', this.completeness);
	}

	async evaluateMore() {
		await this.path.evaluateMoreMove(this.catName, this.dictionary, this.recommendedLabel, this.recommendedCandidates)
	}

	async getRoundNumber() {
		this.roundNumber = await this.ml.getRoundNumber(this.catName, this.dictionary)
	}

	async getLearningCurve() {
		this.learningCurve = await this.ml.get_learning_curve(this.catName, this.dictionary)
	}

}


