import { Injectable } from '@angular/core';
import { HttpService } from '../http/http.service';
import { UrlString } from '../../models/UrlString';


@Injectable({
	providedIn: 'root'
})
export class PathService {
	public filePath: any;
	public images: any;
	public dictionary: any;
	public timeStamps: any;
	public currentTimeStamp: any;

	constructor(public http: HttpService, public url: UrlString) {

	}

	public getImages(catalogname, folder, dict_name): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'get_folder_images/' + catalogname + '/' + folder + '/' + dict_name;
			this.http.get(url).subscribe(
				(data: any) => {
					this.images = data;
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})

	}

	public getFilePath(): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'getpaths';
			this.http.get(url).subscribe(
				(data: any) => {
					this.filePath = data;
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})

	}

	public getFolderNamesOfDict(catalogname, version_dict, cache_dict): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'getfoldernamesOfDict/' + catalogname + '/' + version_dict + '/' + cache_dict;
			this.http.get(url).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})
	}

	public getFolderNames(catalogname, dict_name): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'get_folder_names/' + catalogname + '/' + dict_name;
			this.http.get(url).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})
	}

	public getUnsortedImages(catalogname): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'getUnsortedImages/' + catalogname;
			this.http.get(url).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})
	}

	public renameFolder(catalogname, old_folder_name, new_folder_name, dict_name): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'rename_folder/' + catalogname + '/' + old_folder_name + '/' + new_folder_name + '/' + dict_name;
			this.http.get(url).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})

	}

	public createNewFolder(catalogname, folderName, dictname): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'createFolder/' + catalogname + '/' + folderName + '/' + dictname;
			this.http.get(url).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})

	}

	public deleteFolder(catalogname, folderName, dictname): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'deleteFolder/' + catalogname + '/' + folderName + '/' + dictname;
			this.http.get(url).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})

	}

	public moveImageToFolder(catalogname, source_folder, source_file, destination_folder, dict_name, classIndex?) {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'shiftImage/' + catalogname + '/' + source_folder + '/' + source_file + '/' + destination_folder + '/' + dict_name  + '/' + classIndex;
			this.http.get(url).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})
	}

	public getFileIndex(catalogname, source_file, folder, dict_name) {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'getFileIndex/' + catalogname + '/' + source_file + '/' + folder + '/' + dict_name;
			this.http.get(url).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})
	}


	public saveDict(catalogname: string, dictname: string, round: any): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'save_dict/' + catalogname + '/' + dictname + '/' + round;
			this.http.get(url).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})

	}

	public getAllSortDict(catalogname): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'get_all_sortdict/' + catalogname;
			this.http.get(url).subscribe(
				(data: any) => {
					this.dictionary = data;
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})
	}

	public getTimeStamp(catalogname, cache_dict): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'getTimeStamp/' + catalogname + '/' + cache_dict;
			this.http.get(url).subscribe(
				(data: any) => {
					this.timeStamps = data;
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})

	}

	public loadDictVers(catalogname: string, tmp_dict: string, cache_dict: string): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'loadDictVers/' + catalogname + '/' + tmp_dict + '/' + cache_dict;
			this.http.get(url).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})

	}

	public getManualLabel(catalogname: string, filename: string): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'getManualLabel/' + catalogname + '/' + encodeURI(filename);
			this.http.get(url).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		});
	}


	public evaluateMoreMove(catalogname: string, dict_name: string, destination_folder_key: string, more_images_list: any): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'evaluate_more_move';
			let body = {
				'catalogName': catalogname,
				'dict_name': dict_name,
				'destination_folder_key': destination_folder_key,
				'more_images_list': more_images_list
			};
			this.http.post(url, body).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		});
	}

}
