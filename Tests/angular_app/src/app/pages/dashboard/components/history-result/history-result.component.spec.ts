import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HistoryResultComponent } from './history-result.component';

describe('HistoryResultComponent', () => {
  let component: HistoryResultComponent;
  let fixture: ComponentFixture<HistoryResultComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HistoryResultComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HistoryResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
