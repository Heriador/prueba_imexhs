import { Component, OnInit } from '@angular/core';
import { Point } from 'src/app/interfaces/point.interface';
import { UploadCalculateService } from 'src/app/services/upload-calculate/upload-calculate.service';

@Component({
  selector: 'app-upload-calculate',
  templateUrl: './upload-calculate.component.html',
  styleUrls: ['./upload-calculate.component.scss'],
  standalone: false
})
export class UploadCalculateComponent implements OnInit {

  imageSrc: string | ArrayBuffer | null = null;
  drawImage: string | ArrayBuffer | null = null;
  imageDimensions: { width: number, height: number } = { width: 0, height: 0 };
  number_points_generate: number = 0;
  estimatedArea: number = 0;

  constructor(
    private uploadImageService: UploadCalculateService
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

  calculateArea(){
    if(!this.imageSrc)
      return;

    let points: Point[] = []

    this.uploadImageService.generateRandomPoints(this.number_points_generate).subscribe({
      next: (pointsGenerated) => {
        points = pointsGenerated;
      },
      error: (error) => {
        console.error(error);
      }
    });
    console.log(points)

    this.uploadImageService.drawPointsOnImage(points, this.imageSrc.toString()).subscribe({
      next: (binaryImageWithPoints) => {
        this.drawImage = binaryImageWithPoints
      },
      error: (error) => {
        console.error(error);
      }
    });

    this.uploadImageService.countPointsInsideStain(points).subscribe({
      next: (pointsInsideStain) => {
        console.log(pointsInsideStain);
        this.estimatedArea = (pointsInsideStain / this.number_points_generate) * this.imageDimensions.width * this.imageDimensions.height;

      },
      error: (error) => {
        console.error(error);
      }
    });


  }

}
