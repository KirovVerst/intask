import {Component, OnInit, Output, EventEmitter} from '@angular/core';
import {AuthService} from './auth.service';

@Component({
    selector: 'app-auth',
    templateUrl: './auth.component.html'
})
export class AuthComponent implements OnInit {
    @Output() setAuthorized = new EventEmitter<boolean>();


    isRegistering: boolean;

    constructor(private authService: AuthService) {
    }

    ngOnInit(): void {
        this.isRegistering = false;
    }

    toggleForm(): void {
        this.isRegistering = !this.isRegistering;
    }

    login(): void {
        this.authService.login();
        this.setAuthorized.emit(this.authService.authorized);
    }
}