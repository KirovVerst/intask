import {Component, EventEmitter, Output} from '@angular/core';
import {AuthService} from '../auth/auth.service';
import {Http, Headers, RequestOptions} from '@angular/http';

import 'rxjs/add/operator/toPromise';

@Component({
    selector: 'app-header',
    templateUrl: './header.component.html'
})
export class HeaderComponent {
    @Output() setStatus = new EventEmitter<boolean>();

    private headers = new Headers({'Content-Type': 'application/json'});
    private options = new RequestOptions({headers: this.headers});

    constructor(private authService: AuthService, private http: Http) {
    }

    send(): void {
        const url = 'api/v1/auth/login/';
        this.http.post(url, this.options)
            .toPromise().then(res => res.json().data);
    }

    logout(): void {
        this.authService.logout();
        this.setStatus.emit(this.authService.authorized);
    }
}
