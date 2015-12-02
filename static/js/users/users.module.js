(function () {
    'use strict';

    angular
        .module('application.users', [
            'application.users.services',
            'application.users.controllers'

        ]);

    angular
        .module('application.users.controllers', []);

    angular
        .module('application.users.services', ['ngResource']);

})();
