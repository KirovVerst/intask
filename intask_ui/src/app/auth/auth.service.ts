import {Injectable} from '@angular/core';

@Injectable()
export class AuthService {
    authorized = true;

    login(): void {
        this.authorized = true;
    }

    logout(): void {
        this.authorized = false;
    }
}
