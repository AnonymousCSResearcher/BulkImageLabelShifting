import { Injectable } from '@angular/core';
import { AngularFireDatabase, AngularFireList, AngularFireObject } from '@angular/fire/database';
import { AngularFirestore } from '@angular/fire/firestore';
import { AngularFireStorage } from '@angular/fire/storage';
import { FirebaseListObservable, FirebaseObjectObservable } from '@angular/fire/database-deprecated';


// const {Storage} = require('@google-cloud/storage');
// const storage = new Storage();

@Injectable({
	providedIn: 'root'
})
export class AngularfirestorageService {
	private basePath: string = '/image_labeling';
	url$: AngularFireList<any[]>;

	constructor(private db: AngularFireDatabase, public afs: AngularFireStorage) {

	}


}
