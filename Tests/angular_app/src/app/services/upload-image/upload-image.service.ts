import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UploadImageService {

  private binaryImage: Subject<string | ArrayBuffer | null> = new Subject<string | ArrayBuffer | null>();


  constructor() { }


  receiveImage(image: File): void {
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.src = reader.result as string;
      img.onload = () => {
       const result = this.convertToBinaryImage(img);
       this.binaryImage.next(result);
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

    // Convertir a escala de grises
    for (let i = 0; i < data.length; i += 4) {
      const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
      data[i] = avg;
      data[i + 1] = avg;
      data[i + 2] = avg;
    }

    // Aplicar umbral para convertir a binario
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

  // Observable para obtener la imagen binaria
  getBinaryImage(): Observable<string | ArrayBuffer | null> {
    return this.binaryImage.asObservable();
  }

}
