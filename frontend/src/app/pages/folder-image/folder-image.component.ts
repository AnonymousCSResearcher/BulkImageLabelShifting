import { Component, HostListener, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { PathService } from '../../providers/path/path.service';
import { MlService } from '../../providers/ml/ml.service';
import { MatPaginator, MatSnackBar } from '@angular/material';
import { MatDialog } from '@angular/material';
import { RenameComponent } from '../../dialog/rename/rename.component';
import { LoaderService } from '../../providers/loader/loader.service';
import { ConfirmComponent } from '../../dialog/confirm/confirm.component';
import { InfoComponent } from '../../snackbar/info/info.component';
import { ComponentCanDeactivate } from '../../guard/can-deactivate.guard';
import { Observable } from 'rxjs';
import { NgxUiLoaderService } from 'ngx-ui-loader';


@Component({
	selector: 'app-folder-image',
	templateUrl: './folder-image.component.html',
	styleUrls: ['./folder-image.component.scss']
})
export class FolderImageComponent implements OnInit, ComponentCanDeactivate, OnDestroy {

	@HostListener('window:beforeunload')
	canDeactivate(): boolean | Observable<boolean> {
		return false;
	}


	@ViewChild(MatPaginator) paginator: MatPaginator;
	public catName: string;
	public images: any;
	public length = 100;
	public pageSize = 10;
	public pageSizeOptions: number[] = [5, 10, 25, 100];
	public renderedImages: any;
	public pageIndex = 0;
	public folderNames: any;
	public currentFolder: any;
	public accuracy: any;
	public newFolderName = '';
	public dictionary: any;
	public completeness: any;
	public classification: any;
	public roundNumber: any;

	public constructor(private route: ActivatedRoute,
	                   public path: PathService,
	                   public ml: MlService,
	                   public dialog: MatDialog,
	                   public router: Router,
	                   public loader: LoaderService,
	                   public snack: MatSnackBar,
	                   private ngxService: NgxUiLoaderService) {

	}

	ngOnInit() {

		this.route.params.subscribe(async (params) => {
				this.pageIndex = 0;
				console.log(params);
				this.catName = params.catName;
				this.dictionary = params.dictionary;
				this.currentFolder = params.folder;
				await this.getImagesOfFolder(params.catName, params.folder, params.dictionary);
				this.getUnsortedImages(this.catName);
				await this.getFolderNames();
				this.getCompleteness(false);
				this.getRoundNumber();
				this.getData({pageIndex: this.pageIndex, pageSize: this.pageSize});
				this.classification = await this.ml.getClassifyDict(this.catName, this.dictionary);


			}
		);
	}

	async getFolderNames() {
		this.folderNames = await this.path.getFolderNames(this.catName, this.dictionary);
		console.log(this.folderNames);
	}

	async getUnsortedImages(catalogName: string) {
		let i = await this.path.getUnsortedImages(catalogName);
		console.log(i);
	}

	async getImagesOfFolder(catalog_name, folder, dict_name) {
		this.images = await this.path.getImages(catalog_name, folder, dict_name);
	}

	getData(obj) {
		this.pageIndex = obj.pageIndex;
		this.pageSize = obj.pageSize;
		let index = 0,
			startingIndex = obj.pageIndex * obj.pageSize,
			endingIndex = startingIndex + obj.pageSize;

		this.renderedImages = this.images.data.filter(() => {
			index++;
			return (index > startingIndex && index <= endingIndex);
		});
	}

	isActive(folder) {
		this.currentFolder = folder;
	}

	async moveImageToFolder(catName, from, to, imageIndex) {
		await this.path.moveImageToFolder(catName, from, imageIndex, to, this.dictionary);
		await this.getImagesOfFolder(catName, this.currentFolder, this.dictionary).then(
			() => this.getData({pageIndex: this.pageIndex, pageSize: this.pageSize}));
	}

	edit(folderName) {
		const dialogRef = this.dialog.open(RenameComponent, {
			width: '270px',
			data: {currentFolderName: folderName}
		});

		dialogRef.afterClosed().subscribe(newFolderName => {
			console.log(newFolderName);
			if (newFolderName) {
				this.rename(folderName, newFolderName);
			}
		});
	}

	delete(folderName) {
		const dialogRef = this.dialog.open(ConfirmComponent, {
			width: '270px',
			data: {currentFolderName: folderName}
		});

		dialogRef.afterClosed().subscribe(async data => {
			if (data) {
				this.path.deleteFolder(this.catName, folderName, this.dictionary).then(
					() => {
						this.getFolderNames();
					}).catch(
					(err) => {
						console.log(err);
						this.openSnackBar(err.error)
					}
				);
			}

		});
	}

	rename(old_folder_name, new_folder_name) {
		this.path.renameFolder(this.catName, old_folder_name, new_folder_name, this.dictionary).then(
			(data) => {
				this.getFolderNames().then(
					() => {
						if (old_folder_name == this.currentFolder) {
							this.router.navigate(['folder-image', this.catName, new_folder_name, this.dictionary]);
						}
						console.log(data);
					});
			}
		).catch(
			(err) => {
				console.log(err);
			}
		)
	}

	async classify() {
		this.ngxService.start();
		this.accuracy = await this.ml.classify(this.catName, this.dictionary);
		this.getRoundNumber();
		this.getCompleteness(false);
		console.log(this.accuracy);
		this.ngxService.stop();
	}

	async saveDict() {
		let res = await this.path.saveDict(this.catName, this.dictionary, this.ml.round);
		this.openSnackBar(res.success);
		console.log(res);
	}

	async createNewFolder() {
		console.log(this.dictionary);
		if (this.newFolderName.trim() !== '') {
			await this.path.createNewFolder(this.catName, this.newFolderName, this.dictionary);
			await this.getFolderNames();
			this.newFolderName = '';
		}
	}

	navigateToUnceratin() {
		this.router.navigate(['folder-image-uncertain', this.catName, this.dictionary]);
	}


	openSnackBar(message) {
		this.snack.openFromComponent(InfoComponent, {
			duration: 3 * 1000,
			data: message
		});
	}


	async ngOnDestroy() {
		if (confirm("You have unsaved changes. Do you want to save before leave?")) {
			await this.saveDict();
		}
	}

	async getCompleteness(update_learning_curve) {
		if (update_learning_curve) {
			this.completeness = await this.ml.getCompleteness(this.catName, this.dictionary);
		} else {
			this.completeness = await this.ml.getCompleteness(this.catName, this.dictionary);
		}

		console.log('completeness', this.completeness);
	}

	async getRoundNumber() {
		this.roundNumber = await this.ml.getRoundNumber(this.catName, this.dictionary);
		console.log('round_number', this.roundNumber)
	}

}

