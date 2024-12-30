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

  constructor(
    private uploadImageService: UploadImageService
  ) {
    this.uploadImageService.getBinaryImage().subscribe(binaryImage => {
      this.imageSrc = binaryImage;
    });
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
