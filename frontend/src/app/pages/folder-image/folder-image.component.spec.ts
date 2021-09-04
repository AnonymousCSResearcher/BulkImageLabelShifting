import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FolderImageComponent } from './folder-image.component';

describe('FolderImageComponent', () => {
  let component: FolderImageComponent;
  let fixture: ComponentFixture<FolderImageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FolderImageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FolderImageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
