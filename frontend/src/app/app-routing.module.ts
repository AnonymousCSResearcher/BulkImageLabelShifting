import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { PageNotFoundComponent } from './pages/page-not-found/page-not-found.component';
import { FolderImageComponent } from './pages/folder-image/folder-image.component';
import { UncertainFolderImageComponent } from './pages/folder-image/uncertain-folder-image/uncertain-folder-image.component';


const routes: Routes = [
	{path: '', redirectTo: '/home', pathMatch: 'full'},
	{path: 'home', component: HomeComponent},
	{
		path: 'folder-image/:catName/:folder/:dictionary',
		component: FolderImageComponent

	},
	{
		path: 'folder-image-uncertain/:catName/:dictionary',
		component: UncertainFolderImageComponent,

	},
	{path: '**', component: PageNotFoundComponent}
];

@NgModule({
	imports: [RouterModule.forRoot(routes)],
	exports: [RouterModule]
})
export class AppRoutingModule {
}
