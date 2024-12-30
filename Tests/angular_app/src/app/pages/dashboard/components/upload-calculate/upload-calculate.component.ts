import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-upload-calculate',
  templateUrl: './upload-calculate.component.html',
  styleUrls: ['./upload-calculate.component.scss'],
  standalone: false
})
export class UploadCalculateComponent implements OnInit {

  imageSrc: string | ArrayBuffer | null = null;

  constructor() { }

  ngOnInit(): void {
  }

  onFileChange(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
  
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        this.imageSrc = reader.result;

      };
      reader.readAsDataURL(file);
    }
  }


  
}
