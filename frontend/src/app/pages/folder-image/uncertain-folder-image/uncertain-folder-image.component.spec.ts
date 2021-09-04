import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UncertainFolderImageComponent } from './uncertain-folder-image.component';

describe('UncertainFolderImageComponent', () => {
  let component: UncertainFolderImageComponent;
  let fixture: ComponentFixture<UncertainFolderImageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UncertainFolderImageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UncertainFolderImageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
