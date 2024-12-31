import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './dashboard.component';
import { DashboardRoutingModule } from './dashboard-routing.module';
import { MatTabsModule } from '@angular/material/tabs';
import { MatButtonModule } from '@angular/material/button'
import { MatIconModule } from '@angular/material/icon';
import { UploadCalculateComponent } from './components/upload-calculate/upload-calculate.component'
import { MatSliderModule } from '@angular/material/slider'
import { FormsModule } from '@angular/forms';
import { HistoryResultComponent } from './components/history-result/history-result.component';
import {MatTableModule} from '@angular/material/table';
import { MatStepperModule } from '@angular/material/stepper'
import { MethodologyComponent } from './components/methodology/methodology.component';

@NgModule({
  declarations: [
    DashboardComponent,
    UploadCalculateComponent,
    HistoryResultComponent,
    MethodologyComponent,
  ],
  imports: [
    CommonModule,
    DashboardRoutingModule,
    MatTabsModule,
    MatButtonModule,
    MatIconModule,
    MatSliderModule,
    FormsModule,
    MatTableModule,
    MatStepperModule
]
})
export class DashboardModule { }
