import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';
import { AreaResult } from 'src/app/interfaces/area-result.interface';
import { Point } from 'src/app/interfaces/point.interface';

@Injectable({
  providedIn: 'root'
})
export class UploadCalculateService {

  private binaryImage: BehaviorSubject<string | ArrayBuffer | null> = new BehaviorSubject<string | ArrayBuffer | null>(null);
  private imageDimensions: BehaviorSubject<{ width: number, height: number }> = new BehaviorSubject<{ width: number, height: number }>({ width: 0, height: 0 });
  private previousAreaResults: BehaviorSubject<AreaResult[]> = new BehaviorSubject<AreaResult[]>([]);

  public $imageDimensions = this.imageDimensions.asObservable();
  public $previousAreaResults = this.previousAreaResults.asObservable();

  constructor() { }


  receiveImage(image: File): void {
    const reader = new FileReader();

    // Convert image to binary
    reader.onload = (e) => {
      const img = new Image();
      img.src = reader.result as string;
      img.onload = () => {
       const result = this.convertToBinaryImage(img);
       this.binaryImage.next(result);
       this.imageDimensions.next({ width: img.width, height: img.height });
      };
    };
    reader.readAsDataURL(image);
  }

  private convertToBinaryImage(img: HTMLImageElement): string {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    if (!context) {
      return '';
    }

    canvas.width = img.width;
    canvas.height = img.height;
    context.drawImage(img, 0, 0);

    const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    // Convert to grayscale
    for (let i = 0; i < data.length; i += 4) {
      const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
      data[i] = avg;
      data[i + 1] = avg;
      data[i + 2] = avg;
    }

    // convert to binary
    const threshold = 128;
    for (let i = 0; i < data.length; i += 4) {
      const value = data[i] > threshold ? 255 : 0;
      data[i] = value;
      data[i + 1] = value;
      data[i + 2] = value;
    }

    context.putImageData(imageData, 0, 0);
    return canvas.toDataURL();
  }

  // Observable to get the binary image
  getBinaryImage(): Observable<string | ArrayBuffer | null> {
    return this.binaryImage.asObservable();
  }

  generateRandomPoints(number_points: number): Observable<Point[]> {

    const points: Point[] = [];
    const dimensions = this.imageDimensions.value;
    for (let i = 0; i < number_points; i++) {
      points.push({
        x: Math.floor(Math.random() * dimensions.width),
        y: Math.floor(Math.random() * dimensions.height)
      });
    }

    return new Observable<Point[]>(observer => {
      observer.next(points);
      observer.complete();
    });
  }

  drawPointsOnImage(points: {x: number, y:number}[], binaryImageSrc: string): Observable<string> {
    return new Observable<string>(observer => {
      const img = new Image();
      img.src = binaryImageSrc;

      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      if (!context) {
        observer.error('');
        return;
      }

      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        context.drawImage(img, 0, 0);

        context.fillStyle = 'red';
        points.forEach(point => {
          context.beginPath();
          context.arc(point.x, point.y, 1, 0, 2 * Math.PI);
          context.fill();
        })
        observer.next(canvas.toDataURL());
        observer.complete();
      }

    });
  }

  estimateAreaOfStain(points: Point[]): Observable<number> { 
    
    return new Observable<number>(observer => {
      let count = 0;
      const img = new Image();
      img.src = this.binaryImage.value as string;
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      if (!context) {
        observer.error(0);
        return;
      }

      // Wait for image to load
      img.onload = () => {

        // Draw image on canvas
        canvas.width = img.width;
        canvas.height = img.height;
        context.drawImage(img, 0, 0);

        // Get image data
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;

        // Count points inside the stain
        points.forEach(point => {
          const index = (point.y * canvas.width + point.x) * 4;
          if (data[index] === 0) {
            count++;
          }
        });

        // Calculate estimated area
        const estimatedArea = (count / points.length) * canvas.width * canvas.height;

        // add result to previous results
        const previousResults = this.previousAreaResults.value;
        previousResults.push({ number_points: points.length, estimated_area: estimatedArea });
        observer.next(estimatedArea);
        observer.complete();
      }
    });
  }

}
