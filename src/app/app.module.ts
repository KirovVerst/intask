import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {HeaderComponent} from './base/header.component';
import {AuthComponent} from './auth/auth.component';
import {AuthService} from './auth/auth.service';
import {HttpModule} from '@angular/http';

@NgModule({
    declarations: [
        AppComponent,
        HeaderComponent,
        AuthComponent
    ],
    imports: [
        BrowserModule,
        HttpModule
    ],
    providers: [AuthService],
    bootstrap: [AppComponent]
})
export class AppModule {
}
