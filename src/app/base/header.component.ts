import {Component, EventEmitter, Output} from '@angular/core';
import {AuthService} from '../auth/auth.service';

@Component({
    selector: 'app-header',
    templateUrl: './header.component.html'
})
export class HeaderComponent {
    @Output() setAuthorized = new EventEmitter<boolean>();

    constructor(private authService: AuthService) {
    }


    logout(): void {
        this.authService.logout();
        this.setAuthorized.emit(this.authService.authorized);
    }
}