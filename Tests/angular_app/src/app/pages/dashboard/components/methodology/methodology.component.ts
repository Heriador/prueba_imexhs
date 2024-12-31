import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-methodology',
  templateUrl: './methodology.component.html',
  styleUrls: ['./methodology.component.scss'],
  standalone: false
})
export class MethodologyComponent implements OnInit {

  steps = [
    {
      title: 'Step 1: Upload Image',
      description: 'Upload a image where black pixels represent the stain and white pixels represent the background.'
    },
    {
      title: 'Step 2: Generate Random Points',
      description: 'Choose the number of random points to generate inside the image dimensions.'
    },
    {
      title: 'Step 3: Count Points in Stain',
      description: 'The algorithm generates the number of random points within image dimensions, then paints them in the uploaded image and counts which points fell inside the stain.'
    },
    {
      title: 'Step 4: Estimate Area',
      description: 'Calculate the estimated stain area using the formula: Area = (Image Area) × (Points in Stain / Total Points).'
    }
  ];


  constructor() { }

  ngOnInit(): void {
  }

}
