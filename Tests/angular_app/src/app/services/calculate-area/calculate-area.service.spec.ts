import { TestBed } from '@angular/core/testing';

import { CalculateAreaService } from './calculate-area.service';

describe('CalculateAreaService', () => {
  let service: CalculateAreaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CalculateAreaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
