import { Component, OnInit } from '@angular/core';
import { HttpService } from './providers/http/http.service';
import { UrlString } from './models/UrlString';
import { Router } from '@angular/router';


@Component({
	selector: 'app-root',
	templateUrl: './app.component.html',
	styleUrls: ['./app.component.scss'],
	providers: [HttpService, UrlString]
})
export class AppComponent implements OnInit {

	constructor(private router: Router) {

	}

	ngOnInit(): void {
		this.router.navigate(['']);
	}
}
