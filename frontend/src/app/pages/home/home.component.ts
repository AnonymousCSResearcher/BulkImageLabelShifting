import { Component, OnInit } from '@angular/core';
import { PathService } from '../../providers/path/path.service';
import 'hammerjs';
import { Router } from '@angular/router';


@Component({
	selector: 'app-home',
	templateUrl: './home.component.html',
	styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
	public catalogObj: any;
	public folder: string;
	public dictionary: any;
	public dictionaryName: any;
	public catalogname: any;
	public timeStamps: any;

	constructor(public path: PathService,
	            private router: Router) {
	}

	async ngOnInit() {
		this.getFolder();

	}

	async getFolder() {
		this.catalogObj = await this.path.getFilePath();
		console.log(this.catalogObj);
	}


	async navigateToFolder(catName: string, tmp_dict: string, cache_dict: string) {
		this.path.currentTimeStamp = tmp_dict;
		let folderNames = await this.path.getFolderNamesOfDict(catName, tmp_dict, cache_dict);
		this.path.loadDictVers(catName, tmp_dict, cache_dict);
		this.router.navigate(['folder-image', catName, folderNames.folderNames[0], cache_dict]);
	}

	async getAllSortDict(catalogName) {
		this.catalogname = catalogName;
		this.dictionary = await this.path.getAllSortDict(catalogName);
	}

	async getTimeStamp(catalogName, dict_name) {
		this.dictionaryName = dict_name;
		this.timeStamps = await this.path.getTimeStamp(catalogName, dict_name);
		if (this.timeStamps.timeStamp.length == 0) {
			await this.path.saveDict(catalogName, dict_name, 0);
			this.timeStamps = await this.path.getTimeStamp(catalogName, dict_name);
		}
	}


}
