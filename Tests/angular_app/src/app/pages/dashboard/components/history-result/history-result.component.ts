import { Component, OnInit } from '@angular/core';
import { AreaResult } from 'src/app/interfaces/area-result.interface';
import { UploadCalculateService } from 'src/app/services/upload-calculate/upload-calculate.service';

@Component({
  selector: 'app-history-result',
  templateUrl: './history-result.component.html',
  styleUrls: ['./history-result.component.scss'],
  standalone: false
})
export class HistoryResultComponent implements OnInit {

  public historyResults: any[] = [];
  displayedColumns: string[] = ['number_points', 'estimated_area'];

  constructor(
    private readonly uploadService: UploadCalculateService,
  ) {
    this.uploadService.$previousAreaResults.subscribe({
      next: (results) => {
        this.historyResults = results;
      },
      error: (error) => {
        console.error(error);
      }
    })
  }

  ngOnInit(): void {
  }

}
