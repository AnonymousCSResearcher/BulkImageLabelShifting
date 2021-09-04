import { Component, ViewChild } from '@angular/core';

import { AngularFireStorage } from '@angular/fire/storage';
import { HttpService } from '../../providers/http/http.service';
import { UrlString } from '../../models/UrlString';
import { MatSort, MatTableDataSource } from '@angular/material';
import { MlService } from '../../providers/ml/ml.service';
import { Observable } from 'rxjs';


@Component({
	selector: 'app-file-upload',
	templateUrl: './file-upload.component.html',
	styleUrls: ['./file-upload.component.scss']
})

export class FileUploadComponent {

	public fileList: any = [];
	public tempFileList: any;
	public folderName: string;
	@ViewChild(MatSort) sort: MatSort;
	@ViewChild('folderInput') public folderInput;
	public displayedColumns: string[] = ['name', 'type', 'size', 'lastmodified'];
	public uploadProgress: number = 0;
	public showSpinner = false;
	snapshot: Observable<any>;

	constructor(public afs: AngularFireStorage,
	            public http: HttpService,
	            public url: UrlString,
	            public ml: MlService) {
	}

}
