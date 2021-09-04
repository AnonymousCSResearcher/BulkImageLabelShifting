import { Injectable } from '@angular/core';
import { HttpService } from '../http/http.service';
import { UrlString } from '../../models/UrlString';


@Injectable({
	providedIn: 'root'
})
export class MlService {
	public accuracy: any;
	public round: any;

	constructor(public http: HttpService, public url: UrlString) {
	}

	public getFeatureVector(path: string): Promise<any> {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'getfeaturevector';
			this.http.post(url, {path: path}).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})

	}

	public classify(catalogName: string, dict_name: string) {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'classify/' + catalogName + '/uncertainty/' + dict_name;
			this.http.get(url).subscribe(
				(data: any) => {
					this.accuracy = data;
					this.round++;
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})
	}

	public getClassifyDict(catalogName: string, dict_name: string) {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'get_classification/' + catalogName + '/' + dict_name;
			this.http.get(url).subscribe(
				(data: any) => {
					this.accuracy = data;
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})
	}

	public acceptImageinDict(catalogName: string, index: string, dict_name: string) {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'acceptImage/' + catalogName + '/' + index + '/' + dict_name;
			this.http.get(url).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})
	}

	public getCompleteness(catalogName: string, dict_name: string) {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'get_completeness/' + catalogName + '/' + dict_name;
			this.http.get(url).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})
	}

	public getRoundNumber(catalogName: string, dict_name: string) {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'get_round_number/' + catalogName + '/' + dict_name;
			this.http.get(url).subscribe(
				(data: any) => {
					this.round = data.round_number;
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})
	}

	public incrementClickCounter(catalogName: string, dict_name: string) {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'increment_click_counter/' + catalogName + '/' + dict_name;
			this.http.get(url).subscribe(
				(data: any) => {
					console.warn(data.success);
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})
	}

	public get_learning_curve(catalogName: string, dict_name: string) {
		return new Promise((resolve, reject) => {
			let url = this.url.getBaseUrl() + 'generate_plot/' + catalogName + '/' + dict_name;
			this.http.get(url).subscribe(
				(data: any) => {
					resolve(data);
				},
				(err) => {
					reject(err);
				})
		})
	}
}


