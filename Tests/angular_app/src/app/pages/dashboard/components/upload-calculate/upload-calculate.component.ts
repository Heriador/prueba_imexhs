import { Component, OnInit } from '@angular/core';
import { UploadImageService } from 'src/app/services/upload-image/upload-image.service';

@Component({
  selector: 'app-upload-calculate',
  templateUrl: './upload-calculate.component.html',
  styleUrls: ['./upload-calculate.component.scss'],
  standalone: false
})
export class UploadCalculateComponent implements OnInit {

  imageSrc: string | ArrayBuffer | null = null;
  imageDimensions: { width: number, height: number } = { width: 0, height: 0 };
  number_points_generate: number = 0;
  estimatedArea: number = 0;

  constructor(
    private uploadImageService: UploadImageService
  ) {
    this.uploadImageService.getBinaryImage().subscribe(binaryImage => {
      this.imageSrc = binaryImage;
    });
    this.uploadImageService.$imageDimensions.subscribe(dimensions => {
      this.imageDimensions = dimensions;
    } );
  }

  ngOnInit(): void {
  }

  onFileChange(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
  
    if (file) {
      this.uploadImageService.receiveImage(file);
    }
  }

}
