import { Injectable } from '@angular/core';
import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { LoaderService } from './loader.service';


@Injectable({
	providedIn: 'root'
})
export class LoaderInterceptorService implements HttpInterceptor {

	private requests: HttpRequest<any>[] = [];

	constructor(private loaderService: LoaderService) {
	}

	intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

		//push a request to the stack
		this.requests.push(req);
		//show the loader when a http req started
		this.showLoader();

		return next.handle(req).pipe(tap((event: HttpEvent<any>) => {
				if (event instanceof HttpResponse) {
					//success response, pop the request from stack
					this.removeRequest(req);
				}
			},
			(err: any) => {
				//error response, pop the request from stack
				this.removeRequest(req);
			}));
	}

	/**
	 *  hide loader
	 *
	 * @private
	 * @memberof LoaderInterceptorService
	 */
	private onEnd(): void {
		this.hideLoader();
	}

	/**
	 * show loader
	 *
	 * @private
	 * @memberof LoaderInterceptorService
	 */
	private showLoader(): void {
		this.loaderService.show();
	}

	/**
	 * get hide loader instance from loaderservice
	 *
	 * @private
	 * @memberof LoaderInterceptorService
	 */
	private hideLoader(): void {
		this.loaderService.hide();
	}

	/**
	 *  removes request and stops loader when no
	 * requests are left
	 *
	 * @private
	 * @param {HttpRequest<any>} req
	 * @memberof LoaderInterceptorService
	 */
	private removeRequest(req: HttpRequest<any>) {
		const i = this.requests.indexOf(req);
		this.requests.splice(i, 1);
		if (this.requests.length === 0) {
			this.onEnd();
		}
	}
}
