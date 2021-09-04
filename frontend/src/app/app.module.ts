import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PageNotFoundComponent } from './pages/page-not-found/page-not-found.component';
import { HomeComponent } from './pages/home/home.component';
import { FolderComponent } from './component/folder/folder.component';
import { FolderImageComponent } from './pages/folder-image/folder-image.component';

//AngularFireStorage
import { StorageBucket } from '@angular/fire/storage';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { PathService } from './providers/path/path.service';
import { UrlString } from './models/UrlString';
import { MlService } from './providers/ml/ml.service';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppNavComponent } from './component/nav/app-nav.component';


import { MaterialModule } from './material.module';
import { LoaderInterceptorService } from './providers/loader/loader-interceptor.service';
import { LoaderComponent } from './component/loader/loader.component';
import {
	MAT_DIALOG_DEFAULT_OPTIONS,
	MatInputModule

} from '@angular/material';
import { RenameComponent } from './dialog/rename/rename.component';
import { FormsModule } from '@angular/forms';
import { UncertainFolderImageComponent } from './pages/folder-image/uncertain-folder-image/uncertain-folder-image.component';
import { ConfirmComponent } from './dialog/confirm/confirm.component';
import { InfoComponent } from './snackbar/info/info.component';
import { PendingChangesGuard } from './guard/can-deactivate.guard';
import { ModalComponent } from './dialog/modal/modal.component';
import { NgxUiLoaderConfig, NgxUiLoaderModule } from 'ngx-ui-loader';
import { UncertainImageComponent } from './dialog/uncertain-image/uncertain-image.component';
import { FileUploadComponent } from './component/file-upload/file-upload.component';
import { LearningCurveComponent } from './dialog/learning-curve/learning-curve.component';


const ngxUiLoaderConfig: NgxUiLoaderConfig = {
	"bgsColor": "#2b3450",
	"bgsOpacity": 0.5,
	"bgsPosition": "bottom-right",
	"bgsSize": 60,
	"bgsType": "ball-spin-clockwise",
	"blur": 5,
	"fgsColor": "#2b3450",
	"fgsPosition": "center-center",
	"fgsSize": 70,
	"fgsType": "ball-spin-clockwise",
	"gap": 24,
	"logoPosition": "center-center",
	"logoSize": 120,
	"logoUrl": "",
	"masterLoaderId": "master",
	"overlayBorderRadius": "0",
	"overlayColor": "rgba(40, 40, 40, 0.8)",
	"pbColor": "#2b3450",
	"pbDirection": "ltr",
	"pbThickness": 3,
	"hasProgressBar": false,
	"text": "please wait...",
	"textColor": "#FFFFFF",
	"textPosition": "center-center",
};

@NgModule({
	declarations: [
		AppComponent,
		PageNotFoundComponent,
		HomeComponent,
		FolderComponent,
		FolderImageComponent,
		AppNavComponent,
		LoaderComponent,
		RenameComponent,
		UncertainFolderImageComponent,
		ConfirmComponent,
		InfoComponent,
		ModalComponent,
		FileUploadComponent,
		UncertainImageComponent,
		LearningCurveComponent
	],
	imports: [
		BrowserModule,
		NgxUiLoaderModule.forRoot(ngxUiLoaderConfig),
		AppRoutingModule,
		HttpClientModule,
		BrowserAnimationsModule,
		MaterialModule,
		MatInputModule,
		FormsModule
	],
	entryComponents: [
		RenameComponent,
		ConfirmComponent,
		InfoComponent,
		ModalComponent,
		UncertainImageComponent,
		LearningCurveComponent
	],
	providers: [
		{provide: StorageBucket, useValue: 'image_labeling'},
		PathService,
		UrlString,
		MlService,
		PendingChangesGuard,
		{
			provide: HTTP_INTERCEPTORS,
			useClass: LoaderInterceptorService,
			multi: true
		},
		{provide: MAT_DIALOG_DEFAULT_OPTIONS, useValue: {hasBackdrop: true}}
	],
	bootstrap: [AppComponent]
})
export class AppModule {
}
