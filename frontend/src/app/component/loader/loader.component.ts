import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { LoaderService } from '../../providers/loader/loader.service';
import { LoaderState } from '../../providers/loader/loader';


@Component({
	selector: 'app-loader',
	templateUrl: './loader.component.html',
	styleUrls: ['./loader.component.sass']
})
export class LoaderComponent implements OnInit, OnDestroy {

	public show: boolean = false;
	private subscription: Subscription;

	constructor(private loaderService: LoaderService) {
	}

	ngOnInit() {
		this.subscription = this.loaderService.loaderState.subscribe((state: LoaderState) => {
			this.show = state.show
		})

	}

	ngOnDestroy(): void {
		this.subscription.unsubscribe();
	}

}
