import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadCalculateComponent } from './upload-calculate.component';

describe('UploadCalculateComponent', () => {
  let component: UploadCalculateComponent;
  let fixture: ComponentFixture<UploadCalculateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UploadCalculateComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UploadCalculateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  
});
