import { Injectable } from '@angular/core';


@Injectable()
export class UrlString {

	// private BaseUrl = 'http://127.0.0.1:5000/';
	// private BaseUrl = 'http://34.65.64.121/';
	private BaseUrl = 'https://ml-il.bmtg.app/';

	constructor() {
	}

	public getBaseUrl(): string {
		return this.BaseUrl;
	}
}
