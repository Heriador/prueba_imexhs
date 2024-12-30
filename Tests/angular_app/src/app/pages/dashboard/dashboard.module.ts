import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './dashboard.component';
import { DashboardRoutingModule } from './dashboard-routing.module';
import { MatTabsModule } from '@angular/material/tabs';
import { MatButtonModule } from '@angular/material/button'
import { MatIconModule } from '@angular/material/icon';
import { UploadCalculateComponent } from './components/upload-calculate/upload-calculate.component'


@NgModule({
  declarations: [
    DashboardComponent,
    UploadCalculateComponent,
  ],
  imports: [
    CommonModule,
    DashboardRoutingModule,
    MatTabsModule,
    MatButtonModule,
    MatIconModule
  ]
})
export class DashboardModule { }
