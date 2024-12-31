import { AfterViewInit, Component, OnInit} from '@angular/core';
import { AreaResult } from 'src/app/interfaces/area-result.interface';
import { UploadCalculateService } from '../../../../services/upload-calculate/upload-calculate.service';

@Component({
  selector: 'app-history-result',
  templateUrl: './history-result.component.html',
  styleUrls: ['./history-result.component.scss'],
  standalone: false
})
export class HistoryResultComponent implements OnInit, AfterViewInit {

  public historyResults: AreaResult[] = [];

  constructor(
    private readonly uploadService: UploadCalculateService,
  ) {
    
  }

  ngOnInit(): void {
    
  }

  ngAfterViewInit(): void {
    this.uploadService.$previousAreaResults.subscribe({
      next: (results) => {
        this.historyResults = results;
      },
      error: (error) => {
        console.error(error);
      }
    })
  }

}
