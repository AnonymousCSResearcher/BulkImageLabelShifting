import { NgModule } from '@angular/core';
import {
	MatButtonModule,
	MatCheckboxModule,
	MatIconModule,
	MatListModule,
	MatSidenavModule,
	MatToolbarModule,
	MatProgressBarModule,
	MatCardModule,
	MatTableModule,
	MatSortModule,
	MatProgressSpinnerModule,
	MatPaginatorModule,
	MatFormFieldModule,
	MatSelectModule, MatDialogModule, MatSnackBarModule, MatExpansionModule
} from '@angular/material';
import { LayoutModule } from '@angular/cdk/layout';
import { DragDropModule } from '@angular/cdk/drag-drop';
import { MatFileUploadModule } from 'angular-material-fileupload';
import { ScrollDispatchModule } from '@angular/cdk/scrolling';


@NgModule({
	imports: [
		MatCheckboxModule,
		LayoutModule,
		DragDropModule,
		MatToolbarModule,
		MatButtonModule,
		MatSidenavModule,
		MatIconModule,
		MatListModule,
		MatFileUploadModule,
		MatProgressBarModule,
		MatCardModule,
		MatTableModule,
		MatSortModule,
		MatProgressSpinnerModule,
		MatPaginatorModule,
		MatFormFieldModule,
		MatSelectModule,
		MatDialogModule,
		MatSnackBarModule,
		ScrollDispatchModule,
		MatExpansionModule


	],
	exports: [
		MatCheckboxModule,
		LayoutModule,
		DragDropModule,
		MatToolbarModule,
		MatButtonModule,
		MatSidenavModule,
		MatIconModule,
		MatListModule,
		MatProgressBarModule,
		MatFileUploadModule,
		MatCardModule,
		MatTableModule,
		MatSortModule,
		MatProgressSpinnerModule,
		MatPaginatorModule,
		MatFormFieldModule,
		MatSelectModule,
		MatDialogModule,
		MatSnackBarModule,
		ScrollDispatchModule,
		MatExpansionModule
	]
})
export class MaterialModule {
}
