import { TestBed } from '@angular/core/testing';

import { UploadCalculateService } from './upload-calculate.service';

describe('UploadImageService', () => {
  let service: UploadCalculateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UploadCalculateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
